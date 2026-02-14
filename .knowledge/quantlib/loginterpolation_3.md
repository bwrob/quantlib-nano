       Real rightConditionValue = 0.0)
        : n_(n), behavior_(behavior), da_(da), monotonic_(monotonic),
          leftType_(leftCondition), rightType_(rightCondition),
          leftValue_(leftConditionValue), rightValue_(rightConditionValue) {}
        template <class I1, class I2>
        Interpolation interpolate(const I1& xBegin, const I1& xEnd,
                                  const I2& yBegin) const {
            return LogMixedLinearCubicInterpolation(xBegin, xEnd, yBegin,
                                                    n_, behavior_,
                                                    da_, monotonic_,
                                                    leftType_, leftValue_,
                                                    rightType_, rightValue_);
        }
        static const bool global = true;
        static const Size requiredPoints = 3;
    private:
        Size n_;
        MixedInterpolation::Behavior behavior_;
        CubicInterpolation::DerivativeApprox da_;
        bool monotonic_;
        CubicInterpolation::BoundaryCondition leftType_, rightType_;
        Real leftValue_, rightValue_;
    };

    // convenience classes
    
    class DefaultLogMixedLinearCubic : public LogMixedLinearCubic {
      public:
        explicit DefaultLogMixedLinearCubic(const Size n,
                                            MixedInterpolation::Behavior behavior
                                            = MixedInterpolation::ShareRanges)
        : LogMixedLinearCubic(n, behavior,
                              CubicInterpolation::Kruger) {}
    };

    class MonotonicLogMixedLinearCubic : public LogMixedLinearCubic {
      public:
        explicit MonotonicLogMixedLinearCubic(const Size n,
                                              MixedInterpolation::Behavior behavior
                                              = MixedInterpolation::ShareRanges)
        : LogMixedLinearCubic(n, behavior,
                              CubicInterpolation::Spline, true,
                              CubicInterpolation::SecondDerivative, 0.0,
                              CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class KrugerLogMixedLinearCubic: public LogMixedLinearCubic {
      public:
        explicit KrugerLogMixedLinearCubic(const Size n,
                                           MixedInterpolation::Behavior behavior
                                           = MixedInterpolation::ShareRanges)
        : LogMixedLinearCubic(n, behavior,
                              CubicInterpolation::Kruger, false,
                              CubicInterpolation::SecondDerivative, 0.0,
                              CubicInterpolation::SecondDerivative, 0.0) {}
    };


    class LogMixedLinearCubicNaturalSpline : public LogMixedLinearCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        LogMixedLinearCubicNaturalSpline(const I1& xBegin, const I1& xEnd,
                                         const I2& yBegin, const Size n,
                                         MixedInterpolation::Behavior behavior
                                             = MixedInterpolation::ShareRanges)
        : LogMixedLinearCubicInterpolation(xBegin, xEnd, yBegin, n, behavior,
                                           CubicInterpolation::Spline, false,
                                           CubicInterpolation::SecondDerivative, 0.0,
                                           CubicInterpolation::SecondDerivative, 0.0) {}
    };


    namespace detail {

        template <class I1, class I2>
        class LogInterpolationImpl final
            : public Interpolation::templateImpl<I1, I2> {
          public:
            template <class Interpolator>
            LogInterpolationImpl(const I1& xBegin, const I1& xEnd,
                                 const I2& yBegin,
                                 const Interpolator& factory)
            : Interpolation::t