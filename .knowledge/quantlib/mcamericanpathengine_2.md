ze steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withControlVariate(bool b) {
        controlVariate_ = b;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanPathEngine<RNG>&
    MakeMCAmericanPathEngine<RNG>::withCalibrationSamples(Size samples) {
        calibrationSamples_ = samples;
        return *this;
    }

    template <class RNG>
    inline
    MakeMCAmericanPathEngine<RNG>::operator
    ext::shared_ptr<PricingEngine>() const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");
        return ext::shared_ptr<PricingEngine>(new
            MCAmericanPathEngine<RNG>(process_,
                                        steps_,
                                        stepsPerYear_,
                                        brownianBridge_,
                                        antithetic_,
                                        controlVariate_,
                                        samples_,
                                        tolerance_,
                                        maxSamples_,
                                        seed_,
                                        calibrationSamples_));
    }

}

#endif