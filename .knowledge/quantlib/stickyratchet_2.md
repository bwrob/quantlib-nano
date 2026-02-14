al gearing1_, gearing2_;
        Real spread1_, spread2_;
        Real initialValue_, accrualFactor_;
    };

    //! Ratchet_2 payoff
    class RatchetPayoff_2 : public StickyRatchetPayoff {
      public:
         RatchetPayoff_2(Real gearing1, Real gearing2,
                       Real spread1, Real spread2,
                       Real initialValue, Real accrualFactor)
        : StickyRatchetPayoff(-1,
                              gearing1, gearing2,
                              spread1, spread2,
                              initialValue, accrualFactor) {}
        //! \name Payoff interface
        //@{
        std::string name() const { return "Ratchet";}
        //@}
    };

    //! Sticky_2 payoff
    class StickyPayoff_2 : public StickyRatchetPayoff {
      public:
         StickyPayoff_2(Real gearing1, Real gearing2,
                       Real spread1, Real spread2,
                       Real initialValue, Real accrualFactor) 
        : StickyRatchetPayoff(+1,
                              gearing1, gearing2,
                              spread1, spread2,
                              initialValue, accrualFactor) {}
        //! \name Payoff interface
        //@{
        std::string name() const { return "Sticky";}
        //@}
    };
-----------------------------------------------------------------------------*/

}

#endif