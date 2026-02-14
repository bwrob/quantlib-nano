ps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : HazardRateStructure(dates.at(0), calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(std::vector<Time>(), hazardRates, interpolator),
      dates_(dates)
    {
        initialize();
    }

    template <class T>
    InterpolatedHazardRateCurve<T>::InterpolatedHazardRateCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& hazardRates,
            const DayCounter& dayCounter,
            const Calendar& calendar,
            const T& interpolator)
    : HazardRateStructure(dates.at(0), calendar, dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), hazardRates, interpolator),
      dates_(dates)
    {
        initialize();
    }

    template <class T>
    InterpolatedHazardRateCurve<T>::InterpolatedHazardRateCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& hazardRates,
            const DayCounter& dayCounter,
            const T& interpolator)
    : HazardRateStructure(dates.at(0), Calendar(), dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), hazardRates, interpolator),
      dates_(dates)
    {
        initialize();
    }

    #endif

    template <class T>
    void InterpolatedHazardRateCurve<T>::initialize()
    {
        QL_REQUIRE(dates_.size() >= T::requiredPoints,
                   "not enough input dates given");
        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "dates/data count mismatch");

        for (Size i=0; i<dates_.size(); ++i) {
            QL_REQUIRE(this->data_[i] >= 0.0, "negative hazard rate");
        }

        this->setupTimes(dates_, dates_[0], dayCounter());
        this->setupInterpolation();
        this->interpolation_.update();
    }

}

#endif