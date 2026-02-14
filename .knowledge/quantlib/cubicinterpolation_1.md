     Mathematics Of Computation, v. 52, n. 186, April 1989, pp. 471-494.

        \todo implement missing schemes (FourthOrder and ModifiedParabolic) and
              missing boundary conditions (Periodic and Lagrange).

        \test to be adapted from old ones.

        \ingroup interpolations
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class CubicInterpolation : public Interpolation {
      public:
        enum DerivativeApprox {
            /*! Spline approximation (non-local, non-monotonic, linear[?]).
                Different boundary conditions can be used on the left and right
                boundaries: see BoundaryCondition.
            */
            Spline,

            //! Overshooting minimization 1st derivative
            SplineOM1,

            //! Overshooting minimization 2nd derivative
            SplineOM2,

            //! Fourth-order approximation (local, non-monotonic, linear)
            FourthOrder,

            //! Parabolic approximation (local, non-monotonic, linear)
            Parabolic,

            //! Fritsch-Butland approximation (local, monotonic, non-linear)
            FritschButland,

            //! Akima approximation (local, non-monotonic, non-linear)
            Akima,

            //! Kruger approximation (local, monotonic, non-linear)
            Kruger, 

            //! Weighted harmonic mean approximation (local, monotonic, non-linear)
            Harmonic,
        };
        enum BoundaryCondition {
            //! Make second(-last) point an inactive knot
            NotAKnot,

            //! Match value of end-slope
            FirstDerivative,

            //! Match value of second derivative at end
            SecondDerivative,

            //! Match first and second derivative at either end
            Periodic,

            /*! Match end-slope to the slope of the cubic that matches
                the first four data at the respective end
            */
            Lagrange
        };
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        CubicInterpolation(const I1& xBegin,
                           const I1& xEnd,
                           const I2& yBegin,
                           CubicInterpolation::DerivativeApprox da,
                           bool monotonic,
                           CubicInterpolation::BoundaryCondition leftCond,
                           Real leftConditionValue,
                           CubicInterpolation::BoundaryCondition rightCond,
                           Real rightConditionValue) {
            impl_ = ext::shared_ptr<Interpolation::Impl>(new
                detail::CubicInterpolationImpl<I1,I2>(xBegin, xEnd, yBegin,
                                                      da,
                                                      monotonic,
                                                      leftCond,
                                                      leftConditionValue,
                                                      rightCond,
                                                      rightConditionValue));
            impl_->update();
        }
        const std::vector<Real>& primitiveConstants() const {
            return coeffs().primitiveConst_;
        }
        const std::vector<Real>& aCoefficients() const { return coeffs().a_; }
        const std::vector<Real>& bCoefficients() const { return coeffs().b_; }
        const std::vector<Real>& cCoefficients() const { return coeffs().c_; }
        const std::vector<bool>& monotonicityAdjustments() const {
            return coeffs().monotonicityAdjustments_;
        }
      private:
        const detail::CoefficientHolder& coeffs() const {
            return *dynamic_cast<detail::CoefficientHolder*>(impl_.get());
        }
    };


    // convenience classes

    class CubicNaturalSpline : public CubicInterpolation {
      publi