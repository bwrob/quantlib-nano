ates_;
    private:
        void initialize();
    };

    // inline definitions

    template <class T>
    inline Date InterpolatedSurvivalProbabilityCurve<T>::maxDate() const {
        return dates_.back();
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedSurvivalProbabilityCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedSurvivalProbabilityCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedSurvivalProbabilityCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<Probability>&
    InterpolatedSurvivalProbabilityCurve<T>::survivalProbabilities() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date,Real> >
    InterpolatedSurvivalProbabilityCurve<T>::nodes() const {
        std::vector<std::pair<Date,Real> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i],this->data_[i]);
        return results;
    }

    #ifndef __DOXYGEN__

    // template definitions

    template <class T>
    Probability
    InterpolatedSurvivalProbabilityCurve<T>::survivalProbabilityImpl(Time t)
                                                                        const {
        if (t <= this->times_.back())
            return this->interpolation_(t, true);

        // flat hazard rate extrapolation
        Time tMax = this->times_.back();
        Probability sMax = this->data_.back();
        Rate hazardMax = - this->interpolation_.derivative(tMax) / sMax;
        return sMax * std::exp(- hazardMax * (t-tMax));
    }

    template <class T>
    Real
    InterpolatedSurvivalProbabilityCurve<T>::defaultDensityImpl(Time t) const {
        if (t <= this->times_.back())
            return -this->interpolation_.derivative(t, true);

        // flat hazard rate extrapolation
        Time tMax = this->times_.back();
        Probability sMax = this->data_.back();
        Rate hazardMax = - this->interpolation_.derivative(tMax) / sMax;
        return sMax * hazardMax * std::exp(- hazardMax * (t-tMax));
    }

    template <class T>
    InterpolatedSurvivalProbabilityCurve<T>::InterpolatedSurvivalProbabilityCurve(
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : SurvivalProbabilityStructure(dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedSurvivalProbabilityCurve<T>::InterpolatedSurvivalProbabilityCurve(
                                    const Date& referenceDate,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : SurvivalProbabilityStructure(referenceDate, Calendar(), dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedSurvivalProbabilityCurve<T>::InterpolatedSurvivalProbabilityCurve(
                                    Natural settlementDays,
                                    const Calendar& calendar,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : SurvivalProbabilityStructure(settlementDays, calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator)