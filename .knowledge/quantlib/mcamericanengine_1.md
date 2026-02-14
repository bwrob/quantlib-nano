ry
    template <class RNG = PseudoRandom, class S = Statistics,
              class RNG_Calibration = RNG>
    class MakeMCAmericanEngine {
      public:
        MakeMCAmericanEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);
        // named parameters
        MakeMCAmericanEngine& withSteps(Size steps);
        MakeMCAmericanEngine& withStepsPerYear(Size steps);
        MakeMCAmericanEngine& withSamples(Size samples);
        MakeMCAmericanEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCAmericanEngine& withMaxSamples(Size samples);
        MakeMCAmericanEngine& withSeed(BigNatural seed);
        MakeMCAmericanEngine& withAntitheticVariate(bool b = true);
        MakeMCAmericanEngine& withControlVariate(bool b = true);
        MakeMCAmericanEngine& withPolynomialOrder(Size polynomialOrder);
        MakeMCAmericanEngine& withBasisSystem(LsmBasisSystem::PolynomialType);
        MakeMCAmericanEngine& withCalibrationSamples(Size calibrationSamples);
        MakeMCAmericanEngine& withAntitheticVariateCalibration(bool b = true);
        MakeMCAmericanEngine& withSeedCalibration(BigNatural seed);

        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool antithetic_ = false, controlVariate_ = false;
        Size steps_, stepsPerYear_;
        Size samples_, maxSamples_, calibrationSamples_ = 2048;
        Real tolerance_;
        BigNatural seed_ = 0;
        Size polynomialOrder_ = 2;
        LsmBasisSystem::PolynomialType polynomialType_ = LsmBasisSystem::Monomial;
        ext::optional<bool> antitheticCalibration_;
        BigNatural seedCalibration_;
    };

    template <class RNG, class S, class RNG_Calibration>
    inline MCAmericanEngine<RNG, S, RNG_Calibration>::MCAmericanEngine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool antitheticVariate,
        bool controlVariate,
        Size requiredSamples,
        Real requiredTolerance,
        Size maxSamples,
        BigNatural seed,
        Size polynomialOrder,
        LsmBasisSystem::PolynomialType polynomialType,
        Size nCalibrationSamples,
        const ext::optional<bool>& antitheticVariateCalibration,
        BigNatural seedCalibration)
    : MCLongstaffSchwartzEngine<VanillaOption::engine, SingleVariate, RNG, S, RNG_Calibration>(
          process,
          timeSteps,
          timeStepsPerYear,
          false,
          antitheticVariate,
          controlVariate,
          requiredSamples,
          requiredTolerance,
          maxSamples,
          seed,
          nCalibrationSamples,
          false,
          antitheticVariateCalibration,
          seedCalibration),
      polynomialOrder_(polynomialOrder), polynomialType_(polynomialType) {}

    template <class RNG, class S, class RNG_Calibration>
    inline void MCAmericanEngine<RNG, S, RNG_Calibration>::calculate() const {
        MCLongstaffSchwartzEngine<VanillaOption::engine, SingleVariate, RNG, S,
                                  RNG_Calibration>::calculate();
        if (this->controlVariate_) {
            // control variate might lead to small negative
            // option values for deep OTM options
            this->results_.value = std::max(0.0, this->results_.value);
        }
    }

    template <class RNG, class S, class RNG_Calibration>
    inline ext::shared_ptr<LongstaffSchwartzPathPricer<Path> >
    MCAmericanEngine<RNG, S, RNG_Calibration>::lsmPathPricer() const {
        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                                                              this->process_);
        QL_REQUIRE(process, "generalized Black-Scholes process required");

        ext::shared_ptr<EarlyExercise> exercise =
            ext::dynamic_pointer_cast<Ear