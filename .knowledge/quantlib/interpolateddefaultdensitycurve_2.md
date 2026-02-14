                 const std::vector<Real>& densities,
                                    const DayCounter& dayCounter,
                                    const Calendar& calendar,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : DefaultDensityStructure(dates.at(0), calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(std::vector<Time>(), densities, interpolator),
      dates_(dates)
    {
        initialize(dayCounter);
    }

    template <class T>
    InterpolatedDefaultDensityCurve<T>::InterpolatedDefaultDensityCurve(
            const std::vector<Date>& dates,
            const std::vector<Real>& densities,
            const DayCounter& dayCounter,
            const Calendar& calendar,
            const T& interpolator)
    : DefaultDensityStructure(dates.at(0), calendar, dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), densities, interpolator),
      dates_(dates)
    {
        initialize(dayCounter);
    }

    template <class T>
    InterpolatedDefaultDensityCurve<T>::InterpolatedDefaultDensityCurve(
            const std::vector<Date>& dates,
            const std::vector<Real>& densities,
            const DayCounter& dayCounter,
            const T& interpolator)
    : DefaultDensityStructure(dates.at(0), Calendar(), dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), densities, interpolator),
      dates_(dates)
    {
        initialize(dayCounter);
    }


    #endif


    template <class T>
    void InterpolatedDefaultDensityCurve<T>::initialize(const DayCounter& dayCounter) {
        QL_REQUIRE(dates_.size() >= T::requiredPoints,
                   "not enough input dates given");
        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "dates/data count mismatch");

        for (Size i=0; i<dates_.size(); ++i) {
            QL_REQUIRE(this->data_[i] >= 0.0, "negative default density");
        }

        this->setupTimes(dates_, dates_[0], dayCounter);
        this->setupInterpolation();
        this->interpolation_.update();
    }

}

#endif