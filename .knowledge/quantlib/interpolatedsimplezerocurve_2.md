late <class T>
InterpolatedSimpleZeroCurve<T>::InterpolatedSimpleZeroCurve(const std::vector<Date> &dates,
                                                            const std::vector<Rate> &yields,
                                                            const DayCounter &dayCounter, const T &interpolator)
    : YieldTermStructure(dates.at(0), Calendar(), dayCounter), InterpolatedCurve<T>(std::vector<Time>(), yields,
                                                                                    interpolator),
      dates_(dates) {
    initialize();
}

#endif

template <class T> void InterpolatedSimpleZeroCurve<T>::initialize() {
    QL_REQUIRE(dates_.size() >= T::requiredPoints,
               "not enough input dates given");
    QL_REQUIRE(this->data_.size() == dates_.size(),
               "dates/data count mismatch");

    this->setupTimes(dates_, dates_[0], dayCounter());
    this->setupInterpolation();
    this->interpolation_.update();
}

} // namespace QuantLib

#endif