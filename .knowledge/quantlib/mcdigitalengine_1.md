(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        bool brownianBridge_ = false;
        BigNatural seed_ = 0;
    };

    class DigitalPathPricer : public PathPricer<Path> {
      public:
        DigitalPathPricer(ext::shared_ptr<CashOrNothingPayoff> payoff,
                          ext::shared_ptr<AmericanExercise> exercise,
                          Handle<YieldTermStructure> discountTS,
                          ext::shared_ptr<StochasticProcess1D> diffProcess,
                          PseudoRandom::ursg_type sequenceGen);
        Real operator()(const Path& path) const override;

      private:
        ext::shared_ptr<CashOrNothingPayoff> payoff_;
        ext::shared_ptr<AmericanExercise> exercise_;
        ext::shared_ptr<StochasticProcess1D> diffProcess_;
        PseudoRandom::ursg_type sequenceGen_;
        Handle<YieldTermStructure> discountTS_;
    };



    // template definitions

    template<class RNG, class S>
    MCDigitalEngine<RNG,S>::MCDigitalEngine(
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
    ext::shared_ptr<typename MCDigitalEngine<RNG,S>::path_pricer_type>
    MCDigitalEngine<RNG,S>::pathPricer() const {

        ext::shared_ptr<CashOrNothingPayoff> payoff =
            ext::dynamic_pointer_cast<CashOrNothingPayoff>(
                this->arguments_.payoff);
        QL_REQUIRE(payoff, "wrong payoff given");

        ext::shared_ptr<AmericanExercise> exercise =
            ext::dynamic_pointer_cast<AmericanExercise>(
                this->arguments_.exercise);
        QL_REQUIRE(exercise, "wrong exercise given");

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                                                              this->process_);
        QL_REQUIRE(process, "Black-Scholes process required");

        TimeGrid grid = this->timeGrid();
        PseudoRandom::ursg_type sequenceGen(grid.size()-1,
                                            PseudoRandom::urng_type(76));

        return ext::shared_ptr<
                        typename MCDigitalEngine<RNG,S>::path_pricer_type>(
          new DigitalPathPricer(payoff,
                                exercise,
                                process->riskFreeRate(),
                                process,
                                sequenceGen));
    }


    template <class RNG, class S>
    inline MakeMCDigitalEngine<RNG, S>::MakeMCDigitalEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCDigitalEngine<RNG,S>&
    MakeMCDigitalEngine<RNG,S>::withSteps(Si