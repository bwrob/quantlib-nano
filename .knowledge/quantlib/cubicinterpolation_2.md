c:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        CubicNaturalSpline(const I1& xBegin,
                           const I1& xEnd,
                           const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             Spline, false,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class MonotonicCubicNaturalSpline : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MonotonicCubicNaturalSpline(const I1& xBegin,
                                    const I1& xEnd,
                                    const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             Spline, true,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class CubicSplineOvershootingMinimization1 : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        CubicSplineOvershootingMinimization1 (const I1& xBegin,
                                           const I1& xEnd,
                                           const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             SplineOM1, false,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class CubicSplineOvershootingMinimization2 : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        CubicSplineOvershootingMinimization2 (const I1& xBegin,
                                           const I1& xEnd,
                                           const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             SplineOM2, false,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class AkimaCubicInterpolation : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        AkimaCubicInterpolation(const I1& xBegin,
                                const I1& xEnd,
                                const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             Akima, false,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class KrugerCubic : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        KrugerCubic(const I1& xBegin,
                    const I1& xEnd,
                    const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             Kruger, false,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class HarmonicCubic : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        HarmonicCubic(const I1& xBegin,
                      const I1& xEnd,
                      const I2& yBegin)
        : CubicInterpolation(xBegin, xEnd, yBegin,
                             Harmonic, false,
                             SecondDerivative, 0.0,
                             SecondDerivative, 0.0) {}
    };

    class FritschButlandCubic : public CubicInterpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        FritschButlandCubic(const I1& xBegin,
                            const I1& xEnd,
                            const I2& yBegin)
        : CubicInterpolation(xBegin,