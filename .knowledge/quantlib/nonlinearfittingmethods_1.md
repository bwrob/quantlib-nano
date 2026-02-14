 for US Treasury bills." NBER Working Paper Series, no 1594.
    */
    class NelsonSiegelFitting
        : public FittedBondDiscountCurve::FittingMethod {
      public:
        NelsonSiegelFitting(const Array& weights = Array(),
                            const ext::shared_ptr<OptimizationMethod>& optimizationMethod = {},
                            const Array& l2 = Array(),
                            Real minCutoffTime = 0.0,
                            Real maxCutoffTime = QL_MAX_REAL,
                            Constraint constraint = NoConstraint());
        NelsonSiegelFitting(const Array& weights,
                            const Array& l2,
                            Real minCutoffTime = 0.0,
                            Real maxCutoffTime = QL_MAX_REAL,
                            Constraint constraint = NoConstraint());
        std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const override;
      private:
        Size size() const override;
        DiscountFactor discountFunction(const Array& x, Time t) const override;
    };


    //! Svensson Fitting method
    /*! Fits a discount function to the form
        \f$ d(t) = e^{-r t}, \f$ where the zero rate \f$r\f$ is defined as
        \f[
        r \equiv c_0 + (c_1 + c_2) \left( \frac {1 - e^{-\kappa t}}{\kappa t} \right)
        - c_2 e^{ - \kappa t}
        + c_3 \left( \frac{1 - e^{-\kappa_1 t}}{\kappa_1 t} -e^{-\kappa_1 t} \right).
        \f]
        See: Svensson, L. (1994). Estimating and interpreting forward
        interest rates: Sweden 1992-4.
        Discussion paper, Centre for Economic Policy Research(1051).
    */
    class SvenssonFitting
        : public FittedBondDiscountCurve::FittingMethod {
      public:
        SvenssonFitting(const Array& weights = Array(),
                        const ext::shared_ptr<OptimizationMethod>& optimizationMethod = {},
                        const Array& l2 = Array(),
                        Real minCutoffTime = 0.0,
                        Real maxCutoffTime = QL_MAX_REAL,
                        Constraint constraint = NoConstraint());
        SvenssonFitting(const Array& weights,
                        const Array& l2,
                        Real minCutoffTime = 0.0,
                        Real maxCutoffTime = QL_MAX_REAL,
                        Constraint constraint = NoConstraint());
        std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const override;
      private:
        Size size() const override;
        DiscountFactor discountFunction(const Array& x, Time t) const override;
    };


    //! CubicSpline B-splines fitting method
    /*! Fits a discount function to a set of cubic B-splines
        \f$ N_{i,3}(t) \f$, i.e.,
        \f[
        d(t) = \sum_{i=0}^{n}  c_i \times N_{i,3}(t)
        \f]

        See: McCulloch, J. 1971, "Measuring the Term Structure of
        Interest Rates." Journal of Business, 44: 19-31

        McCulloch, J. 1975, "The tax adjusted yield curve."
        Journal of Finance, XXX811-30

        \warning "The results are extremely sensitive to the number
                  and location of the knot points, and there is no
                  optimal way of selecting them." James, J. and
                  N. Webber, "Interest Rate Modelling" John Wiley,
                  2000, pp. 440.
    */
    class CubicBSplinesFitting
        : public FittedBondDiscountCurve::FittingMethod {
      public:
        CubicBSplinesFitting(const std::vector<Time>& knotVector,
                             bool constrainAtZero = true,
                             const Array& weights = Array(),
                             const ext::shared_ptr<OptimizationMethod>& optimizationMethod = {},
                             const Array& l2 = Array(),
                             Real minCutoffTime = 0.0,
                             Real maxCutoffTime = QL_MAX_REAL,
                             Constraint constraint = NoConstraint());
        CubicBSplinesFitting(c