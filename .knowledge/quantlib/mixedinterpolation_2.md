hareRanges)
        : MixedLinearCubicInterpolation(xBegin, xEnd, yBegin, n, behavior,
                                        CubicInterpolation::FritschButland, false,
                                        CubicInterpolation::SecondDerivative, 0.0,
                                        CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class MixedLinearParabolic : public MixedLinearCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MixedLinearParabolic(const I1& xBegin, const I1& xEnd,
                             const I2& yBegin, Size n,
                             MixedInterpolation::Behavior behavior
                                            = MixedInterpolation::ShareRanges)
        : MixedLinearCubicInterpolation(xBegin, xEnd, yBegin, n, behavior,
                                        CubicInterpolation::Parabolic, false,
                                        CubicInterpolation::SecondDerivative, 0.0,
                                        CubicInterpolation::SecondDerivative, 0.0) {}
    };

    class MixedLinearMonotonicParabolic : public MixedLinearCubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MixedLinearMonotonicParabolic(const I1& xBegin, const I1& xEnd,
                                      const I2& yBegin, Size n,
                                      MixedInterpolation::Behavior behavior
                                            = MixedInterpolation::ShareRanges)
        : MixedLinearCubicInterpolation(xBegin, xEnd, yBegin, n, behavior,
                                        CubicInterpolation::Parabolic, true,
                                        CubicInterpolation::SecondDerivative, 0.0,
                                        CubicInterpolation::SecondDerivative, 0.0) {}
    };

    namespace detail {

        template <class I1, class I2>
        class MixedInterpolationImpl final
            : public Interpolation::templateImpl<I1, I2> {
          public:
            template <class Interpolator1, class Interpolator2>
            MixedInterpolationImpl(const I1& xBegin, const I1& xEnd,
                                   const I2& yBegin, Size n,
                                   MixedInterpolation::Behavior behavior,
                                   const Interpolator1& factory1,
                                   const Interpolator2& factory2)
            : Interpolation::templateImpl<I1, I2>(xBegin, xEnd, yBegin, 1) {
                Size maxN = static_cast<Size>(xEnd - xBegin);
                // SplitRanges needs xBegin2_+1 to be valid
                if (behavior == MixedInterpolation::SplitRanges) {
                    --maxN;
                }
                // This only checks that we pass valid iterators into interpolate()
                // calls below. The calls themselves check requiredPoints for each
                // of the segments.
                QL_REQUIRE(n <= maxN, "n is too large (" << n << " > " << maxN << ")");

                xBegin2_ = this->xBegin_ + n;

                switch (behavior) {
                  case MixedInterpolation::ShareRanges:
                    interpolation1_ = factory1.interpolate(this->xBegin_,
                                                           this->xEnd_,
                                                           this->yBegin_);
                    interpolation2_ = factory2.interpolate(this->xBegin_,
                                                           this->xEnd_,
                                                           this->yBegin_);
                    break;
                  case MixedInterpolation::SplitRanges:
                    interpolation1_ = factory1.interpolate(this->xBegin_,
                                                           this->xBegin2_ + 1,
                                                           this->
