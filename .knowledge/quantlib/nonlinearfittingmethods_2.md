onst std::vector<Time>& knotVector,
                             bool constrainAtZero,
                             const Array& weights,
                             const Array& l2,
                             Real minCutoffTime = 0.0,
                             Real maxCutoffTime = QL_MAX_REAL,
                             Constraint constraint = NoConstraint());
        //! cubic B-spline basis functions
        Real basisFunction(Integer i, Time t) const;
        std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const override;
      private:
        Size size() const override;
        DiscountFactor discountFunction(const Array& x, Time t) const override;
        BSpline splines_;
        Size size_;
        //! N_th basis function coefficient to solve for when d(0)=1
        Natural N_;
    };

        //! Natural cubic spline fitting method
    /*! Fits a discount function using natural cubic spline interpolation
        where the parameters are nodal discount values d(t_i).
        The natural boundary condition (second derivative = 0 at ends)
        is used. If constrainAtZero is true, d(0) is fixed to 1.0 and
        the parameter vector x contains the remaining nodal values.
    */
    class NaturalCubicFitting : public FittedBondDiscountCurve::FittingMethod {
      public:
        explicit
        NaturalCubicFitting(const std::vector<Time>& knotTimes,
                            const Array& weights = Array(),
                            const ext::shared_ptr<OptimizationMethod>& optimizationMethod = {},
                            const Array& l2 = Array(),
                            Real minCutoffTime = 0.0,
                            Real maxCutoffTime = QL_MAX_REAL,
                            Constraint constraint = NoConstraint());

        NaturalCubicFitting(const std::vector<Time>& knotTimes,
                            const Array& weights,
                            const Array& l2,
                            Real minCutoffTime = 0.0,
                            Real maxCutoffTime = QL_MAX_REAL,
                            Constraint constraint = NoConstraint());

        std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const override;

      protected:
        Size size() const override;
        DiscountFactor discountFunction(const Array& x, Time t) const override;

      private:
        std::vector<Time> knotTimes_;
        Size size_;
    };

    //! Simple polynomial fitting method
    /*! Fits a discount function to the simple polynomial form:
        \f[
        d(t) = \sum_{i=0}^{degree} c_i t^{i}
        \f]
        where the constants \f$ c_i \f$ are to be determined.

        This is a simple/crude, but fast and robust, means of fitting
        a yield curve.
    */
    class SimplePolynomialFitting
        : public FittedBondDiscountCurve::FittingMethod {
      public:
        SimplePolynomialFitting(Natural degree,
                                bool constrainAtZero = true,
                                const Array& weights = Array(),
                                const ext::shared_ptr<OptimizationMethod>& optimizationMethod = {},
                                const Array& l2 = Array(),
                                Real minCutoffTime = 0.0,
                                Real maxCutoffTime = QL_MAX_REAL,
                                Constraint constraint = NoConstraint());
        SimplePolynomialFitting(Natural degree,
                                bool constrainAtZero,
                                const Array& weights,
                                const Array& l2,
                                Real minCutoffTime = 0.0,
                                Real maxCutoffTime = QL_MAX_REAL,
                                Constraint constraint = NoConstraint());
        std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const override;
      private:
        Size size() const override;
        DiscountFactor discountFunc
