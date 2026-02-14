NG::make_sequence_generator(grid.size()-1,seed_);
            return ext::shared_ptr<path_generator_type>(
                         new path_generator_type(process_,
                                                 grid, gen, brownianBridge_));
        }
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
        // data members
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        Size timeSteps_, timeStepsPerYear_;
        Size requiredSamples_, maxSamples_;
        Real requiredTolerance_;
        bool isBiased_;
        bool brownianBridge_;
        BigNatural seed_;
    };


    //! Monte Carlo barrier-option engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCBarrierEngine {
      public:
        MakeMCBarrierEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);
        // named parameters
        MakeMCBarrierEngine& withSteps(Size steps);
        MakeMCBarrierEngine& withStepsPerYear(Size steps);
        MakeMCBarrierEngine& withBrownianBridge(bool b = true);
        MakeMCBarrierEngine& withAntitheticVariate(bool b = true);
        MakeMCBarrierEngine& withSamples(Size samples);
        MakeMCBarrierEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCBarrierEngine& withMaxSamples(Size samples);
        MakeMCBarrierEngine& withBias(bool b = true);
        MakeMCBarrierEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool brownianBridge_ = false, antithetic_ = false, biased_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class BarrierPathPricer : public PathPricer<Path> {
      public:
        BarrierPathPricer(Barrier::Type barrierType,
                          Real barrier,
                          Real rebate,
                          Option::Type type,
                          Real strike,
                          std::vector<DiscountFactor> discounts,
                          ext::shared_ptr<StochasticProcess1D> diffProcess,
                          PseudoRandom::ursg_type sequenceGen);
        Real operator()(const Path& path) const override;

      private:
        Barrier::Type barrierType_;
        Real barrier_;
        Real rebate_;
        ext::shared_ptr<StochasticProcess1D> diffProcess_;
        PseudoRandom::ursg_type sequenceGen_;
        PlainVanillaPayoff payoff_;
        std::vector<DiscountFactor> discounts_;
    };


    class BiasedBarrierPathPricer : public PathPricer<Path> {
      public:
        BiasedBarrierPathPricer(Barrier::Type barrierType,
                                Real barrier,
                                Real rebate,
                                Option::Type type,
                                Real strike,
                                std::vector<DiscountFactor> discounts);
        Real operator()(const Path& path) const override;

      private:
        Barrier::Type barrierType_;
        Real barrier_;
        Real rebate_;
        PlainVanillaPayoff payoff_;
        std::vector<DiscountFactor> discounts_;
    };



    // template definitions

    template <class RNG, class S>
    inline MCBarrierEngine<RNG, S>::MCBarrierEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        bool isBiased,
        BigNatural seed)
    : McSimulation<SingleVariate, RNG, S>(antitheticVariate, false), process_(std::move(process)),
      timeSteps_(timeSteps), timeStepsPerYear_(timeStepsPerYear), requiredSamples_(requiredSamples),
      maxSamples_(maxSamples), requiredTolerance_(requiredTolerance), isBiased_