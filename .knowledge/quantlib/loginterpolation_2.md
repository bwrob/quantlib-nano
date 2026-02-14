Harmonic, false,
                                CubicInterpolation::SecondDerivative, 0.0,
                                CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class FritschButlandLogCubic : public LogCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        FritschButlandLogCubic(const I1& xBegin,
                               const I1& xEnd,
                               const I2& yBegin)
        : LogCubicInterpolation(xBegin, xEnd, yBegin,
                                CubicInterpolation::FritschButland, false,
                                CubicInterpolation::SecondDerivative, 0.0,
                                CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class LogParabolic : public LogCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        LogParabolic(const I1& xBegin,
                     const I1& xEnd,
                     const I2& yBegin)
        : LogCubicInterpolation(xBegin, xEnd, yBegin,
                                CubicInterpolation::Parabolic, false,
                                CubicInterpolation::SecondDerivative, 0.0,
                                CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class MonotonicLogParabolic : public LogCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MonotonicLogParabolic(const I1& xBegin,
                              const I1& xEnd,
                              const I2& yBegin)
        : LogCubicInterpolation(xBegin, xEnd, yBegin,
                                CubicInterpolation::Parabolic, true,
                                CubicInterpolation::SecondDerivative, 0.0,
                                CubicInterpolation::SecondDerivative, 0.0) {}
    };

    //! %log-mixedlinearcubic interpolation between discrete points
    /*! \ingroup interpolations */
    class LogMixedLinearCubicInterpolation : public Interpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        LogMixedLinearCubicInterpolation(const I1& xBegin, const I1& xEnd,
                                         const I2& yBegin, const Size n,
                                         MixedInterpolation::Behavior behavior,
                                         CubicInterpolation::DerivativeApprox da,
                                         bool monotonic,
                                         CubicInterpolation::BoundaryCondition leftC,
                                         Real leftConditionValue,
                                         CubicInterpolation::BoundaryCondition rightC,
                                         Real rightConditionValue) {
            impl_ = ext::make_shared<detail::LogInterpolationImpl<I1, I2>>(
                xBegin, xEnd, yBegin,
                MixedLinearCubic(n, behavior, da, monotonic,
                                 leftC, leftConditionValue,
                                 rightC, rightConditionValue));
            impl_->update();
        }
    };

    //! log-cubic interpolation factory and traits
    /*! \ingroup interpolations */
    class LogMixedLinearCubic {
      public:
        LogMixedLinearCubic(const Size n,
                            MixedInterpolation::Behavior behavior,
                            CubicInterpolation::DerivativeApprox da,
                            bool monotonic = true,
                            CubicInterpolation::BoundaryCondition leftCondition
                                = CubicInterpolation::SecondDerivative,
                            Real leftConditionValue = 0.0,
                            CubicInterpolation::BoundaryCondition rightCondition
                                = CubicInterpolation::SecondDerivative,

