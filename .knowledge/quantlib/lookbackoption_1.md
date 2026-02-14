ike lookback
        call option payoff is given by the difference between the
        maximum observed price of the underlying asset during the
        lookback period and the fixed strike price. The partial-time
        fixed strike lookback put option payoff is given by the
        difference between the fixed strike price and the minimum
        observed price of the underlying asset during the lookback
        period. The partial-time fixed strike lookback option is
        cheaper than a similar standard fixed strike lookback
        option. Partial-time fixed strike lookback options can be
        priced analytically using a model introduced by Heynen and Kat
        (1994).

        \ingroup instruments
    */
    class ContinuousPartialFixedLookbackOption : public ContinuousFixedLookbackOption {
      public:
        class arguments;
        class engine;
        ContinuousPartialFixedLookbackOption(
                          Date lookbackPeriodStart,
                          const ext::shared_ptr<StrikedTypePayoff>& payoff,
                          const ext::shared_ptr<Exercise>& exercise);
        void setupArguments(PricingEngine::arguments*) const override;

      protected:
        // arguments
        Date lookbackPeriodStart_;
    };

    //! %Arguments for continuous floating lookback option calculation
    class ContinuousFloatingLookbackOption::arguments
        : public OneAssetOption::arguments {
      public:
        Real minmax;
        void validate() const override;
    };

    //! %Arguments for continuous fixed lookback option calculation
    class ContinuousFixedLookbackOption::arguments
        : public OneAssetOption::arguments {
      public:
        Real minmax;
        void validate() const override;
    };

    //! %Arguments for continuous partial floating lookback option calculation
    class ContinuousPartialFloatingLookbackOption::arguments
        : public ContinuousFloatingLookbackOption::arguments {
      public:
        Real lambda;
        Date lookbackPeriodEnd;
        void validate() const override;
    };

    //! %Arguments for continuous partial fixed lookback option calculation
    class ContinuousPartialFixedLookbackOption::arguments
        : public ContinuousFixedLookbackOption::arguments {
      public:
        Date lookbackPeriodStart;
        void validate() const override;
    };

    //! %Continuous floating lookback %engine base class
    class ContinuousFloatingLookbackOption::engine
        : public GenericEngine<ContinuousFloatingLookbackOption::arguments,
                               ContinuousFloatingLookbackOption::results> {};

    //! %Continuous fixed lookback %engine base class
    class ContinuousFixedLookbackOption::engine
        : public GenericEngine<ContinuousFixedLookbackOption::arguments,
                               ContinuousFixedLookbackOption::results> {};

    //! %Continuous partial floating lookback %engine base class
    class ContinuousPartialFloatingLookbackOption::engine
        : public GenericEngine<ContinuousPartialFloatingLookbackOption::arguments,
                               ContinuousPartialFloatingLookbackOption::results> {};

    //! %Continuous partial fixed lookback %engine base class
    class ContinuousPartialFixedLookbackOption::engine
        : public GenericEngine<ContinuousPartialFixedLookbackOption::arguments,
                               ContinuousPartialFixedLookbackOption::results> {};
}


#endif