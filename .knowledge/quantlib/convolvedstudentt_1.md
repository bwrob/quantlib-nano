f$ \varphi \f$ are polynomials that are computed recursively.

        The convolved characteristic function is the product of the two previous
        characteristic functions and the problem is then the convolution (a
        product) of two polynomials.

            @param n Natural number defining the order of the T for which
            the characteristic function is to be computed. The order of the
             T is then \f$ \nu=2n+1 \f$
        */
        // move outside of the class, as a separate problem?
        std::vector<Real> polynCharactT(Natural n) const;

        std::vector<Real> convolveVectorPolynomials(
            const std::vector<Real>& v1,
            const std::vector<Real>& v2) const ;
    public:
        /*! \brief Returns the cumulative probability of the resulting
        distribution.\par
            To obtain the cumulative probability the Gil-Pelaez theorem
              is applied:\par
            First compute the characteristic function of the linear combination
            variable by multiplying the individual characteristic functions.
            Then transform back integrating the characteristic function
            according to the GP theorem; this is done here analytically feeding
            in the expression of the total characteristic
            function this:
            \f[ \int_0^{\infty}x^n e^{-ax}sin(bx)dx =
                (-1)^n \Gamma(n+1) \frac{sin((n+1)arctg2(-b/a))}
                    {(\sqrt{a^2+b^2})^{n+1}}; for\,a>0,\,b>0
            \f]
            and for the first term I use:
            \f[
            \int_0^{\infty} \frac{e^{-ax}sin(bx)}{x} dx = arctg2(b/a)
            \f]
            The GP complex integration is simplified thanks to the symetry of
            the distribution.
        */
      Probability operator()(Real x) const;

      /*! \brief Returns the probability density of the resulting
      distribution.\par
          Similarly to the cumulative probability, Gil-Pelaez theorem is
          applied, the integration is similar.

          \todo Implement in a separate class? given the name of this class..
      */
      Probability density(Real x) const;

    private:
        mutable std::vector<Integer> degreesFreedom_;
        mutable std::vector<Real> factors_;

        mutable std::vector<std::vector<Real> > polynCharFnc_;
        mutable std::vector<Real> polyConvolved_;

        // cached factor in the exponential of the characteristic function
        mutable Real a_ = 0., a2_;
    };



    /*! \brief Inverse of the cumulative of the convolution of odd-T
    distributions

    Finds the inverse through a root solver. To find limits for the solver
    domain use is made of the property that the convolved distribution is
    bounded above by the normalized gaussian. If the coeffiecient in the linear
    combination add up to a number below one the T of order one can be used as
    a limit below but in general this is not necessarily the case and a constant
    is used.
    Also the fact that the combination is symmetric is used.
     */
    class InverseCumulativeBehrensFisher {
    public:
        /*!
            @param degreesFreedom Degrees of freedom of the Ts convolved. The
                algorithm is limited to odd orders only.
            @param factors Factors in the linear combination of the Ts.
            @param accuracy The accuracy of the root-solving process.
        */
        InverseCumulativeBehrensFisher(
            const std::vector<Integer>& degreesFreedom = std::vector<Integer>(),
            const std::vector<Real>& factors = std::vector<Real>(),
            Real accuracy = 1.e-6);
        //! Returns the cumulative inverse value.
        Real operator()(Probability q) const;

      private:
        mutable Real normSqr_, accuracy_;
        mutable CumulativeBehrensFisher distrib_;
    };

}

#endif