nst override;
            Real floorPrice(const Date& d, Rate k) const override;
            //@}

        protected:

            // data for surfaces and curve
            mutable Matrix cPriceB_;
            mutable Matrix fPriceB_;
            mutable Interpolation2D capPrice_, floorPrice_;
            mutable Interpolator2D interpolator2d_;
    };


    // template definitions, for some reason DOXYGEN doesn't like the first one

    #ifndef __DOXYGEN__

    template<class Interpolator2D>
    InterpolatedCPICapFloorTermPriceSurface<Interpolator2D>::
    InterpolatedCPICapFloorTermPriceSurface(Real nominal,
                                            Rate startRate,
                                            const Period &observationLag,
                                            const Calendar &cal,
                                            const BusinessDayConvention &bdc,
                                            const DayCounter &dc,
                                            const ext::shared_ptr<ZeroInflationIndex>& zii,
                                            CPI::InterpolationType interpolationType,
                                            const Handle<YieldTermStructure>& yts,
                                            const std::vector<Rate> &cStrikes,
                                            const std::vector<Rate> &fStrikes,
                                            const std::vector<Period> &cfMaturities,
                                            const Matrix &cPrice,
                                            const Matrix &fPrice,
                                            const Interpolator2D &interpolator2d)
    : CPICapFloorTermPriceSurface(nominal, startRate, observationLag, cal, bdc, dc,
                                  zii, interpolationType, yts, cStrikes, fStrikes,
                                  cfMaturities, cPrice, fPrice),
      interpolator2d_(interpolator2d) {
        performCalculations();
    }

    #endif

    //! set up the interpolations for capPrice_ and floorPrice_
    //! since we know ATM, and we have single flows,
    //! we can use put/call parity to extend the surfaces
    //! across all strikes
    template<class I2D>
    void InterpolatedCPICapFloorTermPriceSurface<I2D>::
    performCalculations() const {

        cPriceB_ =
            Matrix(cfStrikes_.size(), cfMaturities_.size(), Null<Real>());
        fPriceB_ =
            Matrix(cfStrikes_.size(), cfMaturities_.size(), Null<Real>());

        Handle<YieldTermStructure> yts = nominalTS_;
        QL_REQUIRE(!yts.empty(), "Yts is empty!!!");

        for (Size j = 0; j < cfMaturities_.size(); ++j) {
            Period mat = cfMaturities_[j];
            Real df = yts->discount(cpiOptionDateFromTenor(mat));
            Real atm_quote = atmRate(cpiOptionDateFromTenor(mat));
            Real atm = std::pow(1.0 + atm_quote, mat.length());
            Real S = atm * df;
            for (Size i = 0; i < cfStrikes_.size(); ++i) {
                Real K_quote = cfStrikes_[i];
                Real K = std::pow(1.0 + K_quote, mat.length());
                auto close = [k = cfStrikes_[i]](Real x){ return close_enough(x, k); };
                Size indF = std::find_if(fStrikes_.begin(), fStrikes_.end(), close) - fStrikes_.begin();
                Size indC = std::find_if(cStrikes_.begin(), cStrikes_.end(), close) - cStrikes_.begin();
                bool isFloorStrike = indF < fStrikes_.size();
                bool isCapStrike = indC < cStrikes_.size();
                if (isFloorStrike) {
                    fPriceB_[i][j] = fPrice_[indF][j];
                    if (!isCapStrike) {
                        cPriceB_[i][j] = fPrice_[indF][j] + S - K * df;
                    }
                }
                if (isCapStrike) {
                    cPriceB_[i][j] = cPrice_[indC][j];
                    if (!isFloorStrike) {
                        fPriceB_[i][j] = cPrice_[indC][j] + K * df - S;
                    