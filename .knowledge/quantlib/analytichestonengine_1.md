         Gatheral,
            // old branch correction form of the characteristic function w/o control variate
            BranchCorrection,
            // Gatheral form with Andersen-Piterbarg control variate
            AndersenPiterbarg,
            // same as AndersenPiterbarg, but a slightly better control variate
            AndersenPiterbargOptCV,
            // Gatheral form with asymptotic expansion of the characteristic function as control variate
            // https://hpcquantlib.wordpress.com/2020/08/30/a-novel-control-variate-for-the-heston-model
            AsymptoticChF,
            // angled contour shift integral with control variate
            AngledContour,
            // angled contour shift integral w/o control variate
            AngledContourNoCV,
            // auto selection of best control variate algorithm from above
            OptimalCV
        };

        // Simple to use constructor: Using adaptive
        // Gauss-Lobatto integration and Gatheral's version of complex log.
        // Be aware: using a too large number for maxEvaluations might result
        // in a stack overflow as the Lobatto integration is a recursive
        // algorithm.
        AnalyticHestonEngine(const ext::shared_ptr<HestonModel>& model,
                             Real relTolerance, Size maxEvaluations);

        // Constructor using Laguerre integration
        // and Gatheral's version of complex log.
        AnalyticHestonEngine(const ext::shared_ptr<HestonModel>& model,
                             Size integrationOrder = 144);

        // Constructor giving full control
        // over the Fourier integration algorithm
        AnalyticHestonEngine(const ext::shared_ptr<HestonModel>& model,
                             ComplexLogFormula cpxLog, const Integration& itg,
                             Real andersenPiterbargEpsilon = 1e-25,
                             Real alpha = -0.5);

        void calculate() const override;

        // normalized characteristic function
        std::complex<Real> chF(const std::complex<Real>& z, Time t) const;
        std::complex<Real> lnChF(const std::complex<Real>& z, Time t) const;

        Size numberOfEvaluations() const;

        [[deprecated("Use AnalyticHestonEngine::priceVanillaPayoff instead.")]]
        static void doCalculation(Real riskFreeDiscount,
                                  Real dividendDiscount,
                                  Real spotPrice,
                                  Real strikePrice,
                                  Real term,
                                  Real kappa,
                                  Real theta,
                                  Real sigma,
                                  Real v0,
                                  Real rho,
                                  const TypePayoff& type,
                                  const Integration& integration,
                                  ComplexLogFormula cpxLog,
                                  const AnalyticHestonEngine* enginePtr,
                                  Real& value,
                                  Size& evaluations);

        Real priceVanillaPayoff(
           const ext::shared_ptr<PlainVanillaPayoff>& payoff,
           const Date& maturity) const;

        Real priceVanillaPayoff(
           const ext::shared_ptr<PlainVanillaPayoff>& payoff, Time maturity) const;

        static ComplexLogFormula optimalControlVariate(
             Time t, Real v0, Real kappa, Real theta, Real sigma, Real rho);

      protected:
        // call back for extended stochastic volatility
        // plus jump diffusion engines like bates model
        virtual std::complex<Real> addOnTerm(Real phi,
                                             Time t,
                                             Size j) const;

      private:
        class Fj_Helper;

        Real priceVanillaPayoff(
           const ext::shared_ptr<PlainVanillaPayoff>& payoff,
           Time maturity, Real fwd) c