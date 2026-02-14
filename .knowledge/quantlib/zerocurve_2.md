cy)
    : ZeroYieldStructure(dates.at(0), calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(std::vector<Time>(), yields, interpolator),
      dates_(dates)
    {
        initialize(compounding,frequency);
    }

    template <class T>
    InterpolatedZeroCurve<T>::InterpolatedZeroCurve(
                                               const std::vector<Date>& dates,
                                               const std::vector<Rate>& yields,
                                               const DayCounter& dayCounter,
                                               const Calendar& calendar,
                                               const T& interpolator,
                                               Compounding compounding,
                                               Frequency frequency)
    : ZeroYieldStructure(dates.at(0), calendar, dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), yields, interpolator),
      dates_(dates)
    {
        initialize(compounding,frequency);
    }

    template <class T>
    InterpolatedZeroCurve<T>::InterpolatedZeroCurve(
                                               const std::vector<Date>& dates,
                                               const std::vector<Rate>& yields,
                                               const DayCounter& dayCounter,
                                               const T& interpolator,
                                               Compounding compounding,
                                               Frequency frequency)
    : ZeroYieldStructure(dates.at(0), Calendar(), dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), yields, interpolator),
      dates_(dates)
    {
        initialize(compounding,frequency);
    }

    #endif

    template <class T>
    void InterpolatedZeroCurve<T>::initialize(const Compounding& compounding, 
                                              const Frequency& frequency)
    {
        QL_REQUIRE(dates_.size() >= T::requiredPoints,
                   "not enough input dates given");
        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "dates/data count mismatch");

        this->setupTimes(dates_, dates_[0], dayCounter());

        if (compounding != Continuous) {
            // adjusting zero rates to match continuous compounding

            // The first time is 0.0, so we can't use it.
            // We fall back to about one day.
            Time dt = 1.0/365;
            InterestRate r(this->data_[0], dayCounter(), compounding, frequency);
            this->data_[0] = r.equivalentRate(Continuous, NoFrequency, dt);

            for (Size i=1; i<dates_.size(); ++i) {
                InterestRate r(this->data_[i], dayCounter(), compounding, frequency);
                this->data_[i] = r.equivalentRate(Continuous, NoFrequency, this->times_[i]);
            }
        }

        this->setupInterpolation();
        this->interpolation_.update();
    }

}

#endif