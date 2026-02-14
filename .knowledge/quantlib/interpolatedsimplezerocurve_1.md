onst {
    return this->times_;
}

template <class T> inline const std::vector<Date> &InterpolatedSimpleZeroCurve<T>::dates() const { return dates_; }

template <class T> inline const std::vector<Real> &InterpolatedSimpleZeroCurve<T>::data() const { return this->data_; }

template <class T> inline const std::vector<Rate> &InterpolatedSimpleZeroCurve<T>::zeroRates() const {
    return this->data_;
}

template <class T> inline std::vector<std::pair<Date, Real> > InterpolatedSimpleZeroCurve<T>::nodes() const {
    std::vector<std::pair<Date, Real> > results(dates_.size());
    for (Size i = 0; i < dates_.size(); ++i)
        results[i] = std::make_pair(dates_[i], this->data_[i]);
    return results;
}

#ifndef __DOXYGEN__

// template definitions

template <class T> DiscountFactor InterpolatedSimpleZeroCurve<T>::discountImpl(Time t) const {
    Rate R;
    if (t <= this->times_.back()) {
        R = this->interpolation_(t, true);
    } else {
        // flat fwd extrapolation after last pillar,
        // Notice that bbg uses flat extrapolation of non-annualized zero instead
        Time tMax = this->times_.back();
        Rate zMax = this->data_.back();
        Rate instFwdMax = zMax + tMax * this->interpolation_.derivative(tMax);
        R = (zMax * tMax + instFwdMax * (t - tMax)) / t;
    }

	return DiscountFactor(1.0 / (1.0 + R * t));    
}

template <class T>
InterpolatedSimpleZeroCurve<T>::InterpolatedSimpleZeroCurve(const DayCounter &dayCounter, const T &interpolator)
    : YieldTermStructure(dayCounter), InterpolatedCurve<T>(interpolator) {}

template <class T>
InterpolatedSimpleZeroCurve<T>::InterpolatedSimpleZeroCurve(const Date &referenceDate, const DayCounter &dayCounter,
                                                            const std::vector<Handle<Quote> > &jumps,
                                                            const std::vector<Date> &jumpDates, const T &interpolator)
    : YieldTermStructure(referenceDate, Calendar(), dayCounter, jumps, jumpDates), InterpolatedCurve<T>(interpolator) {}

template <class T>
InterpolatedSimpleZeroCurve<T>::InterpolatedSimpleZeroCurve(Natural settlementDays, const Calendar &calendar,
                                                            const DayCounter &dayCounter,
                                                            const std::vector<Handle<Quote> > &jumps,
                                                            const std::vector<Date> &jumpDates, const T &interpolator)
    : YieldTermStructure(settlementDays, calendar, dayCounter, jumps, jumpDates), InterpolatedCurve<T>(interpolator) {}

template <class T>
InterpolatedSimpleZeroCurve<T>::InterpolatedSimpleZeroCurve(const std::vector<Date> &dates,
                                                            const std::vector<Rate> &yields,
                                                            const DayCounter &dayCounter, const Calendar &calendar,
                                                            const std::vector<Handle<Quote> > &jumps,
                                                            const std::vector<Date> &jumpDates, const T &interpolator)
    : YieldTermStructure(dates.at(0), calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(std::vector<Time>(), yields, interpolator), dates_(dates) {
    initialize();
}

template <class T>
InterpolatedSimpleZeroCurve<T>::InterpolatedSimpleZeroCurve(const std::vector<Date> &dates,
                                                            const std::vector<Rate> &yields,
                                                            const DayCounter &dayCounter, const Calendar &calendar,
                                                            const T &interpolator)
    : YieldTermStructure(dates.at(0), calendar, dayCounter), InterpolatedCurve<T>(std::vector<Time>(), yields,
                                                                                  interpolator),
      dates_(dates) {
    initialize();
}

temp