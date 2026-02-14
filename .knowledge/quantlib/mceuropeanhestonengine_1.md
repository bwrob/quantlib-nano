requiredSamples, Real requiredTolerance,
                Size maxSamples, BigNatural seed)
    : MCVanillaEngine<MultiVariate,RNG,S>(process, timeSteps, timeStepsPerYear,
                                          false, antitheticVariate, false,
                                          requiredSamples, requiredTolerance,
                                          maxSamples, seed) {}


    template <class RNG, class S, class P>
    ext::shared_ptr<
        typename MCEuropeanHestonEngine<RNG,S,P>::path_pricer_type>
    MCEuropeanHestonEngine<RNG,S,P>::pathPricer() const {

        ext::shared_ptr<PlainVanillaPayoff> payoff(
                  ext::dynamic_pointer_cast<PlainVanillaPayoff>(
                                                    this->arguments_.payoff));
        QL_REQUIRE(payoff, "non-plain payoff given");

        ext::shared_ptr<P> process =
            ext::dynamic_pointer_cast<P>(this->process_);
        QL_REQUIRE(process, "Heston like process required");

        return ext::shared_ptr<
            typename MCEuropeanHestonEngine<RNG,S,P>::path_pricer_type>(
                   new EuropeanHestonPathPricer(
                                        payoff->optionType(),
                                        payoff->strike(),
                                        process->riskFreeRate()->discount(
                                                   this->timeGrid().back())));
    }


    template <class RNG, class S, class P>
    inline MakeMCEuropeanHestonEngine<RNG, S, P>::MakeMCEuropeanHestonEngine(
        ext::shared_ptr<P> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S,class P>
    inline MakeMCEuropeanHestonEngine<RNG,S,P>&
    MakeMCEuropeanHestonEngine<RNG,S,P>::withSteps(Size steps) {
        QL_REQUIRE(stepsPerYear_ == Null<Size>(),
                   "number of steps per year already set");
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCEuropeanHestonEngine<RNG,S,P>&
    MakeMCEuropeanHestonEngine<RNG,S,P>::withStepsPerYear(Size steps) {
        QL_REQUIRE(steps_ == Null<Size>(),
                   "number of steps already set");
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S,class P>
    inline MakeMCEuropeanHestonEngine<RNG,S,P>&
    MakeMCEuropeanHestonEngine<RNG,S,P>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCEuropeanHestonEngine<RNG,S,P>&
    MakeMCEuropeanHestonEngine<RNG,S,P>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCEuropeanHestonEngine<RNG,S,P>&
    MakeMCEuropeanHestonEngine<RNG,S,P>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCEuropeanHestonEngine<RNG,S,P>&
    MakeMCEuropeanHestonEngine<RNG,S,P>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCEuropeanHestonEngine<RNG,S,P>&
    MakeMCEuropeanHestonEngine<RNG,S,P>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S, class P>
    inline
    MakeMCEuropeanHestonEngine<RNG,S,P>::
    operator ext::shared_ptr<PricingEngine>() const {
        QL_REQUI