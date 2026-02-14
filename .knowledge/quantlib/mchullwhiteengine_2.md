  samples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHullWhiteCapFloorEngine<RNG,S>&
    MakeMCHullWhiteCapFloorEngine<RNG,S>::withAbsoluteTolerance(
                                                             Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHullWhiteCapFloorEngine<RNG,S>&
    MakeMCHullWhiteCapFloorEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHullWhiteCapFloorEngine<RNG,S>&
    MakeMCHullWhiteCapFloorEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHullWhiteCapFloorEngine<RNG,S>&
    MakeMCHullWhiteCapFloorEngine<RNG,S>::withBrownianBridge(bool b) {
        brownianBridge_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHullWhiteCapFloorEngine<RNG,S>&
    MakeMCHullWhiteCapFloorEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHullWhiteCapFloorEngine<RNG,S>::
    operator ext::shared_ptr<PricingEngine>() const {
        return ext::shared_ptr<PricingEngine>(new
            MCHullWhiteCapFloorEngine<RNG,S>(model_,
                                             brownianBridge_, antithetic_,
                                             samples_, tolerance_,
                                             maxSamples_, seed_));
    }

}


#endif
