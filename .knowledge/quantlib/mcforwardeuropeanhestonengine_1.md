ne& withSamples(Size samples);
        MakeMCForwardEuropeanHestonEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCForwardEuropeanHestonEngine& withMaxSamples(Size samples);
        MakeMCForwardEuropeanHestonEngine& withSeed(BigNatural seed);
        MakeMCForwardEuropeanHestonEngine& withAntitheticVariate(bool b = true);
        MakeMCForwardEuropeanHestonEngine& withControlVariate(bool b = false);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<P> process_;
        bool antithetic_ = false, controlVariate_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class ForwardEuropeanHestonPathPricer : public PathPricer<MultiPath> {
      public:
        ForwardEuropeanHestonPathPricer(Option::Type type,
                                   Real moneyness,
                                   Size resetIndex,
                                   DiscountFactor discount);
        Real operator()(const MultiPath& multiPath) const override;

      private:
        Option::Type type_;
        Real moneyness_;
        Size resetIndex_;
        DiscountFactor discount_;
    };


    // inline definitions

    template <class RNG, class S, class P>
    inline MCForwardEuropeanHestonEngine<RNG,S,P>::MCForwardEuropeanHestonEngine(
             const ext::shared_ptr<P>& process,
             Size timeSteps,
             Size timeStepsPerYear,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed,
             bool controlVariate)
    : MCForwardVanillaEngine<MultiVariate,RNG,S>(process,
                                                 timeSteps,
                                                 timeStepsPerYear,
                                                 false,
                                                 antitheticVariate,
                                                 requiredSamples,
                                                 requiredTolerance,
                                                 maxSamples,
                                                 seed,
                                                 controlVariate) {}


    template <class RNG, class S, class P>
    inline ext::shared_ptr<typename MCForwardEuropeanHestonEngine<RNG,S,P>::path_pricer_type>
        MCForwardEuropeanHestonEngine<RNG,S,P>::pathPricer() const {

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
    inline ext::shared_ptr<typename MCForwardEuropeanHestonEngine<RNG,S,P>::path_pricer_type>
        MCForwardEuropeanHestonEngine
