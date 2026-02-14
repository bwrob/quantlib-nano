er of steps not given");
        return ext::shared_ptr<PricingEngine>(
                 new MCEuropeanGJRGARCHEngine<RNG,S>(process_,
                                                   steps_,
                                                   stepsPerYear_,
                                                   antithetic_,
                                                   samples_, tolerance_,
                                                   maxSamples_,
                                                   seed_));
    }



    inline EuropeanGJRGARCHPathPricer::EuropeanGJRGARCHPathPricer(
                                                 Option::Type type,
                                                 Real strike,
                                                 DiscountFactor discount)
    : payoff_(type, strike), discount_(discount) {
        QL_REQUIRE(strike>=0.0,
                   "strike less than zero not allowed");
    }

    inline Real EuropeanGJRGARCHPathPricer::operator()(
                                           const MultiPath& multiPath) const {
        const Path& path = multiPath[0];
        const Size n = multiPath.pathSize();
        QL_REQUIRE(n>0, "the path cannot be empty");

        return payoff_(path.back()) * discount_;
    }

}


#endif