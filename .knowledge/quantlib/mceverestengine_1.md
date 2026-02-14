class RNG = PseudoRandom, class S = Statistics>
    class MakeMCEverestEngine {
      public:
        explicit MakeMCEverestEngine(ext::shared_ptr<StochasticProcessArray>);
        // named parameters
        MakeMCEverestEngine& withSteps(Size steps);
        MakeMCEverestEngine& withStepsPerYear(Size steps);
        MakeMCEverestEngine& withBrownianBridge(bool b = true);
        MakeMCEverestEngine& withAntitheticVariate(bool b = true);
        MakeMCEverestEngine& withSamples(Size samples);
        MakeMCEverestEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCEverestEngine& withMaxSamples(Size samples);
        MakeMCEverestEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<StochasticProcessArray> process_;
        bool brownianBridge_ = false, antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class EverestMultiPathPricer : public PathPricer<MultiPath> {
      public:
        explicit EverestMultiPathPricer(Real notional,
                                        Rate guarantee,
                                        DiscountFactor discount);
        Real operator()(const MultiPath& multiPath) const override;

      private:
        Real notional_;
        Rate guarantee_;
        DiscountFactor discount_;
    };


    // template definitions

    template <class RNG, class S>
    inline MCEverestEngine<RNG, S>::MCEverestEngine(
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
    inline TimeGrid MCEverestEngine<RNG,S>::timeGrid() const {
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
    inline DiscountFactor MCEverestEngine<RNG,S>::endDiscount() const {
        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                                                      processes_->process(0));
        QL_REQUIRE(process, "Black-Scholes process required");

        return process->riskFreeRate()->discount(
                                             arguments_.exercise->lastDate());
    }

    template <clas
