 = brownianBridge;
        return *this;
    }

    template <class RNG, class S>
    inline MakeMCEuropeanEngine<RNG,S>&
    MakeMCEuropeanEngine<RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S>
    inline
    MakeMCEuropeanEngine<RNG,S>::operator ext::shared_ptr<PricingEngine>()
                                                                      const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");
        return ext::shared_ptr<PricingEngine>(new
            MCEuropeanEngine<RNG,S>(process_,
                                    steps_,
                                    stepsPerYear_,
                                    brownianBridge_,
                                    antithetic_,
                                    samples_, tolerance_,
                                    maxSamples_,
                                    seed_));
    }



    inline EuropeanPathPricer::EuropeanPathPricer(Option::Type type,
                                                  Real strike,
                                                  DiscountFactor discount)
    : payoff_(type, strike), discount_(discount) {
        QL_REQUIRE(strike>=0.0,
                   "strike less than zero not allowed");
    }

    inline Real EuropeanPathPricer::operator()(const Path& path) const {
        QL_REQUIRE(!path.empty(), "the path cannot be empty");
        return payoff_(path.back()) * discount_;
    }

}


#endif
