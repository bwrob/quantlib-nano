;
        //@}
        mutable std::vector<Date> dates_;
      private:
        void initialize(const Compounding& compounding, const Frequency& frequency);
    };

    //! Term structure based on linear interpolation of zero yields
    /*! \ingroup yieldtermstructures */
    typedef InterpolatedZeroCurve<Linear> ZeroCurve;


    // inline definitions

    template <class T>
    inline Date InterpolatedZeroCurve<T>::maxDate() const {
        if (this->maxDate_ != Date())
           return this->maxDate_;
        return dates_.back();
    }

    template <class T>
    inline const std::vector<Time>& InterpolatedZeroCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>& InterpolatedZeroCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedZeroCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<Rate>&
    InterpolatedZeroCurve<T>::zeroRates() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date, Real> >
    InterpolatedZeroCurve<T>::nodes() const {
        std::vector<std::pair<Date, Real> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i], this->data_[i]);
        return results;
    }

    #ifndef __DOXYGEN__

    // template definitions

    template <class T>
    Rate InterpolatedZeroCurve<T>::zeroYieldImpl(Time t) const {
        if (t <= this->times_.back())
            return this->interpolation_(t, true);

        // flat fwd extrapolation
        Time tMax = this->times_.back();
        Rate zMax = this->data_.back();
        Rate instFwdMax = zMax + tMax * this->interpolation_.derivative(tMax);
        return (zMax * tMax + instFwdMax * (t-tMax)) / t;
    }

    template <class T>
    InterpolatedZeroCurve<T>::InterpolatedZeroCurve(
                                    const DayCounter& dayCounter,
                                    const T& interpolator)
    : ZeroYieldStructure(dayCounter), InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedZeroCurve<T>::InterpolatedZeroCurve(
                                    const Date& referenceDate,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : ZeroYieldStructure(referenceDate, Calendar(), dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedZeroCurve<T>::InterpolatedZeroCurve(
                                    Natural settlementDays,
                                    const Calendar& calendar,
                                    const DayCounter& dayCounter,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : ZeroYieldStructure(settlementDays, calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(interpolator) {}

    template <class T>
    InterpolatedZeroCurve<T>::InterpolatedZeroCurve(
                                    const std::vector<Date>& dates,
                                    const std::vector<Rate>& yields,
                                    const DayCounter& dayCounter,
                                    const Calendar& calendar,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator,
                                    Compounding compounding,
                                    Frequency frequen