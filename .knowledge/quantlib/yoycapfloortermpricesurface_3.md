CapFloorTermPriceSurface(fixingDays, yyLag, yii,
                                  interpolation, nominal, dc, cal, bdc,
                                  cStrikes, fStrikes, cfMaturities,
                                  cPrice, fPrice),
      interpolator2d_(interpolator2d), interpolator1d_(interpolator1d) {
        performCalculations();
    }

    #endif

    template<class I2D, class I1D>
    void InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::
    update() {
        notifyObservers();
    }


    template<class I2D, class I1D>
    void InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::
    performCalculations() const {
        // calculate all the useful things
        // ... first the intersection of the cap and floor surfs
        intersect();

        // ... then the yoy term structure, which requires instruments
        // and a bootstrap
        calculateYoYTermStructure();
    }


    template<class I2D, class I1D>
    InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::ObjectiveFunction::
    ObjectiveFunction(const Time t,
                      const Interpolation2D &a,
                      const Interpolation2D &b)
    : t_(t), a_(a), b_(b) {
        // do nothing more
    }


    template<class I2D, class I1D>
    Rate InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::
    price(const Date &d, const Rate k) const {
        Rate atm = atmYoYSwapRate(d);
        return k > atm ? capPrice(d,k): floorPrice(d,k);
    }


    template<class I2D, class I1D>
    Rate InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::
    capPrice(const Date &d, const Rate k) const {
        Time t = timeFromReference(d);
        return capPrice_(t,k);
    }


    template<class I2D, class I1D>
    Rate InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::
    floorPrice(const Date &d, const Rate k) const {
        Time t = timeFromReference(d);
        return floorPrice_(t,k);
    }


    template<class I2D, class I1D>
    Real InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::ObjectiveFunction::
    operator()(Rate guess) const {
        // allow extrapolation because the overlap is typically insufficient
        // looking for a zero
        return ( a_(t_,guess,true) - b_(t_,guess,true) );
    }


    template<class I2D, class I1D>
    void InterpolatedYoYCapFloorTermPriceSurface<I2D,I1D>::
    intersect() const {


        // TODO: define the constants outside the code
        const Real maxSearchRange = 0.0201;
        const Real maxExtrapolationMaturity = 5.01;
        const Real searchStep = 0.0050;
        const Real intrinsicValueAddOn = 0.001;

        std::vector<bool> validMaturity(cfMaturities_.size(),false);

        cfMaturityTimes_.clear();
        for (Size i=0; i<cfMaturities_.size();i++) {
            cfMaturityTimes_.push_back(timeFromReference(
                    yoyOptionDateFromTenor(cfMaturities_[i])));
        }

        capPrice_ = interpolator2d_.interpolate(
                            cfMaturityTimes_.begin(),cfMaturityTimes_.end(),
                            cStrikes_.begin(), cStrikes_.end(),
                            cPrice_
                            );
        capPrice_.enableExtrapolation();

        floorPrice_ = interpolator2d_.interpolate(
                            cfMaturityTimes_.begin(),cfMaturityTimes_.end(),
                            fStrikes_.begin(), fStrikes_.end(),
                            fPrice_
                            );
        floorPrice_.enableExtrapolation();

        atmYoYSwapDateRates_.first.clear();
        atmYoYSwapDateRates_.second.clear();
        atmYoYSwapTimeRates_.first.clear();
        atmYoYSwapTimeRates_.second.clear();
        Brent solver;
        Real solverTolerance_ = 1e-7;
        Real lo,hi,guess;
        std::vector<Real> minSwapRateIntersection(cfMaturityTimes_.size());
        std::vector<Real> maxSwapRateIntersection(cfMaturityTimes_.size());
        std::vector<Time> tmpSwapMaturities;
        std::vector<Rate> tmpSwapRates;
        for (Si
