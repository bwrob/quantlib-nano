de;
        void accept(AcyclicVisitor&) override;
        //@}
        Real secondStrike() const { return secondStrike_;}
      protected:
        Real secondStrike_;
    };

    //! Binary supershare payoff
    class SuperSharePayoff : public StrikedTypePayoff {
      public:
        SuperSharePayoff(Real strike,
                         Real secondStrike,
                         Real cashPayoff)
        : StrikedTypePayoff(Option::Call, strike),
          secondStrike_(secondStrike),
          cashPayoff_(cashPayoff){
              QL_REQUIRE(secondStrike>strike,
              "second strike (" <<  secondStrike << ") must be "
              "higher than first strike (" << strike << ")");}

        //! \name Payoff interface
        //@{
        std::string name() const override { return "SuperShare"; }
        std::string description() const override;
        Real operator()(Real price) const override;
        void accept(AcyclicVisitor&) override;
        //@}
        Real secondStrike() const { return secondStrike_;}
        Real cashPayoff() const { return cashPayoff_;}
      protected:
        Real secondStrike_;
        Real cashPayoff_;
    };
}

#endif
