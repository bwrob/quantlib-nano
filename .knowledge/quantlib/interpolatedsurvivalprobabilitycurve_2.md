 {}

    template <class T>
    InterpolatedSurvivalProbabilityCurve<T>::InterpolatedSurvivalProbabilityCurve(
                                    const std::vector<Date>& dates,
                                    const std::vector<Probability>& probabilities,
                                    const DayCounter& dayCounter,
                                    const Calendar& calendar,
                                    const std::vector<Handle<Quote> >& jumps,
                                    const std::vector<Date>& jumpDates,
                                    const T& interpolator)
    : SurvivalProbabilityStructure(dates.at(0), calendar, dayCounter, jumps, jumpDates),
      InterpolatedCurve<T>(std::vector<Time>(), probabilities, interpolator),
      dates_(dates)
    {
        initialize();
    }

    template <class T>
    InterpolatedSurvivalProbabilityCurve<T>::InterpolatedSurvivalProbabilityCurve(
                                    const std::vector<Date>& dates,
                                    const std::vector<Probability>& probabilities,
                                    const DayCounter& dayCounter,
                                    const Calendar& calendar,
                                    const T& interpolator)
    : SurvivalProbabilityStructure(dates.at(0), calendar, dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), probabilities, interpolator),
      dates_(dates)
    {
        initialize();
    }

    template <class T>
    InterpolatedSurvivalProbabilityCurve<T>::InterpolatedSurvivalProbabilityCurve(
                                    const std::vector<Date>& dates,
                                    const std::vector<Probability>& probabilities,
                                    const DayCounter& dayCounter,
                                    const T& interpolator)
    : SurvivalProbabilityStructure(dates.at(0), Calendar(), dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), probabilities, interpolator),
      dates_(dates)
    {
        initialize();
    }


    #endif


    template <class T>
    void InterpolatedSurvivalProbabilityCurve<T>::initialize()
    {
        QL_REQUIRE(dates_.size() >= T::requiredPoints,
                   "not enough input dates given");
        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "dates/data count mismatch");
        QL_REQUIRE(this->data_[0] == 1.0,
                   "the first probability must be == 1.0 "
                   "to flag the corresponding date as reference date");

        this->setupTimes(dates_, dates_[0], dayCounter());

        for (Size i=1; i<dates_.size(); ++i) {
            QL_REQUIRE(this->data_[i] > 0.0, "negative probability");
            QL_REQUIRE(this->data_[i] <= this->data_[i-1],
                       "negative hazard rate implied by the survival "
                       "probability " <<
                       this->data_[i] << " at " << dates_[i] <<
                       " (t=" << this->times_[i] << ") after the survival "
                       "probability " <<
                       this->data_[i-1] << " at " << dates_[i-1] <<
                       " (t=" << this->times_[i-1] << ")");
        }

        this->setupInterpolation();
        this->interpolation_.update();
    }

}

#endif