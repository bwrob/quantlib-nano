>);
        // named parameters
        MakeMCDoubleBarrierEngine& withSteps(Size steps);
        MakeMCDoubleBarrierEngine& withStepsPerYear(Size steps);
        MakeMCDoubleBarrierEngine& withBrownianBridge(bool b = true);
        MakeMCDoubleBarrierEngine& withAntitheticVariate(bool b = true);
        MakeMCDoubleBarrierEngine& withSamples(Size samples);
        MakeMCDoubleBarrierEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCDoubleBarrierEngine& withMaxSamples(Size samples);
        MakeMCDoubleBarrierEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool brownianBridge_ = false, antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };

    class DoubleBarrierPathPricer : public PathPricer<Path> {
      public:
        DoubleBarrierPathPricer(DoubleBarrier::Type barrierType,
                                Real barrierLow,
                                Real barrieHigh,
                                Real rebate,
                                Option::Type type,
                                Real strike,
                                std::vector<DiscountFactor> discounts);
        Real operator()(const Path& path) const override;

      private:
        DoubleBarrier::Type barrierType_;
        Real barrierLow_;
        Real barrierHigh_;
        Real rebate_;
        PlainVanillaPayoff payoff_;
        std::vector<DiscountFactor> discounts_;
    };

    // template definitions

    template <class RNG, class S>
    inline MCDoubleBarrierEngine<RNG, S>::MCDoubleBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed)
    : McSimulation<SingleVariate, RNG, S>(antitheticVariate, false), process_(std::move(process)),
      timeSteps_(timeSteps), timeStepsPerYear_(timeStepsPerYear), requiredSamples_(requiredSamples),
      maxSamples_(maxSamples), requiredTolerance_(requiredTolerance),
      brownianBridge_(brownianBridge), seed_(seed) {
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
        registerWith(process_);
    }

    template <class RNG, class S>
    inline TimeGrid MCDoubleBarrierEngine<RNG,S>::timeGrid() const {

        Time residualTime = process_->time(arguments_.exercise->lastDate());
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
    ext::shared_ptr<typename MCDoubleBarrierEngine<RNG,S>::path_pricer_type>
    MCDoubleBarrierEngine<RNG,S>::pathPricer() const {
        ext::shared_ptr<PlainVanillaPayoff> payoff =
            ext::dynamic_pointer_cast<PlainVanillaPayoff>(arguments_.payoff);
        QL_REQUIRE(payoff, "non-plain payoff given");

        TimeGrid
