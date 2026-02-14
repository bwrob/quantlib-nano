s
    /*! \ingroup yieldtermstructures */

    typedef InterpolatedPiecewiseZeroSpreadedTermStructure<Linear> PiecewiseZeroSpreadedTermStructure;


    // inline definitions

    #ifndef __DOXYGEN__

    template <class T>
    inline InterpolatedPiecewiseZeroSpreadedTermStructure<
        T>::InterpolatedPiecewiseZeroSpreadedTermStructure(Handle<YieldTermStructure> h,
                                                           std::vector<Handle<Quote>> spreads,
                                                           std::vector<Date> dates,
                                                           Compounding comp,
                                                           Frequency freq,
                                                           T factory)
    : originalCurve_(std::move(h)), spreads_(std::move(spreads)), dates_(std::move(dates)),
      times_(dates_.size()), spreadValues_(dates_.size()), comp_(comp), freq_(freq),
      factory_(std::move(factory)) {
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
    inline InterpolatedPiecewiseZeroSpreadedTermStructure<
        T>::InterpolatedPiecewiseZeroSpreadedTermStructure(Handle<YieldTermStructure> h,
                                                           std::vector<Handle<Quote>> spreads,
                                                           std::vector<Date> dates,
                                                           Compounding comp,
                                                           Frequency freq,
                                                           const DayCounter& dc,
                                                           T factory)
    : InterpolatedPiecewiseZeroSpreadedTermStructure(
        std::move(h), std::move(spreads), std::move(dates), comp, freq, std::move(factory)
    ) {}

    #endif

    template <class T>
    inline DayCounter InterpolatedPiecewiseZeroSpreadedTermStructure<T>::dayCounter() const {
        return originalCurve_->dayCounter();
    }

    template <class T>
    inline Calendar InterpolatedPiecewiseZeroSpreadedTermStructure<T>::calendar() const {
        return originalCurve_->calendar();
    }

    template <class T>
    inline Natural InterpolatedPiecewiseZeroSpreadedTermStructure<T>::settlementDays() const {
        return originalCurve_->settlementDays();
    }

    template <class T>
    inline const Date&
    InterpolatedPiecewiseZeroSpreadedTermStructure<T>::referenceDate() const {
        return originalCurve_->referenceDate();
    }

    template <class T>
    inline Date InterpolatedPiecewiseZeroSpreadedTermStructure<T>::maxDate() const {
        return std::min(originalCurve_->maxDate(), dates_.back());
    }

    template <class T>
    inline Rate
    InterpolatedPiecewiseZeroSpreadedTermStructure<T>::zeroYieldImpl(Time t) const {
        Spread spread = calcSpread(t);
        InterestRate zeroRate = originalCurve_->zeroRate(t, comp_, freq_, true);
        InterestRate spreadedRate(zeroRate + spread,
                                  zeroRate.dayCounter(),
                                  zeroRate.compounding(),
                                  zeroRate.frequency());
        return spreadedRate.equivalentRate(Continuous, NoFrequency, t);
    }

    template <class T>
    inline Spread
    InterpolatedPiecewiseZeroSpreadedTermStructure<T>::calcSpread(Time t) const {
        if (t <= times_.front()) {
            return spreads_.front()->value();
        } else if (t >= times_.back()) {
            return spreads_.back()->value();
        } else {
            return interpolator_(t, true);
        }
    }

    template <class T>
    inline void Inte