st DayCounter& dayCounter);
    };

    // inline definitions

    template <class T>
    inline Date InterpolatedDefaultDensityCurve<T>::maxDate() const {
        return dates_.back();
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedDefaultDensityCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedDefaultDensityCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedDefaultDensityCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedDefaultDensityCurve<T>::defaultDensities() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date, Real> >
    InterpolatedDefaultDensityCurve<T>::nodes() const {
        std::vector<std::pair<Date, Real> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i], this->data_[i]);
        return results;
    }

    #ifndef __DOXYGEN__

    // template definitions

    template <class T>
    Real InterpolatedDefaultDensityCurve<T>::defaultDensityImpl(Time t) const {
        if (t <= this->times_.back())
            return this->interpolation_(t, true);

        // flat default density extrapolation
        return this->data_.back();
    }

    template <class T>
    Probability
    InterpolatedDefaultDensityCurve<T>::survivalProbabilityImpl(Time t) const {
        if (t == 0.0)
            return 1.0;

        Real integral = 0.0;
        if (t <= this->times_.back()) {
            integral = this->interpolation_.primitive(t, true);
        } else {
            // flat default density extrapolation
            integral = this->interpolation_.primitive(this->times_.back(), true)
                     + this->data_.back()*(t - this->times_.back());
        }
        Probability P = 1.0 - integral;
        // QL_ENSURE(P >= 0.0, "negative survival probability");
        return std::max<Real>(P, 0.0);
    }

    template <class T>
    InterpolatedDefaultDensityCurve<T>::InterpolatedDefaultDensityCurve(
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : DefaultDensityStructure(dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedDefaultDensityCurve<T>::InterpolatedDefaultDensityCurve(
                                    const Date& referenceDate,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : DefaultDensityStructure(referenceDate, Calendar(), dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedDefaultDensityCurve<T>::InterpolatedDefaultDensityCurve(
                                    Natural settlementDays,
                                    const Calendar& calendar,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : DefaultDensityStructure(settlementDays, calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedDefaultDensityCurve<T>::InterpolatedDefaultDensityCurve(
                                    const std::vector<Date>& dates,
                   