);
        MakeMCPerformanceEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCPerformanceEngine& withMaxSamples(Size samples);
        MakeMCPerformanceEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool brownianBridge_ = false, antithetic_ = false;
        Size samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };



    class PerformanceOptionPathPricer : public PathPricer<Path> {
      public:
        PerformanceOptionPathPricer(Option::Type type,
                                    Real strike,
                                    std::vector<DiscountFactor> discounts);
        Real operator()(const Path& path) const override;

      private:
        Real strike_;
        Option::Type type_;
        std::vector<DiscountFactor> discounts_;
    };


    // template definitions

    template <class RNG, class S>
    inline MCPerformanceEngine<RNG, S>::MCPerformanceEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed)
    : McSimulation<SingleVariate, RNG, S>(antitheticVariate, false), process_(std::move(process)),
      requiredSamples_(requiredSamples), maxSamples_(maxSamples),
      requiredTolerance_(requiredTolerance), brownianBridge_(brownianBridge), seed_(seed) {
        registerWith(process_);
    }


    template <class RNG, class S>
    inline TimeGrid MCPerformanceEngine<RNG,S>::timeGrid() const {

        std::vector<Time> fixingTimes;
        fixingTimes.reserve(arguments_.resetDates.size());
        for (Size i=0; i<arguments_.resetDates.size(); i++)
            fixingTimes.push_back(process_->time(arguments_.resetDates[i]));
        fixingTimes.push_back(process_->time(arguments_.exercise->lastDate()));

        return TimeGrid(fixingTimes.begin(), fixingTimes.end());
    }


    template <class RNG, class S>
    inline
    ext::shared_ptr<typename MCPerformanceEngine<RNG,S>::path_pricer_type>
    MCPerformanceEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<PercentageStrikePayoff> payoff =
            ext::dynamic_pointer_cast<PercentageStrikePayoff>(
                this->arguments_.payoff);
        QL_REQUIRE(payoff, "non-percentage payoff given");

        ext::shared_ptr<EuropeanExercise> exercise =
            ext::dynamic_pointer_cast<EuropeanExercise>(
                this->arguments_.exercise);
        QL_REQUIRE(exercise, "wrong exercise given");

        std::vector<DiscountFactor> discounts;

        discounts.reserve(arguments_.resetDates.size());
        for (Size k=0;k<arguments_.resetDates.size();k++) {
            discounts.push_back(this->process_->riskFreeRate()->discount(
                                                   arguments_.resetDates[k]));
        }
        discounts.push_back(this->process_->riskFreeRate()->discount(
                                            arguments_.exercise->lastDate()));

        return ext::shared_ptr<
            typename MCPerformanceEngine<RNG,S>::path_pricer_type>(
                         new PerformanceOptionPathPricer(payoff->optionType(),
                                                         payoff->strike(),
                                                         discounts));
    }


    template <class RNG, class S>
    inline MakeMCPerformanceEngine<RNG, S>::MakeMCPerformanceEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), samples_(Null<Size>()), maxSamples_(Null<Size>()),
      tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCPerformanceEngine<RNG,S>&
    MakeMCPerformanceEngine<RNG,S>::withBrownianBridge(bool brownianBridge) {
        brown