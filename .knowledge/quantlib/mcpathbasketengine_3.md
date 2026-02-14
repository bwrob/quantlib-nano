thBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCPathBasketEngine<RNG,S>&
    MakeMCPathBasketEngine<RNG,S>::withControlVariate(bool b) {
        controlVariate_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCPathBasketEngine<RNG,S>::operator ext::shared_ptr<PricingEngine>()
                                                                       const {
        return ext::shared_ptr<PricingEngine>(new
            MCPathBasketEngine<RNG,S>(process_,
                                      steps_,
                                      stepsPerYear_,
                                      brownianBridge_,
                                      antithetic_,
                                      controlVariate_,
                                      samples_,
                                      tolerance_,
                                      maxSamples_,
                                      seed_));
    }

}


#endif