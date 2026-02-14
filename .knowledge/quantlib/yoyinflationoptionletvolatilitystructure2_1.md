 we have no data
        // this is protected as we only expect to use it in the
        // piecewise versions
        InterpolatedYoYOptionletVolatilityCurve(Natural settlementDays,
                                                const Calendar&,
                                                BusinessDayConvention bdc,
                                                const DayCounter& dc,
                                                const Period &lag,
                                                Frequency frequency,
                                                bool indexIsInterpolated,
                                                Rate minStrike,
                                                Rate maxStrike,
                                                Volatility baseYoYVolatility,
                                                const Interpolator1D &i =
                                                            Interpolator1D());

        // we do specify data representation here
        // because the bootstrapper needs this specifically
        mutable std::vector<Date> dates_;
        std::vector<std::pair<Date, Real> > nodes_;
        //@}

        //! implements the actual volatility calculation in derived classes
        Volatility volatilityImpl(Time length, Rate strike) const override;

        Rate minStrike_, maxStrike_;
    };



    template<class Interpolator1D>
    InterpolatedYoYOptionletVolatilityCurve<Interpolator1D>::
    InterpolatedYoYOptionletVolatilityCurve(Natural settlementDays,
                                            const Calendar &cal,
                                            BusinessDayConvention bdc,
                                            const DayCounter& dc,
                                            const Period &lag,
                                            Frequency frequency,
                                            bool indexIsInterpolated,
                                            const std::vector<Date> &d,
                                            const std::vector<Volatility> &v,
                                            Rate minStrike,
                                            Rate maxStrike,
                                            const Interpolator1D &i)
    : YoYOptionletVolatilitySurface(settlementDays, cal, bdc, dc, lag,
                                    frequency, indexIsInterpolated),
      InterpolatedCurve<Interpolator1D>(i),
      dates_(d), minStrike_(minStrike), maxStrike_(maxStrike) {
        QL_REQUIRE(d.size() == v.size(),
                   "must have same number of dates and vols: "
                   << d.size() << " vs " << v.size());
        QL_REQUIRE(d.size() > 1,
                   "must have at least two dates: " << d.size());

        for (Size j = 0; j < d.size(); j++ ){
            this->times_.push_back( this->timeFromReference(dates_[j]) );
            this->data_.push_back(v[j]),
            nodes_.push_back( std::make_pair( dates_[j], this->data_[j]) );
        }

        this->setupInterpolation();
        // set the base vol level to that predicted by the interpolation
        // this is allowed by the extrapolation
        Time baseTime = this->timeFromReference(baseDate());
        setBaseLevel(this->interpolation_(baseTime,true));
    }


    template<class Interpolator1D>
    InterpolatedYoYOptionletVolatilityCurve<Interpolator1D>::
    InterpolatedYoYOptionletVolatilityCurve(Natural settlementDays,
                                            const Calendar &cal,
                                            BusinessDayConvention bdc,
                                            const DayCounter& dc,
                                            const Period &lag,
                                            Frequency frequency,
                                            bool indexIsInterpolated,
                                            Rate minStrike,
                                            Rate m
