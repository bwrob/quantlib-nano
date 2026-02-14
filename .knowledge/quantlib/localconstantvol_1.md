 DayCounter dayCounter)
    : LocalVolTermStructure(settlementDays, calendar),
      volatility_(ext::shared_ptr<Quote>(new SimpleQuote(volatility))),
      dayCounter_(std::move(dayCounter)) {}

    inline LocalConstantVol::LocalConstantVol(Natural settlementDays,
                                              const Calendar& calendar,
                                              Handle<Quote> volatility,
                                              DayCounter dayCounter)
    : LocalVolTermStructure(settlementDays, calendar), volatility_(std::move(volatility)),
      dayCounter_(std::move(dayCounter)) {
        registerWith(volatility_);
    }

    inline void LocalConstantVol::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<LocalConstantVol>*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            LocalVolTermStructure::accept(v);
    }

    inline Volatility LocalConstantVol::localVolImpl(Time, Real) const {
        return volatility_->value();
    }

}


#endif
