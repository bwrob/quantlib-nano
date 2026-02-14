ricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<P> process_;
        bool antithetic_ = false;
        Size samples_, maxSamples_, steps_, stepsPerYear_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };

    class GeometricAPOHestonPathPricer : public PathPricer<MultiPath> {
      public:
        GeometricAPOHestonPathPricer(Option::Type type,
                                     Real strike,
                                     DiscountFactor discount,
                                     std::vector<Size> fixingIndices,
                                     Real runningProduct = 1.0,
                                     Size pastFixings = 0);
        Real operator()(const MultiPath& multiPath) const override;

      private:
        PlainVanillaPayoff payoff_;
        DiscountFactor discount_;
        std::vector<Size> fixingIndices_;
        Real runningProduct_;
        Size pastFixings_;
    };


    // inline definitions

    template <class RNG, class S, class P>
    inline
    MCDiscreteGeometricAPHestonEngine<RNG,S,P>::MCDiscreteGeometricAPHestonEngine(
             const ext::shared_ptr<P>& process,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed,
             Size timeSteps,
             Size timeStepsPerYear)
    : MCDiscreteAveragingAsianEngineBase<MultiVariate,RNG,S>(process,
                                                             false,
                                                             antitheticVariate,
                                                             false,
                                                             requiredSamples,
                                                             requiredTolerance,
                                                             maxSamples,
                                                             seed,
                                                             timeSteps,
                                                             timeStepsPerYear) {
        QL_REQUIRE(timeSteps == Null<Size>() || timeStepsPerYear == Null<Size>(),
                   "both time steps and time steps per year were provided");
    }

    template <class RNG, class S, class P>
    inline ext::shared_ptr<
            typename MCDiscreteGeometricAPHestonEngine<RNG,S,P>::path_pricer_type>
        MCDiscreteGeometricAPHestonEngine<RNG,S,P>::pathPricer() const {

        // Keep track of the fixing indices, the path pricer will need to sum only these
        TimeGrid timeGrid = this->timeGrid();
        std::vector<Time> fixingTimes = timeGrid.mandatoryTimes();
        std::vector<Size> fixingIndexes;
        fixingIndexes.reserve(fixingTimes.size());
        for (Real fixingTime : fixingTimes) {
            fixingIndexes.push_back(timeGrid.closestIndex(fixingTime));
        }

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
            MCDiscreteGeometricAPHestonEngine<RNG,S,P>::path_pricer_type>(
                new GeometricAPOHestonPathPricer(
                    payoff->optionType(),
                    payoff->strike(),
                    process->riskFreeRate()->discount(exercise->lastDate()),
                    fixingIndexes,
                    this->arguments_.runningAccumulator,
                    th
