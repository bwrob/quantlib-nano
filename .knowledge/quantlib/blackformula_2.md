.0e-6,
                                   Natural maxIterations = 100);

    /*! Black 1976 implied standard deviation,
        i.e. volatility*sqrt(timeToMaturity)
    */
    Real blackFormulaImpliedStdDev(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                   Real forward,
                                   Real blackPrice,
                                   Real discount = 1.0,
                                   Real displacement = 0.0,
                                   Real guess = Null<Real>(),
                                   Real accuracy = 1.0e-6,
                                   Natural maxIterations = 100);

    /*! Black 1976 implied standard deviation,
         i.e. volatility*sqrt(timeToMaturity)

        "An Adaptive Successive Over-relaxation Method for Computing the
        Black-Scholes Implied Volatility"
        M. Li, http://mpra.ub.uni-muenchen.de/6867/


        Starting point of the iteration is calculated based on

        "An Explicit Implicit Volatility Formula"
        R. Radoicic, D. Stefanica,
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2908494
    */
    Real blackFormulaImpliedStdDevLiRS(Option::Type optionType,
                                       Real strike,
                                       Real forward,
                                       Real blackPrice,
                                       Real discount = 1.0,
                                       Real displacement = 0.0,
                                       Real guess = Null<Real>(),
                                       Real omega = 1.0,
                                       Real accuracy = 1.0e-6,
                                       Natural maxIterations = 100);

    Real blackFormulaImpliedStdDevLiRS(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                       Real forward,
                                       Real blackPrice,
                                       Real discount = 1.0,
                                       Real displacement = 0.0,
                                       Real guess = Null<Real>(),
                                       Real omega = 1.0,
                                       Real accuracy = 1.0e-6,
                                       Natural maxIterations = 100);

    /*! Black 1976 probability of being in the money (in the bond martingale
        measure), i.e. N(d2).
        It is a risk-neutral probability, not the real world one.
        \warning instead of volatility it uses standard deviation,
                 i.e. volatility*sqrt(timeToMaturity)
    */
    Real blackFormulaCashItmProbability(
        Option::Type optionType, Real strike, Real forward, Real stdDev, Real displacement = 0.0);

    /*! Black 1976 probability of being in the money (in the bond martingale
        measure), i.e. N(d2).
        It is a risk-neutral probability, not the real world one.
        \warning instead of volatility it uses standard deviation,
                 i.e. volatility*sqrt(timeToMaturity)
    */
    Real blackFormulaCashItmProbability(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                        Real forward,
                                        Real stdDev,
                                        Real displacement = 0.0);

    /*! Black 1976 probability of being in the money in the asset martingale
        measure, i.e. N(d1).
        It is a risk-neutral probability, not the real world one.
    */
    Real blackFormulaAssetItmProbability(
        Option::Type optionType, Real strike, Real forward, Real stdDev, Real displacement = 0.0);

    /*! Black 1976 probability of being in the money in the asset martingale
        measure, i.e. N(d1).
        It is a risk-neutral probability, not the real world one.
    */
    Real blackFormulaAssetItmProbability(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                         Real forward,
            