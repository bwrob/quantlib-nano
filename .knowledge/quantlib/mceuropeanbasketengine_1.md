ural seed_;
    };


    //! Monte Carlo basket-option engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCEuropeanBasketEngine {
      public:
        MakeMCEuropeanBasketEngine(ext::shared_ptr<StochasticProcessArray>);
        // named parameters
        MakeMCEuropeanBasketEngine& withSteps(Size steps);
        MakeMCEuropeanBasketEngine& withStepsPerYear(Size steps);
        MakeMCEuropeanBasketEngine& withBrownianBridge(bool b = true);
        MakeMCEuropeanBasketEngine& withAntitheticVariate(bool b = true);
        MakeMCEuropeanBasketEngine& withSamples(Size samples);
        MakeMCEuropeanBasketEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCEuropeanBasketEngine& withMaxSamples(Size samples);
        MakeMCEuropeanBasketEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<StochasticProcessArray> process_;
        bool brownianBridge_ = false, antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class EuropeanMultiPathPricer : public PathPricer<MultiPath> {
      public:
        EuropeanMultiPathPricer(ext::shared_ptr<BasketPayoff> payoff, DiscountFactor discount);
        Real operator()(const MultiPath& multiPath) const override;

      private:
        ext::shared_ptr<BasketPayoff> payoff_;
        DiscountFactor discount_;
    };


    // template definitions

    template <class RNG, class S>
    inline MCEuropeanBasketEngine<RNG, S>::MCEuropeanBasketEngine(
        ext::shared_ptr<StochasticProcessArray> processes,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed)
    : McSimulation<MultiVariate, RNG, S>(antitheticVariate, false),
      processes_(std::move(processes)), timeSteps_(timeSteps), timeStepsPerYear_(timeStepsPerYear),
      requiredSamples_(requiredSamples), maxSamples_(maxSamples),
      requiredTolerance_(requiredTolerance), brownianBridge_(brownianBridge), seed_(seed) {
        QL_REQUIRE(timeSteps != Null<Size>() ||
                   timeStepsPerYear != Null<Size>(),
                   "no time steps provided");
        QL_REQUIRE(timeSteps == Null<Size>() ||
                   timeStepsPerYear == Null<Size>(),
                   "both time steps and time steps per year were provided");
        QL_REQUIRE(timeSteps != 0,
                   "timeSteps must be positive, " << timeSteps <<
                   " not allowed");
        QL_REQUIRE(timeStepsPerYear != 0,
                   "timeStepsPerYear must be positive, " << timeStepsPerYear <<
                   " not allowed");
        registerWith(processes_);
    }

    template <class RNG, class S>
    inline TimeGrid MCEuropeanBasketEngine<RNG,S>::timeGrid() const {

        Time residualTime = processes_->time(
                                       this->arguments_.exercise->lastDate());
        if (timeSteps_ != Null<Size>()) {
            return TimeGrid(residualTime, timeSteps_);
        } else if (timeStepsPerYear_ != Null<Size>()) {
            Size steps = static_cast<Size>(timeStepsPerYear_*residualTime);
            return TimeGrid(residualTime, std::max<Size>(steps, 1));
        } else {
            QL_FAIL("time steps not specified");
        }
    }

    template <class RNG, class S>
    inline
    ext::shared_ptr<typename MCEuropeanBasketEngine<RNG,S>::path_pricer_type>
    MCEuropeanBasketEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<BasketPayoff> payoff =
            ext::dynamic_pointer_cast<BasketPayoff>(arguments_.payoff);
        QL_REQUIRE(payoff, "non-basket payoff given");

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_c
