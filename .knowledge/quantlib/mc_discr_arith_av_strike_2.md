,S>::withBrownianBridge(bool b) {
        brownianBridge_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCDiscreteArithmeticASEngine<RNG,S>&
    MakeMCDiscreteArithmeticASEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCDiscreteArithmeticASEngine<RNG,S>::
    operator ext::shared_ptr<PricingEngine>() const {
        return ext::shared_ptr<PricingEngine>(
            new MCDiscreteArithmeticASEngine<RNG,S>(process_,
                                                    brownianBridge_,
                                                    antithetic_,
                                                    samples_, tolerance_,
                                                    maxSamples_,
                                                    seed_));
    }

}


#endif
