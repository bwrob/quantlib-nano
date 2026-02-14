ples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG,S>&
    MakeMCForwardEuropeanBSEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG,S>&
    MakeMCForwardEuropeanBSEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG,S>&
    MakeMCForwardEuropeanBSEngine<RNG,S>::withBrownianBridge(bool b) {
        brownianBridge_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCForwardEuropeanBSEngine<RNG,S>&
    MakeMCForwardEuropeanBSEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCForwardEuropeanBSEngine<RNG,S>::operator ext::shared_ptr<PricingEngine>()
                                                                      const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified - set EITHER steps OR stepsPerYear");
        return ext::shared_ptr<PricingEngine>(new
            MCForwardEuropeanBSEngine<RNG,S>(process_,
                                             steps_,
                                             stepsPerYear_,
                                             brownianBridge_,
                                             antithetic_,
                                             samples_, tolerance_,
                                             maxSamples_,
                                             seed_));
    }

}


#endif