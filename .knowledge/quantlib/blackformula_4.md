ility, not
                 percentage volatility. Standard deviation is
                 absoluteVolatility*sqrt(timeToMaturity)
    */
    Real bachelierBlackFormulaForwardDerivative(
        Option::Type optionType, Real strike, Real forward, Real stdDev, Real discount = 1.0);

    /*! Bachelier Black model forward derivative.

        \warning Bachelier model needs absolute volatility, not
                 percentage volatility. Standard deviation is
                 absoluteVolatility*sqrt(timeToMaturity)
    */
    Real bachelierBlackFormulaForwardDerivative(
        const ext::shared_ptr<PlainVanillaPayoff>& payoff,
        Real forward,
        Real stdDev,
        Real discount = 1.0);

    /*! Approximated Bachelier implied volatility

        It is calculated using  the analytic implied volatility approximation
        of J. Choi, K Kim and M. Kwak (2009), “Numerical Approximation of the
        Implied Volatility Under Arithmetic Brownian Motion”,
        Applied Math. Finance, 16(3), pp. 261-268.
    */
    Real bachelierBlackFormulaImpliedVolChoi(Option::Type optionType,
                                             Real strike,
                                             Real forward,
                                             Real tte,
                                             Real bachelierPrice,
                                             Real discount = 1.0);

    /*! Exact Bachelier implied volatility

        It is calculated using the analytic implied volatility formula
        of Jaeckel (2017), "Implied Normal Volatility"
    */
    Real bachelierBlackFormulaImpliedVol(Option::Type optionType,
                                         Real strike,
                                         Real forward,
                                         Real tte,
                                         Real bachelierPrice,
                                         Real discount = 1.0);

    /*! Bachelier formula for standard deviation derivative
        \warning instead of volatility it uses standard deviation, i.e.
                 volatility*sqrt(timeToMaturity), and it returns the
                 derivative with respect to the standard deviation.
                 If T is the time to maturity Black vega would be
                 blackStdDevDerivative(strike, forward, stdDev)*sqrt(T)
    */

    Real bachelierBlackFormulaStdDevDerivative(Real strike,
                                               Real forward,
                                               Real stdDev,
                                               Real discount = 1.0);

    Real bachelierBlackFormulaStdDevDerivative(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                               Real forward,
                                               Real stdDev,
                                               Real discount = 1.0);

    /*! Bachelier formula for probability of being in the money in the asset martingale
        measure, i.e. N(d).
        It is a risk-neutral probability, not the real world one.
    */
    Real bachelierBlackFormulaAssetItmProbability(Option::Type optionType,
                                                  Real strike,
                                                  Real forward,
                                                  Real stdDev);

    /*! Bachelier formula for of being in the money in the asset martingale
        measure, i.e. N(d).
        It is a risk-neutral probability, not the real world one.
    */
    Real bachelierBlackFormulaAssetItmProbability(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                                  Real forward,
                                                  Real stdDev);

}

#endif