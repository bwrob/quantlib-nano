late = true) const = 0;
        virtual Rate atmYoYRate(const Date &d,
                                const Period &obsLag = Period(-1,Days),
                                bool extrapolate = true) const = 0;

        virtual Real price(const Period& d, Rate k) const;
        virtual Real capPrice(const Period& d, Rate k) const;
        virtual Real floorPrice(const Period& d, Rate k) const;
        virtual Rate atmYoYSwapRate(const Period &d,
                                    bool extrapolate = true) const;
        virtual Rate atmYoYRate(const Period &d,
                                const Period &obsLag = Period(-1,Days),
                                bool extrapolate = true) const;

        virtual std::vector<Rate> strikes() const {return cfStrikes_;}
        virtual std::vector<Rate> capStrikes() const {return cStrikes_;}
        virtual std::vector<Rate> floorStrikes() const {return fStrikes_;}
        virtual std::vector<Period> maturities() const {return cfMaturities_;}
        virtual Rate minStrike() const {return cfStrikes_.front();};
        virtual Rate maxStrike() const {return cfStrikes_.back();};
        virtual Date minMaturity() const {return referenceDate()+cfMaturities_.front();}// \TODO deal with index interpolation
        virtual Date maxMaturity() const {return referenceDate()+cfMaturities_.back();}
        //@}

        virtual Date yoyOptionDateFromTenor(const Period& p) const;

      protected:
        virtual bool checkStrike(Rate K) {
            return ( minStrike() <= K && K <= maxStrike() );
        }
        virtual bool checkMaturity(const Date& d) {
            return ( minMaturity() <= d && d <= maxMaturity() );
        }

        // defaults, mostly used for building yoy-fwd curve from put-call parity
        //  ext::shared_ptr<YieldTermStructure> nominal_;
        //  Period lag_;
        //  Calendar cal_;
        Natural fixingDays_;
        BusinessDayConvention bdc_;
        ext::shared_ptr<YoYInflationIndex> yoyIndex_;
        Period observationLag_;
        Handle<YieldTermStructure> nominalTS_;
        // data
        std::vector<Rate> cStrikes_;
        std::vector<Rate> fStrikes_;
        std::vector<Period> cfMaturities_;
        mutable std::vector<Real> cfMaturityTimes_;
        Matrix cPrice_;
        Matrix fPrice_;
        bool indexIsInterpolated_;
        // constructed
        mutable std::vector<Rate> cfStrikes_;
        mutable ext::shared_ptr<YoYInflationTermStructure> yoy_;
        mutable std::pair<std::vector<Time>, std::vector<Rate> > atmYoYSwapTimeRates_;
        mutable std::pair<std::vector<Date>, std::vector<Rate> > atmYoYSwapDateRates_;
    };


    template<class Interpolator2D, class Interpolator1D>
    class InterpolatedYoYCapFloorTermPriceSurface
        : public YoYCapFloorTermPriceSurface {
      public:
        InterpolatedYoYCapFloorTermPriceSurface(
                      Natural fixingDays,
                      const Period &yyLag,  // observation lag
                      const ext::shared_ptr<YoYInflationIndex>& yii,
                      CPI::InterpolationType interpolation,
                      const Handle<YieldTermStructure> &nominal,
                      const DayCounter &dc,
                      const Calendar &cal,
                      const BusinessDayConvention &bdc,
                      const std::vector<Rate> &cStrikes,
                      const std::vector<Rate> &fStrikes,
                      const std::vector<Period> &cfMaturities,
                      const Matrix &cPrice,
                      const Matrix &fPrice,
                      const Interpolator2D &interpolator2d = Interpolator2D(),
                      const Interpolator1D &interpolator1d = Interpolator1D());

        //! inflation term structure interface
        //@{
        Date maxDate() const override { return yoy_->maxDate(); }
        Date baseDate() const override { return yoy_->baseDate(); }
        //@}
        Natural fixingDays() const over