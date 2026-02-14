Flat> ForwardCurve;


    // inline definitions

    template <class T>
    inline Date InterpolatedForwardCurve<T>::maxDate() const {
        if (this->maxDate_ != Date())
           return this->maxDate_;
        return dates_.back();
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedForwardCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedForwardCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedForwardCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<Rate>&
    InterpolatedForwardCurve<T>::forwards() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date, Real> >
    InterpolatedForwardCurve<T>::nodes() const {
        std::vector<std::pair<Date, Real> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i], this->data_[i]);
        return results;
    }

    #ifndef __DOXYGEN__

    // template definitions

    template <class T>
    Rate InterpolatedForwardCurve<T>::forwardImpl(Time t) const {
        if (t <= this->times_.back())
            return this->interpolation_(t, true);

        // flat fwd extrapolation
        return this->data_.back();
    }

    template <class T>
    Rate InterpolatedForwardCurve<T>::zeroYieldImpl(Time t) const {
        if (t == 0.0)
            return forwardImpl(0.0);

        Real integral;
        if (t <= this->times_.back()) {
            integral = this->interpolation_.primitive(t, true);
        } else {
            // flat fwd extrapolation
            integral = this->interpolation_.primitive(this->times_.back(), true)
                     + this->data_.back()*(t - this->times_.back());
        }
        return integral/t;
    }

    template <class T>
    InterpolatedForwardCurve<T>::InterpolatedForwardCurve(
                                    const DayCounter& dayCounter,
                                    const T& interpolator)
    : ForwardRateStructure(dayCounter), InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedForwardCurve<T>::InterpolatedForwardCurve(
                                    const Date& referenceDate,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : ForwardRateStructure(referenceDate, Calendar(), dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedForwardCurve<T>::InterpolatedForwardCurve(
                                    Natural settlementDays,
                                    const Calendar& calendar,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : ForwardRateStructure(settlementDays, calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedForwardCurve<T>::InterpolatedForwardCurve(
                                    const std::vector<Date>& dates,
                                    const std::vector<Rate>& forwards,
                                    const DayCounter& dayCounter,
                                    const Calendar& calendar,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : ForwardRateS