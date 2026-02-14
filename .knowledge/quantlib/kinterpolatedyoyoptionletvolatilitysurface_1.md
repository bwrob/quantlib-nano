t DayCounter& dc,
            const Period& lag,
            const ext::shared_ptr<YoYCapFloorTermPriceSurface>& capFloorPrices,
            ext::shared_ptr<YoYInflationCapFloorEngine> pricer,
            ext::shared_ptr<YoYOptionletStripper> yoyOptionletStripper,
            const Real slope,
            const Interpolator1D& interpolator,
            VolatilityType volType,
            Real displacement)
    : YoYOptionletVolatilitySurface(settlementDays,
                                    cal,
                                    bdc,
                                    dc,
                                    lag,
                                    capFloorPrices->yoyIndex()->frequency(),
                                    capFloorPrices->yoyIndex()->interpolated(),
                                    volType,
                                    displacement),
      capFloorPrices_(capFloorPrices), yoyInflationCouponPricer_(std::move(pricer)),
      yoyOptionletStripper_(std::move(yoyOptionletStripper)), factory1D_(interpolator),
      slope_(slope) {
        performCalculations();
    }


    template<class Interpolator1D>
    Date KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
    maxDate() const {
        Size n = capFloorPrices_->maturities().size();
        return referenceDate()+capFloorPrices_->maturities()[n-1];
    }


    template<class Interpolator1D>
    Real KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
    minStrike() const {
        return capFloorPrices_->strikes().front();
    }


    template<class Interpolator1D>
    Real KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
    maxStrike() const {
        return capFloorPrices_->strikes().back();
    }


    template<class Interpolator1D>
    void KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
    performCalculations() const {

        // slope is the assumption on the initial caplet volatility change
        yoyOptionletStripper_->initialize(capFloorPrices_,
                                          yoyInflationCouponPricer_,
                                          slope_);
    }


    template<class Interpolator1D>
    Volatility KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
    volatilityImpl(const Date &d, Rate strike) const {
        updateSlice(d);
        if (this->allowsExtrapolation()) {
            this->tempKinterpolation_.enableExtrapolation();
        }
        return tempKinterpolation_(strike);
    }


    template<class Interpolator1D>
    std::pair<std::vector<Rate>, std::vector<Volatility> >
    KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
    Dslice(const Date &d) const {
        updateSlice(d);
        return slice_;
    }


    template<class Interpolator1D>
    Volatility KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
    volatilityImpl(Time length,  Rate strike) const {

        auto years = (Natural)floor(length);
        auto days = (Natural)floor((length - years) * 365.0);
        Date d = referenceDate() + Period(years, Years) + Period(days, Days);

        return this->volatilityImpl(d, strike);
    }

    template<class Interpolator1D>
    void KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
    updateSlice(const Date &d) const {

        if (!lastDateisSet_ || d != lastDate_ ) {
            slice_ = yoyOptionletStripper_->slice(d);

            tempKinterpolation_ =
                factory1D_.interpolate( slice_.first.begin(),
                                        slice_.first.end(),
                                        slice_.second.begin() );
            lastDateisSet_ = true;
            lastDate_ = d;
        }
    }

}

#endif