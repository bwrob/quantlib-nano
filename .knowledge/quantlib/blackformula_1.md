d standard deviation,
        i.e. volatility*sqrt(timeToMaturity).

        It is calculated using Brenner and Subrahmanyan (1988) and Feinstein
        (1988) approximation for at-the-money forward option, with the
        extended moneyness approximation by Corrado and Miller (1996)
    */
    Real blackFormulaImpliedStdDevApproximation(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                                Real forward,
                                                Real blackPrice,
                                                Real discount = 1.0,
                                                Real displacement = 0.0);

    /*! Approximated Black 1976 implied standard deviation,
        i.e. volatility*sqrt(timeToMaturity).

        It is calculated following "An improved approach to computing
        implied volatility", Chambers, Nawalkha, The Financial Review,
        2001, 89-100. The atm option price must be known to use this
        method.
    */
    Real blackFormulaImpliedStdDevChambers(Option::Type optionType,
                                           Real strike,
                                           Real forward,
                                           Real blackPrice,
                                           Real blackAtmPrice,
                                           Real discount = 1.0,
                                           Real displacement = 0.0);

    /*! Approximated Black 1976 implied standard deviation,
        i.e. volatility*sqrt(timeToMaturity).

        It is calculated following "An improved approach to computing
        implied volatility", Chambers, Nawalkha, The Financial Review,
        2001, 89-100. The atm option price must be known to use this
        method.
    */
    Real blackFormulaImpliedStdDevChambers(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                           Real forward,
                                           Real blackPrice,
                                           Real blackAtmPrice,
                                           Real discount = 1.0,
                                           Real displacement = 0.0);

    /*! Approximated Black 1976 implied standard deviation,
        i.e. volatility*sqrt(timeToMaturity).

        It is calculated using

        "An Explicit Implicit Volatility Formula"
        R. Radoicic, D. Stefanica,
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2908494

        "Tighter Bounds for Implied Volatility",
        J. Gatheral, I. Matic, R. Radoicic, D. Stefanica
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2922742
    */
    Real blackFormulaImpliedStdDevApproximationRS(Option::Type optionType,
                                                  Real strike,
                                                  Real forward,
                                                  Real blackPrice,
                                                  Real discount = 1.0,
                                                  Real displacement = 0.0);

    Real blackFormulaImpliedStdDevApproximationRS(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                                  Real forward,
                                                  Real blackPrice,
                                                  Real discount = 1.0,
                                                  Real displacement = 0.0);


    /*! Black 1976 implied standard deviation,
        i.e. volatility*sqrt(timeToMaturity)
    */
    Real blackFormulaImpliedStdDev(Option::Type optionType,
                                   Real strike,
                                   Real forward,
                                   Real blackPrice,
                                   Real discount = 1.0,
                                   Real displacement = 0.0,
                                   Real guess = Null<Real>(),
                                   Real accuracy = 1
