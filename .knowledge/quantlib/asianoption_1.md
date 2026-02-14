      const ext::shared_ptr<StrikedTypePayoff>& payoff,
                                     const ext::shared_ptr<Exercise>& exercise,
                                     std::vector<Real> allPastFixings = std::vector<Real>());

        void setupArguments(PricingEngine::arguments*) const override;

      protected:
        Average::Type averageType_;
        Real runningAccumulator_;
        Size pastFixings_;
        std::vector<Date> fixingDates_;

        // For backwards compatibility with the traditional interface, we keep track of
        // whether this option was initialised using the full array of seasoned fixings
        // (even if empty) or if a pastFixings and a runningAccumulator was provided
        bool allPastFixingsProvided_;
        std::vector<Real> allPastFixings_;
    };

    //! Extra %arguments for single-asset discrete-average Asian option
    class DiscreteAveragingAsianOption::arguments
        : public OneAssetOption::arguments {
      public:
        arguments() : averageType(Average::Type(-1)),
                      runningAccumulator(Null<Real>()),
                      pastFixings(Null<Size>()) {}
        void validate() const override;
        Average::Type averageType;
        Real runningAccumulator;
        Size pastFixings;
        std::vector<Date> fixingDates;
    };

    //! Extra %arguments for single-asset continuous-average Asian option
    class ContinuousAveragingAsianOption::arguments
        : public OneAssetOption::arguments {
      public:
        arguments() : averageType(Average::Type(-1))
                      {}
        void validate() const override;
        Average::Type averageType;
        Date startDate;
    };

    //! Discrete-averaging Asian %engine base class
    class DiscreteAveragingAsianOption::engine
        : public GenericEngine<DiscreteAveragingAsianOption::arguments,
                               DiscreteAveragingAsianOption::results> {};

    //! Continuous-averaging Asian %engine base class
    class ContinuousAveragingAsianOption::engine
        : public GenericEngine<ContinuousAveragingAsianOption::arguments,
                               ContinuousAveragingAsianOption::results> {};

}


#endif
