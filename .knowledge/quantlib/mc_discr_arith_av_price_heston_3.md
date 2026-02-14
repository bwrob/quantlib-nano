rn *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template<class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::withSteps(Size steps) {
        QL_REQUIRE(stepsPerYear_ == Null<Size>(),
                   "number of steps per year already set");
        steps_ = steps;
        return *this;
    }

    template<class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::withStepsPerYear(Size steps) {
        QL_REQUIRE(steps_ == Null<Size>(),
                   "number of steps already set");
        stepsPerYear_ = steps;
        return *this;
    }

    template<class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>&
    MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::withControlVariate(bool b) {
        controlVariate_ = b;
        return *this;
    }

    template <class RNG, class S, class P>
    inline MakeMCDiscreteArithmeticAPHestonEngine<RNG,S,P>::operator ext::shared_ptr<PricingEngine>() const {
        return ext::shared_ptr<PricingEngine>(new
            MCDiscreteArithmeticAPHestonEngine<RNG,S,P>(process_,
                                                        antithetic_,
                                                        samples_,
                                                        tolerance_,
                                                        maxSamples_,
                                                        seed_,
                                                        steps_,
                                                        stepsPerYear_,
                                                        controlVariate_));
    }
}

#endif
