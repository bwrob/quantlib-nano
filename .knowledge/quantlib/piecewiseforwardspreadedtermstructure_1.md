                       std::vector<Handle<Quote>> spreads,
                                                           std::vector<Date> dates,
                                                           T factory)
    : originalCurve_(std::move(h)), spreads_(std::move(spreads)), dates_(std::move(dates)),
    times_(dates_.size()), spreadValues_(dates_.size()), factory_(std::move(factory)) {
        QL_REQUIRE(!spreads_.empty(), "no spreads given");
        QL_REQUIRE(spreads_.size() == dates_.size(),
                   "spread and date vector have different sizes");
        registerWith(originalCurve_);
        for (auto& spread : spreads_)
            registerWith(spread);
        if (!originalCurve_.empty())
            updateInterpolation();
    }

    template <class T>
    inline InterpolatedPiecewiseForwardSpreadedTermStructure<
        T>::InterpolatedPiecewiseForwardSpreadedTermStructure(Handle<YieldTermStructure> h,
                                                           std::vector<Handle<Quote>> spreads,
                                                           std::vector<Date> dates,
                                                           const DayCounter& dc,
                                                           T factory)
    : InterpolatedPiecewiseForwardSpreadedTermStructure(
        std::move(h), std::move(spreads), std::move(dates), std::move(factory)
    ) {}

    #endif

    template <class T>
    inline DayCounter InterpolatedPiecewiseForwardSpreadedTermStructure<T>::dayCounter() const {
        return originalCurve_->dayCounter();
    }

    template <class T>
    inline Calendar InterpolatedPiecewiseForwardSpreadedTermStructure<T>::calendar() const {
        return originalCurve_->calendar();
    }

    template <class T>
    inline Natural InterpolatedPiecewiseForwardSpreadedTermStructure<T>::settlementDays() const {
        return originalCurve_->settlementDays();
    }

    template <class T>
    inline const Date&
    InterpolatedPiecewiseForwardSpreadedTermStructure<T>::referenceDate() const {
        return originalCurve_->referenceDate();
    }

    template <class T>
    inline Date InterpolatedPiecewiseForwardSpreadedTermStructure<T>::maxDate() const {
        return std::min(originalCurve_->maxDate(), dates_.back());
    }

    template <class T>
    inline Rate
    InterpolatedPiecewiseForwardSpreadedTermStructure<T>::zeroYieldImpl(Time t) const {
        Spread spreadPrimitive = calcSpreadPrimitive(t);
        InterestRate zeroRate = originalCurve_->zeroRate(t, Continuous, NoFrequency, true);
        return zeroRate + spreadPrimitive;
    }

    template <class T>
    inline Rate
    InterpolatedPiecewiseForwardSpreadedTermStructure<T>::forwardImpl(Time t) const {
        Spread spread = calcSpread(t);
        Rate forwardRate = originalCurve_->forwardRate(t, t, Continuous, NoFrequency, true);
        return forwardRate + spread;
    }

    template <class T>
    inline Spread
    InterpolatedPiecewiseForwardSpreadedTermStructure<T>::calcSpread(Time t) const {
        if (t <= times_.front()) {
            return spreads_.front()->value();
        } else if (t >= times_.back()) {
            return spreads_.back()->value();
        } else {
            return interpolator_(t, true);
        }
    }

    template <class T>
    inline Spread
    InterpolatedPiecewiseForwardSpreadedTermStructure<T>::calcSpreadPrimitive(Time t) const {
        if (t == 0.0)
            return calcSpread(0.0);

        Real integral;
        if (t <= this->times_.back()) {
            integral = this->interpolator_.primitive(t, true);
        } else {
            integral = this->interpolator_.primitive(this->times_.back(), true)
                     + this->spreads_.back()->value() * (t - this->times_.back());
        }
        return integral/t;
    }

    template <class T>
    inline void InterpolatedPiecewiseForwardSpreadedTermStructure<T>::update() {
        if (!originalCurve_.empty()) {

