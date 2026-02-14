,
                    CubicInterpolation::SecondDerivative, 0.0,
                    CubicInterpolation::SecondDerivative, 0.0).derivative(x);
            }

            Real secondDerivativeX(Real x, Real y) const override {
                std::vector<Real> section(this->zData_.columns());
                for (Size i=0; i < section.size(); ++i) {
                    section[i] = value(this->xBegin_[i], y);
                }
                
                return CubicInterpolation(
                    this->xBegin_, this->xEnd_,
                    section.begin(),
                    CubicInterpolation::Spline, false,
                    CubicInterpolation::SecondDerivative, 0.0,
                    CubicInterpolation::SecondDerivative, 0.0)
                                                          .secondDerivative(x);
            }

            Real derivativeY(Real x, Real y) const override {
                std::vector<Real> section(splines_.size());
                for (Size i=0; i<splines_.size(); i++)
                    section[i]=splines_[i](x,true);

                return CubicInterpolation(
                    this->yBegin_, this->yEnd_,
                    section.begin(),
                    CubicInterpolation::Spline, false,
                    CubicInterpolation::SecondDerivative, 0.0,
                    CubicInterpolation::SecondDerivative, 0.0).derivative(y);
            }

            Real secondDerivativeY(Real x, Real y) const override {
                std::vector<Real> section(splines_.size());
                for (Size i=0; i<splines_.size(); i++)
                    section[i]=splines_[i](x,true);

                return CubicInterpolation(
                    this->yBegin_, this->yEnd_,
                    section.begin(),
                    CubicInterpolation::Spline, false,
                    CubicInterpolation::SecondDerivative, 0.0,
                    CubicInterpolation::SecondDerivative, 0.0)
                                                        .secondDerivative(y);
            }

            Real derivativeXY(Real x, Real y) const override {
                std::vector<Real> section(this->zData_.columns());
                for (Size i=0; i < section.size(); ++i) {
                    section[i] = derivativeY(this->xBegin_[i], y);
                }
                
                return CubicInterpolation(
                    this->xBegin_, this->xEnd_,
                    section.begin(),
                    CubicInterpolation::Spline, false,
                    CubicInterpolation::SecondDerivative, 0.0,
                    CubicInterpolation::SecondDerivative, 0.0).derivative(x);
            }

          private:
            std::vector<Interpolation> splines_;
        };

    }

    //! bicubic-spline interpolation between discrete points
    /*! \ingroup interpolations
        \todo revise end conditions
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class BicubicSpline : public Interpolation2D {
      public:
        /*! \pre the \f$ x \f$ and \f$ y \f$ values must be sorted. */
        template <class I1, class I2, class M>
        BicubicSpline(const I1& xBegin, const I1& xEnd,
                      const I2& yBegin, const I2& yEnd,
                      const M& zData) {
            impl_ = ext::shared_ptr<Interpolation2D::Impl>(
                  new detail::BicubicSplineImpl<I1,I2,M>(xBegin, xEnd,
                                                         yBegin, yEnd, zData));
        }
        
        Real derivativeX(Real x, Real y) const {
            return ext::dynamic_pointer_cast<detail::BicubicSplineDerivatives>
                    (impl_)->derivativeX(x, y);
        }
        Real derivativeY(Real x, Real y) const {
            return ext::dynamic_pointer_cast<detail::BicubicSplineDerivatives>
                    (impl_)->derivativeY(x, y);
        }
        Real secondDeri