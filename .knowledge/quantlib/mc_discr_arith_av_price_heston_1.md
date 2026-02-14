MakeMCDiscreteArithmeticAPHestonEngine(ext::shared_ptr<P> process);
        // named parameters
        MakeMCDiscreteArithmeticAPHestonEngine& withSamples(Size samples);
        MakeMCDiscreteArithmeticAPHestonEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCDiscreteArithmeticAPHestonEngine& withMaxSamples(Size samples);
        MakeMCDiscreteArithmeticAPHestonEngine& withSeed(BigNatural seed);
        MakeMCDiscreteArithmeticAPHestonEngine& withAntitheticVariate(bool b = true);
        MakeMCDiscreteArithmeticAPHestonEngine& withSteps(Size steps);
        MakeMCDiscreteArithmeticAPHestonEngine& withStepsPerYear(Size steps);
        MakeMCDiscreteArithmeticAPHestonEngine& withControlVariate(bool b = false);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<P> process_;
        bool antithetic_ = false, controlVariate_ = false;
        Size samples_, maxSamples_, steps_, stepsPerYear_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class ArithmeticAPOHestonPathPricer : public PathPricer<MultiPath> {
      public:
        ArithmeticAPOHestonPathPricer(Option::Type type,
                                      Real strike,
                                      DiscountFactor discount,
                                      std::vector<Size> fixingIndices,
                                      Real runningSum = 0.0,
                                      Size pastFixings = 0);
        Real operator()(const MultiPath& multiPath) const override;

      private:
        PlainVanillaPayoff payoff_;
        DiscountFactor discount_;
        std::vector<Size> fixingIndices_;
        Real runningSum_;
        Size pastFixings_;
    };


    // inline definitions

    template <class RNG, class S, class P>
    inline
    MCDiscreteArithmeticAPHestonEngine<RNG,S,P>::MCDiscreteArithmeticAPHestonEngine(
             const ext::shared_ptr<P>& process,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed,
             Size timeSteps,
             Size timeStepsPerYear,
             bool controlVariate)
    : MCDiscreteAveragingAsianEngineBase<MultiVariate,RNG,S>(process,
                                                             false,
                                                             antitheticVariate,
                                                             controlVariate,
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
            typename MCDiscreteArithmeticAPHestonEngine<RNG,S,P>::path_pricer_type>
        MCDiscreteArithmeticAPHestonEngine<RNG,S,P>::pathPricer() const {

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
        QL_REQUIRE(payoff, "n