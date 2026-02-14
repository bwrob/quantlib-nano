nic_(monotonic),
          leftType_(leftCondition), rightType_(rightCondition),
          leftValue_(leftConditionValue), rightValue_(rightConditionValue) {}
        template <class I1, class I2>
        Interpolation interpolate(const I1& xBegin, const I1& xEnd,
                                  const I2& yBegin) const {
            return MixedLinearCubicInterpolation(xBegin, xEnd,
                                                 yBegin, n_, behavior_,
                                                 da_, monotonic_,
                                                 leftType_, leftValue_,
                                                 rightType_, rightValue_);
        }
        // fix below
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

    class MixedLinearCubicNaturalSpline : public MixedLinearCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MixedLinearCubicNaturalSpline(const I1& xBegin, const I1& xEnd,
                                      const I2& yBegin, Size n,
                                      MixedInterpolation::Behavior behavior
                                            = MixedInterpolation::ShareRanges)
        : MixedLinearCubicInterpolation(xBegin, xEnd, yBegin, n, behavior,
                                        CubicInterpolation::Spline, false,
                                        CubicInterpolation::SecondDerivative, 0.0,
                                        CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class MixedLinearMonotonicCubicNaturalSpline : public MixedLinearCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MixedLinearMonotonicCubicNaturalSpline(const I1& xBegin, const I1& xEnd,
                                               const I2& yBegin, Size n,
                                               MixedInterpolation::Behavior behavior
                                                   = MixedInterpolation::ShareRanges)
        : MixedLinearCubicInterpolation(xBegin, xEnd, yBegin, n, behavior,
                                        CubicInterpolation::Spline, true,
                                        CubicInterpolation::SecondDerivative, 0.0,
                                        CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class MixedLinearKrugerCubic : public MixedLinearCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MixedLinearKrugerCubic(const I1& xBegin, const I1& xEnd,
                               const I2& yBegin, Size n,
                               MixedInterpolation::Behavior behavior
                                            = MixedInterpolation::ShareRanges)
        : MixedLinearCubicInterpolation(xBegin, xEnd, yBegin, n, behavior,
                                        CubicInterpolation::Kruger, false,
                                        CubicInterpolation::SecondDerivative, 0.0,
                                        CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class MixedLinearFritschButlandCubic : public MixedLinearCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MixedLinearFritschButlandCubic(const I1& xBegin, const I1& xEnd,
                                       const I2& yBegin, Size n,
                                       MixedInterpolation::Behavior behavior
                                            = MixedInterpolation::S
