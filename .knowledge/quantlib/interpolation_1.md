n std::vector<Real>(yBegin_,yBegin_+(xEnd_-xBegin_));
            }
            bool isInRange(Real x) const override {
#if defined(QL_EXTRA_SAFETY_CHECKS)
                for (I1 i=xBegin_, j=xBegin_+1; j!=xEnd_; ++i, ++j)
                    QL_REQUIRE(*j > *i, "unsorted x values");
                #endif
                Real x1 = xMin(), x2 = xMax();
                return (x >= x1 && x <= x2) || close(x,x1) || close(x,x2);
            }

          protected:
            Size locate(Real x) const {
                #if defined(QL_EXTRA_SAFETY_CHECKS)
                for (I1 i=xBegin_, j=xBegin_+1; j!=xEnd_; ++i, ++j)
                    QL_REQUIRE(*j > *i, "unsorted x values");
                #endif
                if (x < *xBegin_)
                    return 0;
                else if (x > *(xEnd_-1))
                    return xEnd_-xBegin_-2;
                else
                    return std::upper_bound(xBegin_,xEnd_-1,x)-xBegin_-1;
            }
            I1 xBegin_, xEnd_;
            I2 yBegin_;
        };

        Interpolation() = default;
        ~Interpolation() override = default;
        bool empty() const { return !impl_; }
        Real operator()(Real x, bool allowExtrapolation = false) const {
            checkRange(x,allowExtrapolation);
            return impl_->value(x);
        }
        Real primitive(Real x, bool allowExtrapolation = false) const {
            checkRange(x,allowExtrapolation);
            return impl_->primitive(x);
        }
        Real derivative(Real x, bool allowExtrapolation = false) const {
            checkRange(x,allowExtrapolation);
            return impl_->derivative(x);
        }
        Real secondDerivative(Real x, bool allowExtrapolation = false) const {
            checkRange(x,allowExtrapolation);
            return impl_->secondDerivative(x);
        }
        Real xMin() const {
            return impl_->xMin();
        }
        Real xMax() const {
            return impl_->xMax();
        }
        bool isInRange(Real x) const {
            return impl_->isInRange(x);
        }
        void update() {
            impl_->update();
        }
      protected:
        void checkRange(Real x, bool extrapolate) const {
            QL_REQUIRE(extrapolate || allowsExtrapolation() ||
                       impl_->isInRange(x),
                       "interpolation range is ["
                       << impl_->xMin() << ", " << impl_->xMax()
                       << "]: extrapolation at " << x << " not allowed");
        }
    };

}

#endif
