

    template <class RNG, class S, class P>
    inline MakeMCForwardEuropeanHestonEngine<RNG,S,P>::operator ext::shared_ptr<PricingEngine>()
                                                                      const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified - set EITHER steps OR stepsPerYear");
        return ext::shared_ptr<PricingEngine>(new
            MCForwardEuropeanHestonEngine<RNG,S,P>(process_,
                                                   steps_,
                                                   stepsPerYear_,
                                                   antithetic_,
                                                   samples_,
                                                   tolerance_,
                                                   maxSamples_,
                                                   seed_,
                                                   controlVariate_));
    }
}


#endif
