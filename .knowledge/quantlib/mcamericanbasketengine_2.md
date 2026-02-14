turn ext::make_shared<LongstaffSchwartzPathPricer<MultiPath> > (
             
                     this->timeGrid(),
                     earlyExercisePathPricer,
                     *(process->riskFreeRate()));
    }


    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>::MakeMCAmericanBasketEngine(
        ext::shared_ptr<StochasticProcessArray> process)
    : process_(std::move(process)), steps_(Null<Size>()), stepsPerYear_(Null<Size>()),
      samples_(Null<Size>()), maxSamples_(Null<Size>()), calibrationSamples_(Null<Size>()),
      tolerance_(Null<Real>()) {}

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withSteps(Size steps) {
        steps_ = steps;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withStepsPerYear(Size steps) {
        stepsPerYear_ = steps;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withBrownianBridge(bool brownianBridge) {
        brownianBridge_ = brownianBridge;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withAntitheticVariate(bool b) {
        antithetic_ = b;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withSamples(Size samples) {
        QL_REQUIRE(tolerance_ == Null<Real>(),
                   "tolerance already set");
        samples_ = samples;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withAbsoluteTolerance(Real tolerance) {
        QL_REQUIRE(samples_ == Null<Size>(),
                   "number of samples already set");
        QL_REQUIRE(RNG::allowsErrorEstimate,
                   "chosen random generator policy "
                   "does not allow an error estimate");
        tolerance_ = tolerance;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withMaxSamples(Size samples) {
        maxSamples_ = samples;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withSeed(BigNatural seed) {
        seed_ = seed;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withCalibrationSamples(Size samples) {
        calibrationSamples_ = samples;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withPolynomialOrder(Size polynomialOrder) {
        polynomialOrder_ = polynomialOrder;
        return *this;
    }

    template <class RNG>
    inline MakeMCAmericanBasketEngine<RNG>&
    MakeMCAmericanBasketEngine<RNG>::withBasisSystem(LsmBasisSystem::PolynomialType polynomialType) {
        polynomialType_ = polynomialType;
        return *this;
    }

    template <class RNG>
    inline
    MakeMCAmericanBasketEngine<RNG>::operator
    ext::shared_ptr<PricingEngine>() const {
        QL_REQUIRE(steps_ != Null<Size>() || stepsPerYear_ != Null<Size>(),
                   "number of steps not given");
        QL_REQUIRE(steps_ == Null<Size>() || stepsPerYear_ == Null<Size>(),
                   "number of steps overspecified");
        return ext::shared_ptr<PricingEngine>(new
            MCAmericanBasketEngine<RNG>(process_,
                                        steps_,
                                        stepsPerYear_,
                                        brownianBridge_,
                                        antithetic_,
                                        samples_,
                                        tolerance_,
                     