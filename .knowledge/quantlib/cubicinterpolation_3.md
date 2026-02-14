 xEnd, yBegin,
                             FritschButland, true,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class Parabolic : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        Parabolic(const I1& xBegin,
                  const I1& xEnd,
                  const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             CubicInterpolation::Parabolic, false,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class MonotonicParabolic : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MonotonicParabolic(const I1& xBegin,
                           const I1& xEnd,
                           const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             Parabolic, true,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    //! %Cubic interpolation factory and traits
    /*! \ingroup interpolations */
    class Cubic {
      public:
        Cubic(CubicInterpolation::DerivativeApprox da
                  = CubicInterpolation::Kruger,
              bool monotonic = false,
              CubicInterpolation::BoundaryCondition leftCondition
                  = CubicInterpolation::SecondDerivative,
              Real leftConditionValue = 0.0,
              CubicInterpolation::BoundaryCondition rightCondition
                  = CubicInterpolation::SecondDerivative,
              Real rightConditionValue = 0.0)
        : da_(da), monotonic_(monotonic),
          leftType_(leftCondition), rightType_(rightCondition),
          leftValue_(leftConditionValue), rightValue_(rightConditionValue) {}
        template <class I1, class I2>
        Interpolation interpolate(const I1& xBegin,
                                  const I1& xEnd,
                                  const I2& yBegin) const {
            return CubicInterpolation(xBegin, xEnd, yBegin,
                                      da_, monotonic_,
                                      leftType_, leftValue_,
                                      rightType_, rightValue_);
        }
        static const bool global = true;
        static const Size requiredPoints = 2;
      private:
        CubicInterpolation::DerivativeApprox da_;
        bool monotonic_;
        CubicInterpolation::BoundaryCondition leftType_, rightType_;
        Real leftValue_, rightValue_;
    };


    namespace detail {

        template <class I1, class I2>
        class CubicInterpolationImpl final : public CoefficientHolder,
                                             public Interpolation::templateImpl<I1,I2> {
          public:
            CubicInterpolationImpl(const I1& xBegin,
                                   const I1& xEnd,
                                   const I2& yBegin,
                                   CubicInterpolation::DerivativeApprox da,
                                   bool monotonic,
                                   CubicInterpolation::BoundaryCondition leftCondition,
                                   Real leftConditionValue,
                                   CubicInterpolation::BoundaryCondition rightCondition,
                                   Real rightConditionValue)
            : CoefficientHolder(xEnd-xBegin),
              Interpolation::templateImpl<I1,I2>(xBegin, xEnd, yBegin,
                                                 Cubic::requiredPoints),
              da_(da),
              monotonic_(monotonic),
              leftType_(leftCondition), rightType_(rightCondition),
              leftValue_(leftConditionValue),
              rightValue_(rightConditionValue),
              tmp_(n_), dx_(n_-1), S_(n_-1), L_(n_)
