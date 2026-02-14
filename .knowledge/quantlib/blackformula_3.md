                             Real stdDev,
                                         Real displacement = 0.0);

    /*! Black 1976 formula for standard deviation derivative
        \warning instead of volatility it uses standard deviation, i.e.
                 volatility*sqrt(timeToMaturity), and it returns the
                 derivative with respect to the standard deviation.
                 If T is the time to maturity Black vega would be
                 blackStdDevDerivative(strike, forward, stdDev)*sqrt(T)
    */
    Real blackFormulaStdDevDerivative(
        Real strike, Real forward, Real stdDev, Real discount = 1.0, Real displacement = 0.0);

    /*! Black 1976 formula for  derivative with respect to implied vol, this
        is basically the vega, but if you want 1% change multiply by 1%
   */
    Real blackFormulaVolDerivative(Real strike,
                                   Real forward,
                                   Real stdDev,
                                   Real expiry,
                                   Real discount = 1.0,
                                   Real displacement = 0.0);


    /*! Black 1976 formula for standard deviation derivative
        \warning instead of volatility it uses standard deviation, i.e.
                 volatility*sqrt(timeToMaturity), and it returns the
                 derivative with respect to the standard deviation.
                 If T is the time to maturity Black vega would be
                 blackStdDevDerivative(strike, forward, stdDev)*sqrt(T)
    */
    Real blackFormulaStdDevDerivative(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                      Real forward,
                                      Real stdDev,
                                      Real discount = 1.0,
                                      Real displacement = 0.0);

    /*! Black 1976 formula for second derivative by standard deviation
        \warning instead of volatility it uses standard deviation, i.e.
                 volatility*sqrt(timeToMaturity), and it returns the
                 derivative with respect to the standard deviation.
    */
    Real blackFormulaStdDevSecondDerivative(
        Rate strike, Rate forward, Real stdDev, Real discount, Real displacement);

    /*! Black 1976 formula for second derivative by standard deviation
        \warning instead of volatility it uses standard deviation, i.e.
                 volatility*sqrt(timeToMaturity), and it returns the
                 derivative with respect to the standard deviation.
    */
    Real blackFormulaStdDevSecondDerivative(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                            Real forward,
                                            Real stdDev,
                                            Real discount = 1.0,
                                            Real displacement = 0.0);

    /*! Black style formula when forward is normal rather than
        log-normal. This is essentially the model of Bachelier.

        \warning Bachelier model needs absolute volatility, not
                 percentage volatility. Standard deviation is
                 absoluteVolatility*sqrt(timeToMaturity)
    */
    Real bachelierBlackFormula(
        Option::Type optionType, Real strike, Real forward, Real stdDev, Real discount = 1.0);

    /*! Black style formula when forward is normal rather than
        log-normal. This is essentially the model of Bachelier.

        \warning Bachelier model needs absolute volatility, not
                 percentage volatility. Standard deviation is
                 absoluteVolatility*sqrt(timeToMaturity)
    */
    Real bachelierBlackFormula(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                               Real forward,
                               Real stdDev,
                               Real discount = 1.0);

    /*! Bachelier Black model forward derivative.

        \warning Bachelier model needs absolute volat
