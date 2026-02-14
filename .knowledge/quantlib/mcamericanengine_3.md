alibration>::withBasisSystem(LsmBasisSystem::PolynomialType polynomialType) {
        polynomialType_ = polynomialType;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withStepsPerYear(
        Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withAbsoluteTolerance(
        Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withMaxSamples(
        Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withCalibrationSamples(
        Size samples) {
        calibrationSamples_ = samples;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withAntitheticVariate(
        bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withControlVariate(bool b) {
        controlVariate_ = b;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &MakeMCAmericanEngine<
        RNG, S, RNG_Calibration>::withAntitheticVariateCalibration(bool b) {
        antitheticCalibration_ = b;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration> &
    MakeMCAmericanEngine<RNG, S, RNG_Calibration>::withSeedCalibration(
        BigNatural seed) {
        seedCalibration_ = seed;
        return *this;
    }

    template <class RNG, class S, class RNG_Calibration>
    inline MakeMCAmericanEngine<RNG, S, RNG_Calibration>::
    operator ext::shared_ptr<PricingEngine>() const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");
        return ext::shared_ptr<PricingEngine>(new
           MCAmericanEngine<RNG, S, RNG_Calibration>(process_,
                                     steps_,
                 