                    const DayCounter& dc)
    : BlackVolatilityTermStructure(settlementDays, cal, Following, dc),
      volatility_(ext::shared_ptr<Quote>(new SimpleQuote(volatility))) {}

    inline BlackConstantVol::BlackConstantVol(Natural settlementDays,
                                              const Calendar& cal,
                                              Handle<Quote> volatility,
                                              const DayCounter& dc)
    : BlackVolatilityTermStructure(settlementDays, cal, Following, dc),
      volatility_(std::move(volatility)) {
        registerWith(volatility_);
    }

    inline Date BlackConstantVol::maxDate() const {
        return Date::maxDate();
    }

    inline Real BlackConstantVol::minStrike() const {
        return QL_MIN_REAL;
    }

    inline Real BlackConstantVol::maxStrike() const {
        return QL_MAX_REAL;
    }

    inline void BlackConstantVol::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<BlackConstantVol>*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            BlackVolatilityTermStructure::accept(v);
    }

    inline Volatility BlackConstantVol::blackVolImpl(Time, Real) const {
        return volatility_->value();
    }

}


#endif