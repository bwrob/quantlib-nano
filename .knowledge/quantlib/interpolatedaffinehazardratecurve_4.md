 }

    template <class T>
    InterpolatedAffineHazardRateCurve<T>::InterpolatedAffineHazardRateCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& hazardRates,
        const DayCounter& dayCounter,
        const ext::shared_ptr<OneFactorAffineModel>& model,
        const Calendar& calendar,
        const T& interpolator)
    : OneFactorAffineSurvivalStructure(model, dates.at(0), calendar, dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), hazardRates, interpolator), dates_(dates) {
        initialize();
    }

    template <class T>
    InterpolatedAffineHazardRateCurve<T>::InterpolatedAffineHazardRateCurve(
        const std::vector<Date>& dates,
        const std::vector<Rate>& hazardRates,
        const DayCounter& dayCounter,
        const ext::shared_ptr<OneFactorAffineModel>& model,
        const T& interpolator)
    : OneFactorAffineSurvivalStructure(model, dates.at(0), Calendar(), dayCounter),
      InterpolatedCurve<T>(std::vector<Time>(), hazardRates, interpolator), dates_(dates) {
        initialize();
    }

    template <class T>
    void InterpolatedAffineHazardRateCurve<T>::initialize()
    {
        QL_REQUIRE(dates_.size() >= T::requiredPoints,
                   "not enough input dates given");
        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "dates/data count mismatch");

        this->setupTimes(dates_, dates_[0], dayCounter());
        this->setupInterpolation();
        this->interpolation_.update();
    }

    #endif

}

#endif