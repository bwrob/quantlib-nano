grid = timeGrid();
        std::vector<DiscountFactor> discounts(grid.size());
        for (Size i=0; i<grid.size(); i++)
            discounts[i] = process_->riskFreeRate()->discount(grid[i]);

        return ext::shared_ptr<
                    typename MCDoubleBarrierEngine<RNG,S>::path_pricer_type>(
            new DoubleBarrierPathPricer(
                arguments_.barrierType,
                arguments_.barrier_lo,
                arguments_.barrier_hi,
                arguments_.rebate,
                payoff->optionType(),
                payoff->strike(),
                discounts));
        }

        template <class RNG, class S>
        inline MakeMCDoubleBarrierEngine<RNG, S>::MakeMCDoubleBarrierEngine(
            ext::shared_ptr<GeneralizedBlackScholesProcess> process)
        : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
          samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

        template <class RNG, class S>
        inline MakeMCDoubleBarrierEngine<RNG, S>&
        MakeMCDoubleBarrierEngine<RNG, S>::withSteps(Size steps) {
            steps_ = steps;
            return *this;
    }

    template <class RNG, class S>
    inline MakeMCDoubleBarrierEngine<RNG,S>&
    MakeMCDoubleBarrierEngine<RNG,S>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDoubleBarrierEngine<RNG,S>&
    MakeMCDoubleBarrierEngine<RNG,S>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDoubleBarrierEngine<RNG,S>&
    MakeMCDoubleBarrierEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDoubleBarrierEngine<RNG,S>&
    MakeMCDoubleBarrierEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDoubleBarrierEngine<RNG,S>&
    MakeMCDoubleBarrierEngine<RNG,S>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDoubleBarrierEngine<RNG,S>&
    MakeMCDoubleBarrierEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDoubleBarrierEngine<RNG,S>&
    MakeMCDoubleBarrierEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCDoubleBarrierEngine<RNG,S>::operator ext::shared_ptr<PricingEngine>()
                                                                      const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");
        return ext::shared_ptr<PricingEngine>(new
            MCDoubleBarrierEngine<RNG,S>(process_,
                                   steps_,
                                   stepsPerYear_,
                                   brownianBridge_,
                                   antithetic_,
                                   samples_,
                                   tolerance_,
                                   maxSamples_,
                                   seed_));
    }

}


#endif