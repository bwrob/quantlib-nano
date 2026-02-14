FlatInterpolationImpl;
    }

    //! %Linear interpolation between discrete points with flat extapolation
    /*! \ingroup interpolations */
    class LinearFlatInterpolation : public Interpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        LinearFlatInterpolation(const I1& xBegin, const I1& xEnd,
                            const I2& yBegin) {
            impl_ = ext::shared_ptr<Interpolation::Impl>(new
                detail::LinearFlatInterpolationImpl<I1,I2>(xBegin, xEnd,
                                                       yBegin));
            impl_->update();
        }
    };

    //! %Linear-interpolation with flat-extrapolation factory and traits
    /*! \ingroup interpolations */
    class LinearFlat {
      public:
        template <class I1, class I2>
        Interpolation interpolate(const I1& xBegin, const I1& xEnd,
                                  const I2& yBegin) const {
            return LinearFlatInterpolation(xBegin, xEnd, yBegin);
        }
        static const bool global = false;
        static const Size requiredPoints = 1;
    };

    namespace detail {
        template <class I1, class I2>
        class LinearFlatInterpolationImpl final
            : public Interpolation::templateImpl<I1,I2> {
          public:
            LinearFlatInterpolationImpl(const I1& xBegin, const I1& xEnd,
                                    const I2& yBegin)
            : Interpolation::templateImpl<I1,I2>(xBegin, xEnd, yBegin,
                                    LinearFlat::requiredPoints),
              primitiveConst_(xEnd-xBegin), s_(xEnd-xBegin) {}
            void update() override {
                primitiveConst_[0] = 0.0;
                for (Size i=1; i<Size(this->xEnd_-this->xBegin_); ++i) {
                    Real dx = this->xBegin_[i]-this->xBegin_[i-1];
                    s_[i-1] = (this->yBegin_[i]-this->yBegin_[i-1])/dx;
                    primitiveConst_[i] = primitiveConst_[i-1]
                        + dx*(this->yBegin_[i-1] +0.5*dx*s_[i-1]);
                }
            }
            Real value(Real x) const override {
                if (x <= this->xMin())
                    return this->yBegin_[0];
                if (x >= this->xMax())
                    return *(this->yBegin_+(this->xEnd_-this->xBegin_)-1);
                Size i = this->locate(x);
                return this->yBegin_[i] + (x-this->xBegin_[i])*s_[i];
            }
            Real primitive(Real x) const override {
                Size i = this->locate(x);
                Real dx = x-this->xBegin_[i];
                return primitiveConst_[i] +
                    dx*(this->yBegin_[i] + 0.5*dx*s_[i]);
            }
            Real derivative(Real x) const override {
                if (!this->isInRange(x))
                    return 0;
                Size i = this->locate(x);
                return s_[i];
            }
            Real secondDerivative(Real) const override { return 0.0; }

          private:
            std::vector<Real> primitiveConst_, s_;
        };
    }

}


#endif
