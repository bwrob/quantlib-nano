ngroup yieldtermstructures
    */
    typedef InterpolatedDiscountCurve<LogLinear> DiscountCurve;


    // inline definitions

    template <class T>
    inline Date InterpolatedDiscountCurve<T>::maxDate() const {
        if (this->maxDate_ != Date())
            return this->maxDate_;
        return dates_.back();
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedDiscountCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedDiscountCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedDiscountCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<DiscountFactor>&
    InterpolatedDiscountCurve<T>::discounts() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date, Real> >
    InterpolatedDiscountCurve<T>::nodes() const {
        std::vector<std::pair<Date, Real> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i], this->data_[i]);
        return results;
    }

    #ifndef __DOXYGEN__

    // template definitions
    
    template <class T>
    DiscountFactor InterpolatedDiscountCurve<T>::discountImpl(Time t) const {
        if (t <= this->times_.back())
            return this->interpolation_(t, true);

        // flat fwd extrapolation
        Time tMax = this->times_.back();
        DiscountFactor dMax = this->data_.back();
        Rate instFwdMax = - this->interpolation_.derivative(tMax) / dMax;
        return dMax * std::exp(- instFwdMax * (t-tMax));
    }

    template <class T>
    InterpolatedDiscountCurve<T>::InterpolatedDiscountCurve(
                                    const DayCounter& dayCounter,
                                    const T& interpolator)
    : YieldTermStructure(dayCounter),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedDiscountCurve<T>::InterpolatedDiscountCurve(
                                    const Date& referenceDate,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : YieldTermStructure(referenceDate, Calendar(), dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedDiscountCurve<T>::InterpolatedDiscountCurve(
                                    Natural settlementDays,
                                    const Calendar& calendar,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : YieldTermStructure(settlementDays, calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedDiscountCurve<T>::InterpolatedDiscountCurve(
                                 const std::vector<Date>& dates,
                                 const std::vector<DiscountFactor>& discounts,
                                 const DayCounter& dayCounter,
                                 const Calendar& calendar,
                                 const std::vector<Handle<Quote> >& jumps,
                                 const std::vector<Date>& jumpDates,
                                 const T& interpolator)
    : YieldTermStructure(dates.at(0), calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(std::vector<Time>(), discounts, interpolator),
      dates_(dates)
    {
        initialize();
    }

    template <class T>
    InterpolatedD