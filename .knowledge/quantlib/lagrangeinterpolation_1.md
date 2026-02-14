      QL_FAIL("LagrangeInterpolation secondDerivative "
                        "is not implemented");
            }

            Real value(const Array& y, Real x) const override { return _value(y.begin(), x); }

          private:
            template <class Iterator>
            Real _value(const Iterator& yBegin, Real x) const {

                const Real eps = 10*QL_EPSILON*std::abs(x);
                const auto iter = std::lower_bound(
                    this->xBegin_, this->xEnd_, x - eps);
                if (iter != this->xEnd_ && *iter - x < eps) {
                    return yBegin[std::distance(this->xBegin_, iter)];
                }

                Real n = 0.0, d = 0.0;
                for (Size i = 0; i < n_; ++i) {
                    const Real alpha = lambda_[i] / (x - this->xBegin_[i]);
                    n += alpha * yBegin[i];
                    d += alpha;
                }
                return n / d;
              }

              const Size n_;
              Array lambda_;
        };
    }

    /*! \ingroup interpolations
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class LagrangeInterpolation : public Interpolation {
      public:
        template <class I1, class I2>
        LagrangeInterpolation(const I1& xBegin, const I1& xEnd,
                              const I2& yBegin) {
            impl_ = ext::make_shared<detail::LagrangeInterpolationImpl<I1,I2> >(
                xBegin, xEnd, yBegin);
            impl_->update();
        }

        // interpolate with new set of y values for a new x value
        Real value(const Array& y, Real x) const {
            return ext::dynamic_pointer_cast<detail::UpdatedYInterpolation>
                (impl_)->value(y, x);
        }
    };

}

#endif
