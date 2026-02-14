              CubicInterpolation::BoundaryCondition rightCondition
                      = CubicInterpolation::SecondDerivative,
                  Real rightConditionValue = 0.0)
        : da_(da), monotonic_(monotonic),
          leftType_(leftCondition), rightType_(rightCondition),
          leftValue_(leftConditionValue), rightValue_(rightConditionValue) {}
        template <class I1, class I2>
        Interpolation interpolate(const I1& xBegin, const I1& xEnd,
                                  const I2& yBegin) const {
            return LogCubicInterpolation(xBegin, xEnd, yBegin,
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

    // convenience classes

    class DefaultLogCubic : public LogCubic {
      public:
        DefaultLogCubic()
        : LogCubic(CubicInterpolation::Kruger) {}
    };

    class MonotonicLogCubic : public LogCubic {
      public:
        MonotonicLogCubic()
        : LogCubic(CubicInterpolation::Spline, true,
                   CubicInterpolation::SecondDerivative, 0.0,
                   CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class KrugerLog : public LogCubic {
      public:
        KrugerLog()
        : LogCubic(CubicInterpolation::Kruger, false,
                   CubicInterpolation::SecondDerivative, 0.0,
                   CubicInterpolation::SecondDerivative, 0.0) {}
    };


    class LogCubicNaturalSpline : public LogCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        LogCubicNaturalSpline(const I1& xBegin,
                              const I1& xEnd,
                              const I2& yBegin)
        : LogCubicInterpolation(xBegin, xEnd, yBegin,
                                CubicInterpolation::Spline, false,
                                CubicInterpolation::SecondDerivative, 0.0,
                                CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class MonotonicLogCubicNaturalSpline : public LogCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MonotonicLogCubicNaturalSpline(const I1& xBegin,
                                       const I1& xEnd,
                                       const I2& yBegin)
        : LogCubicInterpolation(xBegin, xEnd, yBegin,
                                CubicInterpolation::Spline, true,
                                CubicInterpolation::SecondDerivative, 0.0,
                                CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class KrugerLogCubic : public LogCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        KrugerLogCubic(const I1& xBegin,
                       const I1& xEnd,
                       const I2& yBegin)
        : LogCubicInterpolation(xBegin, xEnd, yBegin,
                                CubicInterpolation::Kruger, false,
                                CubicInterpolation::SecondDerivative, 0.0,
                                CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class HarmonicLogCubic : public LogCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        HarmonicLogCubic(const I1& xBegin,
                         const I1& xEnd,
                         const I2& yBegin)
        : LogCubicInterpolation(xBegin, xEnd, yBegin,
                                CubicInterpolation::
