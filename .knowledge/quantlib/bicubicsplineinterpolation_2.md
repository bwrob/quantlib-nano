vativeX(Real x, Real y) const {
            return ext::dynamic_pointer_cast<detail::BicubicSplineDerivatives>
                    (impl_)->secondDerivativeX(x, y);
        }
        Real secondDerivativeY(Real x, Real y) const {
            return ext::dynamic_pointer_cast<detail::BicubicSplineDerivatives>
                    (impl_)->secondDerivativeY(x, y);
        }

        Real derivativeXY(Real x, Real y) const {
            return ext::dynamic_pointer_cast<detail::BicubicSplineDerivatives>
                    (impl_)->derivativeXY(x, y);
        }
    };

    //! bicubic-spline-interpolation factory
    class Bicubic {
      public:
        template <class I1, class I2, class M>
        Interpolation2D interpolate(const I1& xBegin, const I1& xEnd,
                                    const I2& yBegin, const I2& yEnd,
                                    const M& z) const {
            return BicubicSpline(xBegin,xEnd,yBegin,yEnd,z);
        }
    };

}

#endif
