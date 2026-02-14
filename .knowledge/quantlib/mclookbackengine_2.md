h_pricer_type>
    MCLookbackEngine<I,RNG,S>::pathPricer() const {
        TimeGrid grid = this->timeGrid();
        DiscountFactor discount = this->process_->riskFreeRate()->discount(grid.back());

        return detail::mc_lookback_path_pricer(this->arguments_,
                                               *(this->process_),
                                               discount);
    }


    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I, RNG, S>::MakeMCLookbackEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), tolerance_(Null<Real>()) {}

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>&
    MakeMCLookbackEngine<I,RNG,S>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>&
    MakeMCLookbackEngine<I,RNG,S>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>&
    MakeMCLookbackEngine<I,RNG,S>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>&
    MakeMCLookbackEngine<I,RNG,S>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>&
    MakeMCLookbackEngine<I,RNG,S>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>&
    MakeMCLookbackEngine<I,RNG,S>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>&
    MakeMCLookbackEngine<I,RNG,S>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>&
    MakeMCLookbackEngine<I,RNG,S>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class I, class RNG, class S>
    inline MakeMCLookbackEngine<I,RNG,S>::operator ext::shared_ptr<PricingEngine>() const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");

        return ext::shared_ptr<PricingEngine>(
            new MCLookbackEngine<I,RNG,S>(process_,
                                          steps_,
                                          stepsPerYear_,
                                          brownianBridge_,
                                          antithetic_,
                                          samples_,
                                          tolerance_,
                                          maxSamples_,
                                          seed_));
    }

}

#endif