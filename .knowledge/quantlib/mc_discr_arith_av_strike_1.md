  inline
    ext::shared_ptr<
               typename MCDiscreteArithmeticASEngine<RNG,S>::path_pricer_type>
    MCDiscreteArithmeticASEngine<RNG,S>::pathPricer() const {

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
            MCDiscreteArithmeticASEngine<RNG,S>::path_pricer_type>(
                new ArithmeticASOPathPricer(
                    payoff->optionType(),
                    process->riskFreeRate()->discount(exercise->lastDate()),
                    this->arguments_.runningAccumulator,
                    this->arguments_.pastFixings));
    }



    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCDiscreteArithmeticASEngine {
      public:
        explicit MakeMCDiscreteArithmeticASEngine(
            ext::shared_ptr<GeneralizedBlackScholesProcess> process);
        // named parameters
        MakeMCDiscreteArithmeticASEngine& withBrownianBridge(bool b = true);
        MakeMCDiscreteArithmeticASEngine& withSamples(Size samples);
        MakeMCDiscreteArithmeticASEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCDiscreteArithmeticASEngine& withMaxSamples(Size samples);
        MakeMCDiscreteArithmeticASEngine& withSeed(BigNatural seed);
        MakeMCDiscreteArithmeticASEngine& withAntitheticVariate(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool antithetic_ = false;
        Size samples_, maxSamples_;
        Real tolerance_;
        bool brownianBridge_ = true;
        BigNatural seed_ = 0;
    };

    template <class RNG, class S>
    inline MakeMCDiscreteArithmeticASEngine<RNG, S>::MakeMCDiscreteArithmeticASEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), samples_(Null<Size>()), maxSamples_(Null<Size>()),
      tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCDiscreteArithmeticASEngine<RNG,S>&
    MakeMCDiscreteArithmeticASEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDiscreteArithmeticASEngine<RNG,S>&
    MakeMCDiscreteArithmeticASEngine<RNG,S>::withAbsoluteTolerance(
                                                             Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDiscreteArithmeticASEngine<RNG,S>&
    MakeMCDiscreteArithmeticASEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDiscreteArithmeticASEngine<RNG,S>&
    MakeMCDiscreteArithmeticASEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDiscreteArithmeticASEngine<RNG,S>&
    MakeMCDiscreteArithmeticASEngine<RNG
