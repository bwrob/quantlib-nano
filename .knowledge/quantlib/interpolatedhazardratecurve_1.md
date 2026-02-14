definitions

    template <class T>
    inline Date InterpolatedHazardRateCurve<T>::maxDate() const {
        return dates_.back();
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedHazardRateCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedHazardRateCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedHazardRateCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<Rate>&
    InterpolatedHazardRateCurve<T>::hazardRates() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date, Real> >
    InterpolatedHazardRateCurve<T>::nodes() const {
        std::vector<std::pair<Date, Real> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i], this->data_[i]);
        return results;
    }

    #ifndef __DOXYGEN__

    // template definitions

    template <class T>
    Real InterpolatedHazardRateCurve<T>::hazardRateImpl(Time t) const {
        if (t <= this->times_.back())
            return this->interpolation_(t, true);

        // flat hazard rate extrapolation
        return this->data_.back();
    }

    template <class T>
    Probability
    InterpolatedHazardRateCurve<T>::survivalProbabilityImpl(Time t) const {
        if (t == 0.0)
            return 1.0;

        Real integral;
        if (t <= this->times_.back()) {
            integral = this->interpolation_.primitive(t, true);
        } else {
            // flat hazard rate extrapolation
            integral = this->interpolation_.primitive(this->times_.back(), true)
                     + this->data_.back()*(t - this->times_.back());
        }
        return std::exp(-integral);
    }

    template <class T>
    InterpolatedHazardRateCurve<T>::InterpolatedHazardRateCurve(
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : HazardRateStructure(dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedHazardRateCurve<T>::InterpolatedHazardRateCurve(
                                    const Date& referenceDate,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : HazardRateStructure(referenceDate, Calendar(), dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedHazardRateCurve<T>::InterpolatedHazardRateCurve(
                                    Natural settlementDays,
                                    const Calendar& calendar,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : HazardRateStructure(settlementDays, calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedHazardRateCurve<T>::InterpolatedHazardRateCurve(
                                    const std::vector<Date>& dates,
                                    const std::vector<Rate>& hazardRates,
                                    const DayCounter& dayCounter,
                                    const Calendar& calendar,
                                    const std::vector<Handle<Quote> >& jum