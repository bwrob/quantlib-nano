fTimes, "Invalid dates/times");

        std::vector<Size> timePositions(numberOfTimes);
        Array discountFactors(numberOfTimes);
        std::vector<Handle<YieldTermStructure> > forwardTermStructures(numberOfTimes);

        const Handle<YieldTermStructure> & riskFreeRate = process->riskFreeRate();

        for (Size i = 0; i < numberOfTimes; ++i) {
            timePositions[i] = theTimeGrid.index(times[i]);
            discountFactors[i] = riskFreeRate->discount(times[i]);
            forwardTermStructures[i] = Handle<YieldTermStructure>(
                ext::make_shared<ImpliedTermStructure>(riskFreeRate,
                                                         fixings[i]));
        }

        return ext::shared_ptr<
            typename MCPathBasketEngine<RNG,S>::path_pricer_type>(
                        new EuropeanPathMultiPathPricer(payoff, timePositions,
                                                        forwardTermStructures,
                                                        discountFactors));
    }


    //! Monte Carlo Path Basket engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCPathBasketEngine {
      public:
        explicit MakeMCPathBasketEngine(ext::shared_ptr<StochasticProcessArray>);
        // named parameters
        MakeMCPathBasketEngine& withSteps(Size steps);
        MakeMCPathBasketEngine& withStepsPerYear(Size steps);
        MakeMCPathBasketEngine& withBrownianBridge(bool b = true);
        MakeMCPathBasketEngine& withSamples(Size samples);
        MakeMCPathBasketEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCPathBasketEngine& withMaxSamples(Size samples);
        MakeMCPathBasketEngine& withSeed(BigNatural seed);
        MakeMCPathBasketEngine& withAntitheticVariate(bool b = true);
        MakeMCPathBasketEngine& withControlVariate(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<StochasticProcessArray> process_;
        bool antithetic_ = false, controlVariate_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        bool brownianBridge_ = false;
        BigNatural seed_ = 0;
    };

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG, S>::MakeMCPathBasketEngine(
        ext::shared_ptr<StochasticProcessArray> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPa