les_ = samples;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDiscreteGeometricAPEngine<RNG,S>&
    MakeMCDiscreteGeometricAPEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDiscreteGeometricAPEngine<RNG,S>&
    MakeMCDiscreteGeometricAPEngine<RNG,S>::withBrownianBridge(bool b) {
        brownianBridge_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDiscreteGeometricAPEngine<RNG,S>&
    MakeMCDiscreteGeometricAPEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCDiscreteGeometricAPEngine<RNG,S>::operator ext::shared_ptr<PricingEngine>()
                                                                      const {
        return ext::shared_ptr<PricingEngine>(new
            MCDiscreteGeometricAPEngine<RNG,S>(process_,
                                               brownianBridge_,
                                               antithetic_,
                                               samples_, tolerance_,
                                               maxSamples_,
                                               seed_));
    }

}


#endif
