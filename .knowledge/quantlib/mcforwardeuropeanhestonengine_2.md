<RNG,S,P>::controlPathPricer() const {

        // Control variate prices a vanilla option on the path, and compares to analytical Heston
        // vanilla price. First entry in TimeGrid is 0, so use the existing path pricer reset at 0
        Size resetIndex = 0;
        TimeGrid timeGrid = this->timeGrid();

        ext::shared_ptr<PlainVanillaPayoff> payoff =
            ext::dynamic_pointer_cast<PlainVanillaPayoff>(
                this->arguments_.payoff);
        QL_REQUIRE(payoff, "non-plain payoff given");

        ext::shared_ptr<EuropeanExercise> exercise =
            ext::dynamic_pointer_cast<EuropeanExercise>(
                this->arguments_.exercise);
        QL_REQUIRE(exercise, "wrong exercise given");

        ext::shared_ptr<P> process =
            ext::dynamic_pointer_cast<P>(this->process_);
        QL_REQUIRE(process, "Heston like process required");

        return ext::shared_ptr<typename
            MCForwardEuropeanHestonEngine<RNG,S,P>::path_pricer_type>(
                new ForwardEuropeanHestonPathPricer(
                                        payoff->optionType(),
                                        this->arguments_.moneyness,
                                        resetIndex,
                                        process->riskFreeRate()->discount(
                                                   timeGrid.back())));
    }

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG, S, P>::MakeMCForwardEuropeanHestonEngine(
        ext::shared_ptr<P> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>&
    MakeMCForwardEuropeanHestonEngine<RNG,S,P>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>&
    MakeMCForwardEuropeanHestonEngine<RNG,S,P>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>&
    MakeMCForwardEuropeanHestonEngine<RNG,S,P>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>&
    MakeMCForwardEuropeanHestonEngine<RNG,S,P>::withAbsoluteTolerance(
                                                             Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>&
    MakeMCForwardEuropeanHestonEngine<RNG,S,P>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>&
    MakeMCForwardEuropeanHestonEngine<RNG,S,P>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>&
    MakeMCForwardEuropeanHestonEngine<RNG,S,P>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>&
    MakeMCForwardEuropeanHestonEngine<RNG,S,P>::withControlVariate(bool b) {
        controlVariate_ = b;
        return *this;
    }
