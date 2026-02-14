iscountCurve<T>::InterpolatedDiscountCurve(
                                 const std::vector<Date>& dates,
                                 const std::vector<DiscountFactor>& discounts,
                                 const DayCounter& dayCounter,
                                 const Calendar& calendar,
                                 const T& interpolator)
    : YieldTermStructure(dates.at(0), calendar, dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), discounts, interpolator),
      dates_(dates)
    {
        initialize();
    }

    template <class T>
    InterpolatedDiscountCurve<T>::InterpolatedDiscountCurve(
                                 const std::vector<Date>& dates,
                                 const std::vector<DiscountFactor>& discounts,
                                 const DayCounter& dayCounter,
                                 const T& interpolator)
    : YieldTermStructure(dates.at(0), Calendar(), dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), discounts, interpolator),
      dates_(dates)
    {
        initialize();
    }

    #endif

    template <class T>
    void InterpolatedDiscountCurve<T>::initialize()
    {
        QL_REQUIRE(dates_.size() >= T::requiredPoints,
                   "not enough input dates given");
        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "dates/data count mismatch");
        QL_REQUIRE(this->data_[0] == 1.0,
                   "the first discount must be == 1.0 "
                   "to flag the corresponding date as reference date");
        for (Size i=1; i<dates_.size(); ++i) {
            QL_REQUIRE(this->data_[i] > 0.0, "negative discount");
        }

        this->setupTimes(dates_, dates_[0], dayCounter());
        this->setupInterpolation();
        this->interpolation_.update();
    }

}

#endif