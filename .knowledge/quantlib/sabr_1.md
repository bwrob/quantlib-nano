eSabrParameters(Real alpha,
                                Real beta,
                                Real nu,
                                Real rho);

    //! Initial guess for SABR calibration
    /*! See Fabien Le Floc’h and Gary Kennedy, "Explicit SABR Calibration through Simple Expansions",
        available from <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2467231>.

        The returned array contains the guesses for alpha, beta, nu and rho.  The value for beta
        is the one passed in input.

        The idea is to estimate atm volatility, skew and curvature using the three volatility points
        closest around the forward (k_0 and vol_0 would be the closest strike and its volatility,
        k_m and vol_m the previous point, k_p and vol_p the following one) and solve a system for
        the SABR parameters that match them.

        \warning This functionality requires Boost 1.78 or later.  When compiled with an earlier
                 version, calling this function will raise a run-time exception.
    */
    std::array<Real, 4> sabrGuess(Real k_m, Volatility vol_m,
                                  Real k_0, Volatility vol_0,
                                  Real k_p, Volatility vol_p,
                                  Rate forward,
                                  Time expiryTime,
                                  Real beta,
                                  Real shift,
                                  VolatilityType volatilityType);


}

#endif
