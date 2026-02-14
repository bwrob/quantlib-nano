rance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHimalayaEngine<RNG,S>&
    MakeMCHimalayaEngine<RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCHimalayaEngine<RNG,S>&
    MakeMCHimalayaEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCHimalayaEngine<RNG,S>::operator ext::shared_ptr<PricingEngine>()
                                                                      const {
        return ext::shared_ptr<PricingEngine>(new
            MCHimalayaEngine<RNG,S>(process_,
                                    brownianBridge_,
                                    antithetic_,
                                    samples_,
                                    tolerance_,
                                    maxSamples_,
                                    seed_));
    }

}

#endif
