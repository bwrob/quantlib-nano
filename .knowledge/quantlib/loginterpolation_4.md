emplateImpl<I1, I2>(xBegin, xEnd, yBegin,
                                                  Interpolator::requiredPoints),
              logY_(xEnd-xBegin) {
                interpolation_ = factory.interpolate(this->xBegin_,
                                                     this->xEnd_,
                                                     logY_.begin());
            }
            void update() override {
                for (Size i=0; i<logY_.size(); ++i) {
                    QL_REQUIRE(this->yBegin_[i]>0.0,
                               "invalid value (" << this->yBegin_[i]
                               << ") at index " << i);
                    logY_[i] = std::log(this->yBegin_[i]);
                }
                interpolation_.update();
            }
            Real value(Real x) const override { return std::exp(interpolation_(x, true)); }
            Real primitive(Real) const override {
                QL_FAIL("LogInterpolation primitive not implemented");
            }
            Real derivative(Real x) const override {
                return value(x)*interpolation_.derivative(x, true);
            }
            Real secondDerivative(Real x) const override {
                return derivative(x)*interpolation_.derivative(x, true) +
                            value(x)*interpolation_.secondDerivative(x, true);
            }

          private:
            std::vector<Real> logY_;
            Interpolation interpolation_;
        };

    }

}

#endif
