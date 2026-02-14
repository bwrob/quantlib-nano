pe_;
        Real moneyness_;
        Size resetIndex_;
        DiscountFactor discount_;
    };


    // inline definitions

    template <class RNG, class S>
    inline
    MCForwardEuropeanBSEngine<RNG,S>::MCForwardEuropeanBSEngine(
             const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
             Size timeSteps,
             Size timeStepsPerYear,
             bool brownianBridge,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed)
    : MCForwardVanillaEngine<SingleVariate,RNG,S>(process,
                                                  timeSteps,
                                                  timeStepsPerYear,
                                                  brownianBridge,
                                                  antitheticVariate,
                                                  requiredSamples,
                                                  requiredTolerance,
                                                  maxSamples,
                                                  seed) {}


    template <class RNG, class S>
    inline
    ext::shared_ptr<typename MCForwardEuropeanBSEngine<RNG,S>::path_pricer_type>
        MCForwardEuropeanBSEngine<RNG,S>::pathPricer() const {

        TimeGrid timeGrid = this->timeGrid();

        Time resetTime = this->process_->time(this->arguments_.resetDate);
        Size resetIndex = timeGrid.closestIndex(resetTime);

        ext::shared_ptr<PlainVanillaPayoff> payoff =
            ext::dynamic_pointer_cast<PlainVanillaPayoff>(
                this->arguments_.payoff);
        QL_REQUIRE(payoff, "non-plain payoff given");

        ext::shared_ptr<EuropeanExercise> exercise =
            ext::dynamic_pointer_cast<EuropeanExercise>(
                this->arguments_.exercise);
        QL_REQUIRE(exercise, "wrong exercise given");

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                this->process_);
        QL_REQUIRE(process, "Black-Scholes process required");

        return ext::shared_ptr<typename
            MCForwardEuropeanBSEngine<RNG,S>::path_pricer_type>(
                new ForwardEuropeanBSPathPricer(
                                        payoff->optionType(),
                                        this->arguments_.moneyness,
                                        resetIndex,
                                        process->riskFreeRate()->discount(
                                                   timeGrid.back())));
    }


    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG, S>::MakeMCForwardEuropeanBSEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG,S>&
    MakeMCForwardEuropeanBSEngine<RNG,S>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG,S>&
    MakeMCForwardEuropeanBSEngine<RNG,S>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG,S>&
    MakeMCForwardEuropeanBSEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG,S>&
    MakeMCForwardEuropeanBSEngine<RNG,S>::withAbsoluteTolerance(
                                                             Real tolerance) {
        QL_REQUIRE(sam
