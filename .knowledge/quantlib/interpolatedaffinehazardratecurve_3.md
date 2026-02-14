(-integral) * model_->discountBond(0., t, initValHR);
    }

    template <class T>
    Probability
    InterpolatedAffineHazardRateCurve<T>::conditionalSurvivalProbabilityImpl(
        Time tFwd, Time tTarget, Real yVal) const 
    {
        QL_REQUIRE(tFwd <= tTarget, "Probability time in the past.");
        // Still leaves the possibility of sending tFwd=0 and an yVal different
        //   to the initial conditions. In an abstract sense thats all right as
        //   long as it is seen as a zero probability scenario.
        #if defined(QL_EXTRA_SAFETY_CHECKS)
            QL_REQUIRE(tFwd > 0. || yVal == 
                model_->dynamics()->process()->x0(), 
                "Initial value different to process'.");
        #endif
        if (tFwd == 0.) return survivalProbabilityImpl(tTarget);
        if (tFwd - tTarget == 0.0)
            return 1.;

        Real integralTFwd, integralTP;
        if (tFwd <= this->times_.back()) {
            integralTFwd = this->interpolation_.primitive(tFwd, true);
        } else {
            // flat hazard rate extrapolation
            integralTFwd = 
                this->interpolation_.primitive(this->times_.back(), true)
                     + this->data_.back()*(tFwd - this->times_.back());
        }
        if (tTarget <= this->times_.back()) {
            integralTP = this->interpolation_.primitive(tTarget, true);
        } else {
            // flat hazard rate extrapolation
            integralTP = 
                this->interpolation_.primitive(this->times_.back(), true)
                     + this->data_.back()*(tTarget - this->times_.back());
        }

        return std::exp(-(integralTP-integralTFwd)) * 
            model_->discountBond(tFwd, tTarget, yVal );
    }

    template <class T>
    InterpolatedAffineHazardRateCurve<T>::InterpolatedAffineHazardRateCurve(
        const DayCounter& dayCounter,
        const ext::shared_ptr<OneFactorAffineModel>& model,
        const std::vector<Handle<Quote> >& jumps,
        const std::vector<Date>& jumpDates,
        const T& interpolator)
    : OneFactorAffineSurvivalStructure(model, dayCounter, jumps, jumpDates), InterpolatedCurve<T>(
                                                                                 interpolator) {}

    template <class T>
    InterpolatedAffineHazardRateCurve<T>::InterpolatedAffineHazardRateCurve(
        const Date& referenceDate,
        const DayCounter& dayCounter,
        const ext::shared_ptr<OneFactorAffineModel>& model,
        const std::vector<Handle<Quote> >& jumps,
        const std::vector<Date>& jumpDates,
        const T& interpolator)
    : OneFactorAffineSurvivalStructure(
          model, referenceDate, Calendar(), dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedAffineHazardRateCurve<T>::InterpolatedAffineHazardRateCurve(
        Natural settlementDays,
        const Calendar& calendar,
        const DayCounter& dayCounter,
        const ext::shared_ptr<OneFactorAffineModel>& model,
        const std::vector<Handle<Quote> >& jumps,
        const std::vector<Date>& jumpDates,
        const T& interpolator)
    : OneFactorAffineSurvivalStructure(
          model, settlementDays, calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedAffineHazardRateCurve<T>::InterpolatedAffineHazardRateCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& hazardRates,
        const DayCounter& dayCounter,
        const ext::shared_ptr<OneFactorAffineModel>& model,
        const Calendar& calendar,
        const std::vector<Handle<Quote> >& jumps,
        const std::vector<Date>& jumpDates,
        const T& interpolator)
    : OneFactorAffineSurvivalStructure(model, dates.at(0), calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(std::vector<Time>(), hazardRates, interpolator), dates_(dates) {
        initialize();
   