tructure(dates.at(0), calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(std::vector<Time>(), forwards, interpolator),
      dates_(dates)
    {
        initialize();
    }

    template <class T>
    InterpolatedForwardCurve<T>::InterpolatedForwardCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& forwards,
            const DayCounter& dayCounter,
            const Calendar& calendar,
            const T& interpolator)
    : ForwardRateStructure(dates.at(0), calendar, dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), forwards, interpolator),
      dates_(dates)
    {
        initialize();
    }

    template <class T>
    InterpolatedForwardCurve<T>::InterpolatedForwardCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& forwards,
            const DayCounter& dayCounter,
            const T& interpolator)
    : ForwardRateStructure(dates.at(0), Calendar(), dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), forwards, interpolator),
      dates_(dates)
    {
        initialize();
    }

    #endif

    template <class T>
    void InterpolatedForwardCurve<T>::initialize()
    {
        QL_REQUIRE(dates_.size() >= T::requiredPoints,
                   "not enough input dates given");
        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "dates/data count mismatch");

        this->setupTimes(dates_, dates_[0], dayCounter());
        this->setupInterpolation();
        this->interpolation_.update();
    }

}

#endif