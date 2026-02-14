eal x, Real y) const override {
#if defined(QL_EXTRA_SAFETY_CHECKS)
                for (I1 i=xBegin_, j=xBegin_+1; j!=xEnd_; ++i, ++j)
                    QL_REQUIRE(*j > *i, "unsorted x values");
                #endif
                Real x1 = xMin(), x2 = xMax();
                bool xIsInrange = (x >= x1 && x <= x2) ||
                                  close(x,x1) ||
                                  close(x,x2);
                if (!xIsInrange) return false;

                #if defined(QL_EXTRA_SAFETY_CHECKS)
                for (I2 k=yBegin_, l=yBegin_+1; l!=yEnd_; ++k, ++l)
                    QL_REQUIRE(*l > *k, "unsorted y values");
                #endif
                Real y1 = yMin(), y2 = yMax();
                return (y >= y1 && y <= y2) || close(y,y1) || close(y,y2);
            }

          protected:
            Size locateX(Real x) const override {
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
            Size locateY(Real y) const override {
#if defined(QL_EXTRA_SAFETY_CHECKS)
                for (I2 k=yBegin_, l=yBegin_+1; l!=yEnd_; ++k, ++l)
                    QL_REQUIRE(*l > *k, "unsorted y values");
                #endif
                if (y < *yBegin_)
                    return 0;
                else if (y > *(yEnd_-1))
                    return yEnd_-yBegin_-2;
                else
                    return std::upper_bound(yBegin_,yEnd_-1,y)-yBegin_-1;
            }
            I1 xBegin_, xEnd_;
            I2 yBegin_, yEnd_;
            const M& zData_;
        };

        Interpolation2D() = default;
        Real operator()(Real x, Real y,
                        bool allowExtrapolation = false) const {
            checkRange(x,y,allowExtrapolation);
            return impl_->value(x,y);
        }
        Real xMin() const {
            return impl_->xMin();
        }
        Real xMax() const {
            return impl_->xMax();
        }
        std::vector<Real> xValues() const {
            return impl_->xValues();
        }
        Size locateX(Real x) const {
            return impl_->locateX(x);
        }
        Real yMin() const {
            return impl_->yMin();
        }
        Real yMax() const {
            return impl_->yMax();
        }
        std::vector<Real> yValues() const {
            return impl_->yValues();
        }
        Size locateY(Real y) const {
            return impl_->locateY(y);
        }
        const Matrix& zData() const {
            return impl_->zData();
        }
        bool isInRange(Real x, Real y) const {
            return impl_->isInRange(x,y);
        }
        void update() {
            impl_->calculate();
        }
      protected:
        void checkRange(Real x, Real y, bool extrapolate) const {
            QL_REQUIRE(extrapolate || allowsExtrapolation() ||
                       impl_->isInRange(x,y),
                       "interpolation range is ["
                       << impl_->xMin() << ", " << impl_->xMax()
                       << "] x ["
                       << impl_->yMin() << ", " << impl_->yMax()
                       << "]: extrapolation at ("
                       << x << ", " << y << ") not allowed");
        }
    };

}


#endif
