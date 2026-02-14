;
        DiscountFactor discount_;
    };


    // inline definitions

    template <class RNG, class S>
    inline
    MCEuropeanEngine<RNG,S>::MCEuropeanEngine(
             const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
             Size timeSteps,
             Size timeStepsPerYear,
             bool brownianBridge,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed)
    : MCVanillaEngine<SingleVariate,RNG,S>(process,
                                           timeSteps,
                                           timeStepsPerYear,
                                           brownianBridge,
                                           antitheticVariate,
                                           false,
                                           requiredSamples,
                                           requiredTolerance,
                                           maxSamples,
                                           seed) {}


    template <class RNG, class S>
    inline
    ext::shared_ptr<typename MCEuropeanEngine<RNG,S>::path_pricer_type>
    MCEuropeanEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<PlainVanillaPayoff> payoff =
            ext::dynamic_pointer_cast<PlainVanillaPayoff>(
                this->arguments_.payoff);
        QL_REQUIRE(payoff, "non-plain payoff given");

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                this->process_);
        QL_REQUIRE(process, "Black-Scholes process required");

        return ext::shared_ptr<
                       typename MCEuropeanEngine<RNG,S>::path_pricer_type>(
          new EuropeanPathPricer(
              payoff->optionType(),
              payoff->strike(),
              process->riskFreeRate()->discount(this->timeGrid().back())));
    }


    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG, S>::MakeMCEuropeanEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG,S>&
    MakeMCEuropeanEngine<RNG,S>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG,S>&
    MakeMCEuropeanEngine<RNG,S>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG,S>&
    MakeMCEuropeanEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG,S>&
    MakeMCEuropeanEngine<RNG,S>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG,S>&
    MakeMCEuropeanEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG,S>&
    MakeMCEuropeanEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG,S>&
    MakeMCEuropeanEngine<RNG,S>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_
