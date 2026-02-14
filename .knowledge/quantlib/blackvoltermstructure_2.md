BlackVarianceTermStructure(BusinessDayConvention bdc = Following,
                                   const DayCounter& dc = DayCounter());
        //! initialize with a fixed reference date
        BlackVarianceTermStructure(const Date& referenceDate,
                                   const Calendar& cal = Calendar(),
                                   BusinessDayConvention bdc = Following,
                                   const DayCounter& dc = DayCounter());
        //! calculate the reference date based on the global evaluation date
        BlackVarianceTermStructure(Natural settlementDays,
                                   const Calendar&,
                                   BusinessDayConvention bdc = Following,
                                   const DayCounter& dc = DayCounter());
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      protected:
        /*! Returns the volatility for the given strike and date calculating it
            from the variance.
        */
        Volatility blackVolImpl(Time t, Real strike) const override;
    };



    // inline definitions

    inline Volatility BlackVolTermStructure::blackVol(const Date& d,
                                                      Real strike,
                                                      bool extrapolate) const {
        checkRange(d, extrapolate);
        checkStrike(strike, extrapolate);
        Time t = timeFromReference(d);
        return blackVolImpl(t, strike);
    }

    inline Volatility BlackVolTermStructure::blackVol(Time t,
                                                      Real strike,
                                                      bool extrapolate) const {
        checkRange(t, extrapolate);
        checkStrike(strike, extrapolate);
        return blackVolImpl(t, strike);
    }

    inline Real BlackVolTermStructure::blackVariance(const Date& d,
                                                     Real strike,
                                                     bool extrapolate) const {
        checkRange(d, extrapolate);
        checkStrike(strike, extrapolate);
        Time t = timeFromReference(d);
        return blackVarianceImpl(t, strike);
    }

    inline Real BlackVolTermStructure::blackVariance(Time t,
                                                     Real strike,
                                                     bool extrapolate) const {
        checkRange(t, extrapolate);
        checkStrike(strike, extrapolate);
        return blackVarianceImpl(t, strike);
    }

    inline void BlackVolTermStructure::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<BlackVolTermStructure>*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            QL_FAIL("not a Black-volatility term structure visitor");
    }

    inline
    Real BlackVolatilityTermStructure::blackVarianceImpl(Time t,
                                                         Real strike) const {
        Volatility vol = blackVolImpl(t, strike);
        return vol*vol*t;
    }

    inline void BlackVolatilityTermStructure::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<BlackVolatilityTermStructure>*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            BlackVolTermStructure::accept(v);
    }

    inline
    Volatility BlackVarianceTermStructure ::blackVolImpl(Time t,
                                                         Real strike) const {
        Time nonZeroMaturity = (t==0.0 ? 0.00001 : t);
        Real var = blackVarianceImpl(nonZeroMaturity, strike);
        return std::sqrt(var/nonZeroMaturity);
    }

    inline void BlackVarianceTermStructure::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<BlackVarianceTermStructure>*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            BlackVolTermStructure::accept(v);
    }

}

#endif