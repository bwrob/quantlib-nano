ame Payoff interface
        //@{
        std::string name() const override { return "PercentageStrike"; }
        Real operator()(Real price) const override;
        void accept(AcyclicVisitor&) override;
        //@}
    };

    /*! Definitions of Binary path-independent payoffs used below,
        can be found in M. Rubinstein, E. Reiner:"Unscrambling The Binary Code", Risk, Vol.4 no.9,1991.
        (see: http://www.in-the-money.com/artandpap/Binary%20Options.doc)
    */

    //! Binary asset-or-nothing payoff
    class AssetOrNothingPayoff : public StrikedTypePayoff {
      public:
        AssetOrNothingPayoff(Option::Type type,
                             Real strike)
        : StrikedTypePayoff(type, strike) {}
        //! \name Payoff interface
        //@{
        std::string name() const override { return "AssetOrNothing"; }
        Real operator()(Real price) const override;
        void accept(AcyclicVisitor&) override;
        //@}
    };

    //! Binary cash-or-nothing payoff
    class CashOrNothingPayoff : public StrikedTypePayoff {
      public:
        CashOrNothingPayoff(Option::Type type,
                            Real strike,
                            Real cashPayoff)
        : StrikedTypePayoff(type, strike), cashPayoff_(cashPayoff) {}
        //! \name Payoff interface
        //@{
        std::string name() const override { return "CashOrNothing"; }
        std::string description() const override;
        Real operator()(Real price) const override;
        void accept(AcyclicVisitor&) override;
        //@}
        Real cashPayoff() const { return cashPayoff_;}
      protected:
        Real cashPayoff_;
    };

    //! Binary gap payoff
    /*! This payoff is equivalent to being a) long a PlainVanillaPayoff at
        the first strike (same Call/Put type) and b) short a
        CashOrNothingPayoff at the first strike (same Call/Put type) with
        cash payoff equal to the difference between the second and the first
        strike.
        \warning this payoff can be negative depending on the strikes
    */
    class GapPayoff : public StrikedTypePayoff {
      public:
        GapPayoff(Option::Type type,
                  Real strike,
                  Real secondStrike) // a.k.a. payoff strike
        : StrikedTypePayoff(type, strike), secondStrike_(secondStrike) {}
        //! \name Payoff interface
        //@{
        std::string name() const override { return "Gap"; }
        std::string description() const override;
        Real operator()(Real price) const override;
        void accept(AcyclicVisitor&) override;
        //@}
        Real secondStrike() const { return secondStrike_;}
      protected:
        Real secondStrike_;
    };

    //! Binary supershare and superfund payoffs

    //! Binary superfund payoff
    /*! Superfund sometimes also called "supershare", which can lead to ambiguity; within QuantLib
        the terms supershare and superfund are used consistently according to the definitions in
        Bloomberg OVX function's help pages.
    */
    /*! This payoff is equivalent to being (1/lowerstrike) a) long (short) an AssetOrNothing
        Call (Put) at the lower strike and b) short (long) an AssetOrNothing
        Call (Put) at the higher strike
    */
    class SuperFundPayoff : public StrikedTypePayoff {
      public:
        SuperFundPayoff(Real strike,
                        Real secondStrike)
        : StrikedTypePayoff(Option::Call, strike),
          secondStrike_(secondStrike) {
            QL_REQUIRE(strike>0.0,
                       "strike (" <<  strike << ") must be "
                       "positive");
            QL_REQUIRE(secondStrike>strike,
                       "second strike (" <<  secondStrike << ") must be "
                       "higher than first strike (" << strike << ")");
        }
        //! \name Payoff interface
        //@{
        std::string name() const override { return "SuperFund"; }
        Real operator()(Real price) const overri