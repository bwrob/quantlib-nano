: GaussianQuadrature(n, GaussHermitePolynomial(mu)) {}
    };

    //! Gauss-Jacobi integration
    /*! This class performs a 1-dimensional Gauss-Jacobi integration.
        \f[
        \int_{-1}^{1} f(x) \mathrm{d}x
        \f]
        The weighting function is
        \f[
            w(x;\alpha,\beta)=(1-x)^\alpha (1+x)^\beta
        \f]
    */
    class GaussJacobiIntegration : public GaussianQuadrature {
      public:
        GaussJacobiIntegration(Size n, Real alpha, Real beta)
        : GaussianQuadrature(n, GaussJacobiPolynomial(alpha, beta)) {}
    };

    //! Gauss-Hyperbolic integration
    /*! This class performs a 1-dimensional Gauss-Hyperbolic integration.
        \f[
        \int_{-\inf}^{\inf} f(x) \mathrm{d}x
        \f]
        The weighting function is
        \f[
            w(x)=1/cosh(x)
        \f]
    */
    class GaussHyperbolicIntegration : public GaussianQuadrature {
      public:
        explicit GaussHyperbolicIntegration(Size n)
        : GaussianQuadrature(n, GaussHyperbolicPolynomial()) {}
    };

    //! Gauss-Legendre integration
    /*! This class performs a 1-dimensional Gauss-Legendre integration.
        \f[
        \int_{-1}^{1} f(x) \mathrm{d}x
        \f]
        The weighting function is
        \f[
            w(x)=1
        \f]
    */
    class GaussLegendreIntegration : public GaussianQuadrature {
      public:
        explicit GaussLegendreIntegration(Size n)
        : GaussianQuadrature(n, GaussJacobiPolynomial(0.0, 0.0)) {}
    };

    //! Gauss-Chebyshev integration
    /*! This class performs a 1-dimensional Gauss-Chebyshev integration.
        \f[
        \int_{-1}^{1} f(x) \mathrm{d}x
        \f]
        The weighting function is
        \f[
            w(x)=(1-x^2)^{-1/2}
        \f]
    */
    class GaussChebyshevIntegration : public GaussianQuadrature {
      public:
        explicit GaussChebyshevIntegration(Size n)
        : GaussianQuadrature(n, GaussJacobiPolynomial(-0.5, -0.5)) {}
    };

    //! Gauss-Chebyshev integration (second kind)
    /*! This class performs a 1-dimensional Gauss-Chebyshev integration.
        \f[
        \int_{-1}^{1} f(x) \mathrm{d}x
        \f]
        The weighting function is
        \f[
            w(x)=(1-x^2)^{1/2}
        \f]
    */
    class GaussChebyshev2ndIntegration : public GaussianQuadrature {
      public:
        explicit GaussChebyshev2ndIntegration(Size n)
      : GaussianQuadrature(n, GaussJacobiPolynomial(0.5, 0.5)) {}
    };

    //! Gauss-Gegenbauer integration
    /*! This class performs a 1-dimensional Gauss-Gegenbauer integration.
        \f[
        \int_{-1}^{1} f(x) \mathrm{d}x
        \f]
        The weighting function is
        \f[
            w(x)=(1-x^2)^{\lambda-1/2}
        \f]
    */
    class GaussGegenbauerIntegration : public GaussianQuadrature {
      public:
        GaussGegenbauerIntegration(Size n, Real lambda)
        : GaussianQuadrature(n, GaussJacobiPolynomial(lambda-0.5, lambda-0.5))
        {}
    };


    namespace detail {
        template <class Integration>
        class GaussianQuadratureIntegrator: public Integrator {
          public:
            explicit GaussianQuadratureIntegrator(Size n);

            ext::shared_ptr<Integration> getIntegration() const { return integration_; }

          private:
            Real integrate(const std::function<Real (Real)>& f,
                                           Real a,
                                           Real b) const override;

            const ext::shared_ptr<Integration> integration_;
        };
    }

    typedef detail::GaussianQuadratureIntegrator<GaussLegendreIntegration>
        GaussLegendreIntegrator;

    typedef detail::GaussianQuadratureIntegrator<GaussChebyshevIntegration>
        GaussChebyshevIntegrator;

    typedef detail::GaussianQuadratureIntegrator<GaussChebyshev2ndIntegration>
        GaussChebyshev2ndIntegrator;

    //! tabulated Gauss-Legendre quadratures
    class TabulatedGaussLegendre {
      public:

