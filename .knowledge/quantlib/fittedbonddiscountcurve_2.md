sed as weights to each bond. If not given
        or empty, then the bonds will be weighted by inverse duration

        An optional Array may be provided as an L2 regularizor in this case
        a L2 (gaussian) penalty is applied to each parameter starting from the
        initial guess. This is the same as giving a Gaussian prior on the parameters

        \todo derive the special-case class LinearFittingMethods from
              FittingMethod. A linear fitting to a set of basis
              functions \f$ b_i(t) \f$ is any fitting of the form
              \f[
              d(t) = \sum_{i=0} c_i b_i(t)
              \f]
              i.e., linear in the unknown coefficients \f$ c_i
              \f$. Such a fitting can be reduced to a linear algebra
              problem \f$ Ax = b \f$, and for large numbers of bonds,
              would typically be much faster computationally than the
              generic non-linear fitting method.

        \warning some parameters to the Simplex optimization method
                 may need to be tweaked internally to the class,
                 depending on the fitting method used, in order to get
                 proper/reasonable/faster convergence.
    */
    class FittedBondDiscountCurve::FittingMethod {
        friend class FittedBondDiscountCurve;
        // internal class
        class FittingCost;
      public:
        virtual ~FittingMethod() = default;
        //! total number of coefficients to fit/solve for
        virtual Size size() const = 0;
        //! output array of results of optimization problem
        Array solution() const;
        //! final number of iterations used in the optimization problem
        Integer numberOfIterations() const;
        //! final value of cost function after optimization
        Real minimumCostValue() const;
        //! error code of the optimization
        EndCriteria::Type errorCode() const;
        //! clone of the current object
        virtual std::unique_ptr<FittingMethod> clone() const = 0;
        //! return whether there is a constraint at zero
        bool constrainAtZero() const;
        //! return weights being used
        Array weights() const;
        //! return l2 penalties being used
        Array l2() const;
        //! return optimization method being used
        ext::shared_ptr<OptimizationMethod> optimizationMethod() const;
        //! return optimization contraint
        const Constraint& constraint() const;
        //! open discountFunction to public
        DiscountFactor discount(const Array& x, Time t) const;
      protected:
        //! constructors
        FittingMethod(bool constrainAtZero = true,
                      const Array& weights = Array(),
                      ext::shared_ptr<OptimizationMethod> optimizationMethod =
                          ext::shared_ptr<OptimizationMethod>(),
                      Array l2 = Array(),
                      Real minCutoffTime = 0.0,
                      Real maxCutoffTime = QL_MAX_REAL,
                      Constraint constraint = NoConstraint());
        //! rerun every time instruments/referenceDate changes
        virtual void init();
        //! discount function called by FittedBondDiscountCurve
        virtual DiscountFactor discountFunction(const Array& x,
                                                Time t) const = 0;

        //! constrains discount function to unity at \f$ T=0 \f$, if true
        bool constrainAtZero_;
        //! internal reference to the FittedBondDiscountCurve instance
        FittedBondDiscountCurve* curve_;
        //! solution array found from optimization, set in calculate()
        Array solution_;
        //! optional guess solution to be passed into constructor.
        /*! The idea is to use a previous solution as a guess solution to
            the discount curve, in an attempt to speed up calculations.
        */
        Array guessSolution_;
        //! base class sets this cost function used in the optimiza
