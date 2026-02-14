e,
                Size maxSamples, BigNatural seed)
    : MCVanillaEngine<MultiVariate,RNG,S>(process, timeSteps, timeStepsPerYear,
                                          false, antitheticVariate, false,
                                          requiredSamples, requiredTolerance,
                                          maxSamples, seed) {}


    template <class RNG, class S>
    ext::shared_ptr<
        typename MCEuropeanGJRGARCHEngine<RNG,S>::path_pricer_type>
    MCEuropeanGJRGARCHEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<PlainVanillaPayoff> payoff(
                  ext::dynamic_pointer_cast<PlainVanillaPayoff>(
                                                    this->arguments_.payoff));
        QL_REQUIRE(payoff, "non-plain payoff given");

        ext::shared_ptr<GJRGARCHProcess> process =
            ext::dynamic_pointer_cast<GJRGARCHProcess>(this->process_);
        QL_REQUIRE(process, "GJRGARCH process required");

        return ext::shared_ptr<
            typename MCEuropeanGJRGARCHEngine<RNG,S>::path_pricer_type>(
                   new EuropeanGJRGARCHPathPricer(
                                        payoff->optionType(),
                                        payoff->strike(),
                                        process->riskFreeRate()->discount(
                                                   this->timeGrid().back())));
    }


    template <class RNG, class S>
    inline MakeMCEuropeanGJRGARCHEngine<RNG, S>::MakeMCEuropeanGJRGARCHEngine(
        ext::shared_ptr<GJRGARCHProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCEuropeanGJRGARCHEngine<RNG,S>&
    MakeMCEuropeanGJRGARCHEngine<RNG,S>::withSteps(Size steps) {
        QL_REQUIRE(stepsPerYear_ == Null<Size>(),
                   "number of steps per year already set");
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanGJRGARCHEngine<RNG,S>&
    MakeMCEuropeanGJRGARCHEngine<RNG,S>::withStepsPerYear(Size steps) {
        QL_REQUIRE(steps_ == Null<Size>(),
                   "number of steps already set");
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanGJRGARCHEngine<RNG,S>&
    MakeMCEuropeanGJRGARCHEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanGJRGARCHEngine<RNG,S>&
    MakeMCEuropeanGJRGARCHEngine<RNG,S>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanGJRGARCHEngine<RNG,S>&
    MakeMCEuropeanGJRGARCHEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanGJRGARCHEngine<RNG,S>&
    MakeMCEuropeanGJRGARCHEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanGJRGARCHEngine<RNG,S>&
    MakeMCEuropeanGJRGARCHEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCEuropeanGJRGARCHEngine<RNG,S>::
    operator ext::shared_ptr<PricingEngine>() const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "numb