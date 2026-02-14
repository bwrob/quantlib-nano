(isBiased),
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
    inline TimeGrid MCBarrierEngine<RNG,S>::timeGrid() const {

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
    ext::shared_ptr<typename MCBarrierEngine<RNG,S>::path_pricer_type>
    MCBarrierEngine<RNG,S>::pathPricer() const {
        ext::shared_ptr<PlainVanillaPayoff> payoff =
            ext::dynamic_pointer_cast<PlainVanillaPayoff>(arguments_.payoff);
        QL_REQUIRE(payoff, "non-plain payoff given");

        TimeGrid grid = timeGrid();
        std::vector<DiscountFactor> discounts(grid.size());
        for (Size i=0; i<grid.size(); i++)
            discounts[i] = process_->riskFreeRate()->discount(grid[i]);

        // do this with template parameters?
        if (isBiased_) {
            return ext::shared_ptr<
                        typename MCBarrierEngine<RNG,S>::path_pricer_type>(
                new BiasedBarrierPathPricer(
                       arguments_.barrierType,
                       arguments_.barrier,
                       arguments_.rebate,
                       payoff->optionType(),
                       payoff->strike(),
                       discounts));
        } else {
            PseudoRandom::ursg_type sequenceGen(grid.size()-1,
                                                PseudoRandom::urng_type(5));
            return ext::shared_ptr<
                        typename MCBarrierEngine<RNG,S>::path_pricer_type>(
                new BarrierPathPricer(
                    arguments_.barrierType,
                    arguments_.barrier,
                    arguments_.rebate,
                    payoff->optionType(),
                    payoff->strike(),
                    discounts,
                    process_,
                    sequenceGen));
        }
    }


    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG, S>::MakeMCBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withAntitheticVa
