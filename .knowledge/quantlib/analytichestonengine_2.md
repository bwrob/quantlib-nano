onst;


        mutable Size evaluations_;
        const ComplexLogFormula cpxLog_;
        const ext::shared_ptr<Integration> integration_;
        const Real andersenPiterbargEpsilon_, alpha_;
    };


    class AnalyticHestonEngine::Integration {
      public:
        // non adaptive integration algorithms based on Gaussian quadrature
        static Integration gaussLaguerre    (Size integrationOrder = 128);
        static Integration gaussLegendre    (Size integrationOrder = 128);
        static Integration gaussChebyshev   (Size integrationOrder = 128);
        static Integration gaussChebyshev2nd(Size integrationOrder = 128);

        // Gatheral's version has to be used for an adaptive integration
        // algorithm .Be aware: using a too large number for maxEvaluations might
        // result in a stack overflow as the these integrations are based on
        // recursive algorithms.
        static Integration gaussLobatto(Real relTolerance, Real absTolerance,
                                        Size maxEvaluations = 1000,
                                        bool useConvergenceEstimate = false);

        // usually these routines have a poor convergence behavior.
        static Integration gaussKronrod(Real absTolerance,
                                        Size maxEvaluations = 1000);
        static Integration simpson(Real absTolerance,
                                   Size maxEvaluations = 1000);
        static Integration trapezoid(Real absTolerance,
                                     Size maxEvaluations = 1000);
        static Integration discreteSimpson(Size evaluation = 1000);
        static Integration discreteTrapezoid(Size evaluation = 1000);
        static Integration expSinh(Real relTolerance = 1e-8);

        static Real andersenPiterbargIntegrationLimit(
            Real c_inf, Real epsilon, Real v0, Real t);

        Real calculate(Real c_inf,
                       const std::function<Real(Real)>& f,
                       const std::function<Real()>& maxBound = {},
                       Real scaling = 1.0) const;

        Real calculate(Real c_inf,
                       const std::function<Real(Real)>& f,
                       Real maxBound) const;

        Size numberOfEvaluations() const;
        bool isAdaptiveIntegration() const;

      private:
        enum Algorithm
            { GaussLobatto, GaussKronrod, Simpson, Trapezoid,
              DiscreteTrapezoid, DiscreteSimpson,
              GaussLaguerre, GaussLegendre,
              GaussChebyshev, GaussChebyshev2nd,
              ExpSinh};

        Integration(Algorithm intAlgo, ext::shared_ptr<GaussianQuadrature> quadrature);

        Integration(Algorithm intAlgo, ext::shared_ptr<Integrator> integrator);

        const Algorithm intAlgo_;
        const ext::shared_ptr<Integrator> integrator_;
        const ext::shared_ptr<GaussianQuadrature> gaussianQuadrature_;
    };

    class AnalyticHestonEngine::AP_Helper {
      public:
        AP_Helper(Time term, Real fwd, Real strike,
                  ComplexLogFormula cpxLog,
                  const AnalyticHestonEngine* enginePtr,
                  Real alpha = -0.5);

        Real operator()(Real u) const;
        Real controlVariateValue() const;

      private:
        const Time term_;
        const Real fwd_, strike_, freq_;
        const ComplexLogFormula cpxLog_;
        const AnalyticHestonEngine* const enginePtr_;
        const Real alpha_, s_alpha_;
        Real vAvg_, tanPhi_;
        std::complex<Real> phi_, psi_;
    };


    class AnalyticHestonEngine::OptimalAlpha {
      public:
        OptimalAlpha(
            Time t,
            const AnalyticHestonEngine* enginePtr);

        Real operator()(Real strike) const;
        std::pair<Real, Real> alphaGreaterZero(Real strike) const;
        std::pair<Real, Real> alphaSmallerMinusOne(Real strike) const;

        Size numberOfEvaluations() const;
        Real M(Real k) const;
        Real k(Real x, Integer sgn) const