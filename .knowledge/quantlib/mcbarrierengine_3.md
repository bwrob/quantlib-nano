riate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withBias(bool biased) {
        biased_ = biased;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCBarrierEngine<RNG,S>&
    MakeMCBarrierEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCBarrierEngine<RNG,S>::operator ext::shared_ptr<PricingEngine>()
                                                                      const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");
        return ext::shared_ptr<PricingEngine>(new
            MCBarrierEngine<RNG,S>(process_,
                                   steps_,
                                   stepsPerYear_,
                                   brownianBridge_,
                                   antithetic_,
                                   samples_, tolerance_,
                                   maxSamples_,
                                   biased_,
                                   seed_));
    }

}


#endif
