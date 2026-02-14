nillaPayoff payoff_;
        DiscountFactor discount_;
        Real runningSum_;
        Size pastFixings_;
    };


    // inline definitions

    template <class RNG, class S>
    inline
    MCDiscreteArithmeticAPEngine<RNG,S>::MCDiscreteArithmeticAPEngine(
             const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
             bool brownianBridge,
             bool antitheticVariate,
             bool controlVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed)
    : MCDiscreteAveragingAsianEngineBase<SingleVariate,RNG,S>(process,
                                                              brownianBridge,
                                                              antitheticVariate,
                                                              controlVariate,
                                                              requiredSamples,
                                                              requiredTolerance,
                                                              maxSamples,
                                                              seed) {}

    template <class RNG, class S>
    inline
    ext::shared_ptr<
            typename MCDiscreteArithmeticAPEngine<RNG,S>::path_pricer_type>
        MCDiscreteArithmeticAPEngine<RNG,S>::pathPricer() const {

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
            MCDiscreteArithmeticAPEngine<RNG,S>::path_pricer_type>(
                new ArithmeticAPOPathPricer(
                    payoff->optionType(),
                    payoff->strike(),
                    process->riskFreeRate()->discount(exercise->lastDate()),
                    this->arguments_.runningAccumulator,
                    this->arguments_.pastFixings));
    }

    template <class RNG, class S>
    inline
    ext::shared_ptr<
            typename MCDiscreteArithmeticAPEngine<RNG,S>::path_pricer_type>
        MCDiscreteArithmeticAPEngine<RNG,S>::controlPathPricer() const {

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

        // for seasoned option the geometric strike might be rescaled
        // to obtain an equivalent arithmetic strike.
        // Any change applied here MUST be applied to the analytic engine too
        return ext::shared_ptr<typename
            MCDiscreteArithmeticAPEngine<RNG,S>::path_pricer_type>(
            new GeometricAPOPathPricer(
              payoff->optionType(),
              payoff->strike(),
              process->riskFreeRate()->discount(this->timeGrid().back())));
    }

    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCDiscreteArithmeticAPEngine {
      public:
        explicit MakeMCDiscreteArit