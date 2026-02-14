te, dates.at(0), rates[0],
                                frequency, dayCounter, seasonality),
      InterpolatedCurve<Interpolator>(std::vector<Time>(), rates, interpolator),
      dates_(std::move(dates)) {

        QL_REQUIRE(dates_.size()>1, "too few dates: " << dates_.size());

        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "indices/dates count mismatch: "
                   << this->data_.size() << " vs " << dates_.size());

        for (Size i = 1; i < dates_.size(); i++) {
            // YoY inflation data may be positive or negative
            // but must be greater than -1
            QL_REQUIRE(this->data_[i] > -1.0,
                       "year-on-year inflation data < -100 %");
        }

        this->setupTimes(dates_, referenceDate, dayCounter);
        this->setupInterpolation();
        this->interpolation_.update();
    }

    template <class Interpolator>
    InterpolatedYoYInflationCurve<Interpolator>::
    InterpolatedYoYInflationCurve(const Date& referenceDate,
                                  Date baseDate,
                                  Rate baseYoYRate,
                                  Frequency frequency,
                                  const DayCounter& dayCounter,
                                  const ext::shared_ptr<Seasonality>& seasonality,
                                  const Interpolator& interpolator)
    : YoYInflationTermStructure(referenceDate, baseDate, baseYoYRate,
                                frequency, dayCounter, seasonality),
      InterpolatedCurve<Interpolator>(interpolator) {}


    template <class T>
    Date InterpolatedYoYInflationCurve<T>::maxDate() const {
        return dates_.back();
    }


    template <class T>
    inline Rate InterpolatedYoYInflationCurve<T>::yoyRateImpl(Time t) const {
        return this->interpolation_(t, true);
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedYoYInflationCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedYoYInflationCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Rate>&
    InterpolatedYoYInflationCurve<T>::rates() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedYoYInflationCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date,Rate> >
    InterpolatedYoYInflationCurve<T>::nodes() const {
        std::vector<std::pair<Date,Rate> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i],this->data_[i]);
        return results;
    }

}


#endif