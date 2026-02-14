bool brownianBridge_ = false, antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_, calibrationSamples_,
            polynomialOrder_ = 2;
        LsmBasisSystem::PolynomialType polynomialType_ = LsmBasisSystem::Monomial;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class AmericanBasketPathPricer
        : public EarlyExercisePathPricer<MultiPath>  {
      public:
        AmericanBasketPathPricer(
            Size assetNumber,
            ext::shared_ptr<Payoff> payoff,
            Size polynomialOrder = 2,
            LsmBasisSystem::PolynomialType polynomialType = LsmBasisSystem::Monomial);

        Array state(const MultiPath& path, Size t) const override;
        Real operator()(const MultiPath& path, Size t) const override;

        std::vector<std::function<Real(Array)> > basisSystem() const override;

      protected:
        Real payoff(const Array& state) const;

        const Size assetNumber_;
        const ext::shared_ptr<Payoff> payoff_;

        Real scalingValue_ = 1.0;
        std::vector<std::function<Real(Array)> > v_;
    };

    template <class RNG> inline
    MCAmericanBasketEngine<RNG>::MCAmericanBasketEngine(
                   const ext::shared_ptr<StochasticProcessArray>& processes,
                   Size timeSteps,
                   Size timeStepsPerYear,
                   bool brownianBridge,
                   bool antitheticVariate,
                   Size requiredSamples,
                   Real requiredTolerance,
                   Size maxSamples,
                   BigNatural seed,
                   Size nCalibrationSamples,
                   Size polynomialOrder,
                   LsmBasisSystem::PolynomialType polynomialType)
        : MCLongstaffSchwartzEngine<BasketOption::engine,
                                    MultiVariate,RNG>(processes,
                                                      timeSteps,
                                                      timeStepsPerYear,
                                                      brownianBridge,
                                                      antitheticVariate,
                                                      false,
                                                      requiredSamples,
                                                      requiredTolerance,
                                                      maxSamples,
                                                      seed,
                                                      nCalibrationSamples),
          polynomialOrder_(polynomialOrder), polynomialType_(polynomialType) {}

    template <class RNG>
    inline ext::shared_ptr<LongstaffSchwartzPathPricer<MultiPath> >
    MCAmericanBasketEngine<RNG>::lsmPathPricer() const {

        ext::shared_ptr<StochasticProcessArray> processArray =
            ext::dynamic_pointer_cast<StochasticProcessArray>(
                                                              this->process_);
        QL_REQUIRE(processArray && processArray->size()>0,
                   "Stochastic process array required");

        ext::shared_ptr<GeneralizedBlackScholesProcess> process =
            ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
               processArray->process(0));
        QL_REQUIRE(process, "generalized Black-Scholes process required");

        ext::shared_ptr<EarlyExercise> exercise =
            ext::dynamic_pointer_cast<EarlyExercise>(
                this->arguments_.exercise);
        QL_REQUIRE(exercise, "wrong exercise given");
        QL_REQUIRE(!exercise->payoffAtExpiry(),
                   "payoff at expiry not handled");

        ext::shared_ptr<AmericanBasketPathPricer> earlyExercisePathPricer(
            new AmericanBasketPathPricer(processArray->size(),
                                         this->arguments_.payoff,
                                         polynomialOrder_,
                                         polynomialType_));

        re
