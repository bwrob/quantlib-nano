urve_(std::move(baseCurve))
    {
        registerWith(baseCurve_);
    }

    #endif

    template <class T>
    inline DayCounter InterpolatedSpreadDiscountCurve<T>::dayCounter() const {
        return baseCurve_->dayCounter();
    }

    template <class T>
    inline Calendar InterpolatedSpreadDiscountCurve<T>::calendar() const {
        return baseCurve_->calendar();
    }

    template <class T>
    inline Natural InterpolatedSpreadDiscountCurve<T>::settlementDays() const {
        return baseCurve_->settlementDays();
    }

    template <class T>
    inline const Date& InterpolatedSpreadDiscountCurve<T>::referenceDate() const {
        return baseCurve_->referenceDate();
    }

    template <class T>
    inline Date InterpolatedSpreadDiscountCurve<T>::maxDate() const {
        Date maxDate = this->maxDate_ != Date() ? this->maxDate_ : dates_.back();
        return std::min(baseCurve_->maxDate(), maxDate);
    }

    template <class T>
    inline const Handle<YieldTermStructure>&
    InterpolatedSpreadDiscountCurve<T>::baseCurve() const {
        return baseCurve_;
    }

    template <class T>
    inline const std::vector<Time>&
    InterpolatedSpreadDiscountCurve<T>::times() const {
        return this->times_;
    }

    template <class T>
    inline const std::vector<Date>&
    InterpolatedSpreadDiscountCurve<T>::dates() const {
        return dates_;
    }

    template <class T>
    inline const std::vector<Real>&
    InterpolatedSpreadDiscountCurve<T>::data() const {
        return this->data_;
    }

    template <class T>
    inline std::vector<std::pair<Date, Real>>
    InterpolatedSpreadDiscountCurve<T>::nodes() const {
        std::vector<std::pair<Date, Real>> results(dates_.size());
        for (Size i = 0, size = dates_.size(); i < size; ++i)
            results[i] = {dates_[i], this->data_[i]};
        return results;
    }

    template <class T>
    inline DiscountFactor
    InterpolatedSpreadDiscountCurve<T>::discountImpl(Time t) const {
        return baseCurve_->discount(t) * calcSpread(t);
    }

    template <class T>
    inline DiscountFactor
    InterpolatedSpreadDiscountCurve<T>::calcSpread(Time t) const {
        if (t <= this->times_.back())
            return this->interpolation_(t, true);

        // flat fwd extrapolation
        Time tMax = this->times_.back();
        DiscountFactor dMax = this->data_.back();
        Rate instFwdMax = - this->interpolation_.derivative(tMax) / dMax;
        return dMax * std::exp(- instFwdMax * (t-tMax));
    }

    template <class T>
    inline void InterpolatedSpreadDiscountCurve<T>::update() {
        if (!baseCurve_.empty()) {
            if (!dates_.empty())
                updateInterpolation();
            YieldTermStructure::update();
        } else {
            /* The implementation inherited from YieldTermStructure
               asks for our reference date, which we don't have since
               the original curve is still not set. Therefore, we skip
               over that and just call the base-class behavior. */
            // NOLINTNEXTLINE(bugprone-parent-virtual-call)
            TermStructure::update();
        }
    }

    template <class T>
    inline void InterpolatedSpreadDiscountCurve<T>::updateInterpolation() {
        QL_REQUIRE(dates_[0] == referenceDate(),
                   "the first date should be the same as in the original curve");
        // Since dates_ are fixed and dates_[0] must be equal to referenceDate(),
        // the only thing that can change is dayCounter().
        auto dc = dayCounter();
        if (prevDayCount_ != dc) {
            this->setupTimes(dates_, dates_[0], dc);
            this->setupInterpolation();
            this->interpolation_.update();
            prevDayCount_ = dc;
        }
    }

}

#endif