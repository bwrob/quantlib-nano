               Real initialValue1, Real initialValue2, 
                          Real accrualFactor)
        : DoubleStickyRatchetPayoff(-1.0, -1.0,
                                    gearing1, gearing2, gearing3,
                                    spread1, spread2, spread3,
                                    initialValue1, initialValue2, 
                                    accrualFactor) {}
        //! \name Payoff interface
        //@{
         std::string name() const override { return "RatchetMax"; }
         //@}
    };    

    //! RatchetMin payoff (double option)
    class RatchetMinPayoff : public DoubleStickyRatchetPayoff {
      public:
         RatchetMinPayoff(Real gearing1, Real gearing2, Real gearing3,
                          Real spread1, Real spread2, Real spread3,
                          Real initialValue1, Real initialValue2, 
                          Real accrualFactor)
        : DoubleStickyRatchetPayoff(-1.0, +1.0,
                                    gearing1, gearing2, gearing3,
                                    spread1, spread2, spread3,
                                    initialValue1, initialValue2, 
                                    accrualFactor) {}
        //! \name Payoff interface
        //@{
         std::string name() const override { return "RatchetMin"; }
         //@}
    };    

    //! StickyMax payoff (double option)
    class StickyMaxPayoff : public DoubleStickyRatchetPayoff {
      public:
         StickyMaxPayoff(Real gearing1, Real gearing2, Real gearing3,
                          Real spread1, Real spread2, Real spread3,
                          Real initialValue1, Real initialValue2, 
                          Real accrualFactor)
        : DoubleStickyRatchetPayoff(+1.0, -1.0,
                                    gearing1, gearing2, gearing3,
                                    spread1, spread2, spread3,
                                    initialValue1, initialValue2, 
                                    accrualFactor) {}
        //! \name Payoff interface
        //@{
         std::string name() const override { return "StickyMax"; }
         //@}
    };    

    //! StickyMin payoff (double option)
    class StickyMinPayoff : public DoubleStickyRatchetPayoff {
      public:
         StickyMinPayoff(Real gearing1, Real gearing2, Real gearing3,
                          Real spread1, Real spread2, Real spread3,
                          Real initialValue1, Real initialValue2, 
                          Real accrualFactor)
        : DoubleStickyRatchetPayoff(+1.0, +1.0,
                                    gearing1, gearing2, gearing3,
                                    spread1, spread2, spread3,
                                    initialValue1, initialValue2, 
                                    accrualFactor) {}
        //! \name Payoff interface
        //@{
         std::string name() const override { return "StickyMin"; }
         //@}
    };    

/*---------------------------------------------------------------------------------
    // Old code for single sticky/ratchet payoffs, 
    // superated by DoubleStickyRatchetPayoff class above

    //! Intermediate class for sticky/ratchet payoffs
    //  initialValue can be a (forward) rate or a coupon/accrualFactor 
    class StickyRatchetPayoff : public Payoff {
      public:
        StickyRatchetPayoff(Real type,
                            Real gearing1, Real gearing2,
                            Real spread1, Real spread2,
                            Real initialValue, Real accrualFactor) 
        : type_(type), gearing1_(gearing1), gearing2_(gearing2), 
          spread1_(spread1), spread2_(spread2), initialValue_(initialValue),
          accrualFactor_(accrualFactor) {}
        //! \name Payoff interface
        //@{
        Real operator()(Real forward) const;
        std::string description() const;
        virtual void accept(AcyclicVisitor&);
        //@}
      protected:
        Real type_;
        Re