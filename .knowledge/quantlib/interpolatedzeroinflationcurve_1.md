tor),
      dates_(std::move(dates)) {

        QL_REQUIRE(dates_.size() > 1, "too few dates: " << dates_.size());

        QL_REQUIRE(this->data_.size() == dates_.size(),
                   "indices/dates count mismatch: " << this->data_.size() << " vs "
                                                    << dates_.size());
        for (Size i = 1; i < dates_.size(); i++) {
            // must be greater than -1
            QL_REQUIRE(this->data_[i] > -1.0, "zero inflation data < -100 %");
        }

        this->setupTimes(dates_, referenceDate, dayCounter);
        this->setupInterpolation();
        this->interpolation_.update();
    }

    template <class Interpolator>
    InterpolatedZeroInflationCurve<Interpolator>::
    InterpolatedZeroInflationCurve(const Date& referenceDate,
                                   Date baseDate,
                                   Frequency frequency,
                                   const DayCounter& dayCounter,
                                   const ext::shared_ptr<Seasonality>& seasonality,
                                   const Interpolator& interpolator)
    :  ZeroInflationTermStructure(referenceDate, baseDate, frequency, dayCounter, seasonality),
       InterpolatedCurve<Interpolator>(interpolator) {
    }

    template <class T>
    Date InterpolatedZeroInflationCurve<T>::maxDate() const {
        return dates_.back();
    }

    template <class T>
    inline Rate InterpolatedZeroInflationCurve<T>::zeroRateImpl(Time t) const {
        return this->interpolation_(t, true);
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedZeroInflationCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedZeroInflationCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Rate>&
    InterpolatedZeroInflationCurve<T>::rates() const {
        return this->data_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedZeroInflationCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date,Rate> >
    InterpolatedZeroInflationCurve<T>::nodes() const {
        std::vector<std::pair<Date,Rate> > results(dates_.size());
        for (Size i=0; i<dates_.size(); ++i)
            results[i] = std::make_pair(dates_[i],this->data_[i]);
        return results;
    }

}


#endif