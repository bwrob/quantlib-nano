   monotonicityAdjustments_[i] = true;
                            }
                        }
                    }
                }


                // cubic coefficients
                for (Size i=0; i<n_-1; ++i) {
                    a_[i] = tmp_[i];
                    b_[i] = (3.0*S_[i] - tmp_[i+1] - 2.0*tmp_[i])/dx_[i];
                    c_[i] = (tmp_[i+1] + tmp_[i] - 2.0*S_[i])/(dx_[i]*dx_[i]);
                }

                primitiveConst_[0] = 0.0;
                for (Size i=1; i<n_-1; ++i) {
                    primitiveConst_[i] = primitiveConst_[i-1]
                        + dx_[i-1] *
                        (this->yBegin_[i-1] + dx_[i-1] *
                         (a_[i-1]/2.0 + dx_[i-1] *
                          (b_[i-1]/3.0 + dx_[i-1] * c_[i-1]/4.0)));
                }
            }
            Real value(Real x) const override {
                Size j = this->locate(x);
                Real dx_ = x-this->xBegin_[j];
                return this->yBegin_[j] + dx_*(a_[j] + dx_*(b_[j] + dx_*c_[j]));
            }
            Real primitive(Real x) const override {
                Size j = this->locate(x);
                Real dx_ = x-this->xBegin_[j];
                return primitiveConst_[j]
                    + dx_*(this->yBegin_[j] + dx_*(a_[j]/2.0
                    + dx_*(b_[j]/3.0 + dx_*c_[j]/4.0)));
            }
            Real derivative(Real x) const override {
                Size j = this->locate(x);
                Real dx_ = x-this->xBegin_[j];
                return a_[j] + (2.0*b_[j] + 3.0*c_[j]*dx_)*dx_;
            }
            Real secondDerivative(Real x) const override {
                Size j = this->locate(x);
                Real dx_ = x-this->xBegin_[j];
                return 2.0*b_[j] + 6.0*c_[j]*dx_;
            }

          private:
            CubicInterpolation::DerivativeApprox da_;
            bool monotonic_;
            CubicInterpolation::BoundaryCondition leftType_, rightType_;
            Real leftValue_, rightValue_;
            mutable Array tmp_;
            mutable std::vector<Real> dx_, S_;
            mutable TridiagonalOperator L_;

            Real cubicInterpolatingPolynomialDerivative(
                               Real a, Real b, Real c, Real d,
                               Real u, Real v, Real w, Real z, Real x) const {
                return (-((((a-c)*(b-c)*(c-x)*z-(a-d)*(b-d)*(d-x)*w)*(a-x+b-x)
                           +((a-c)*(b-c)*z-(a-d)*(b-d)*w)*(a-x)*(b-x))*(a-b)+
                          ((a-c)*(a-d)*v-(b-c)*(b-d)*u)*(c-d)*(c-x)*(d-x)
                          +((a-c)*(a-d)*(a-x)*v-(b-c)*(b-d)*(b-x)*u)
                          *(c-x+d-x)*(c-d)))/
                    ((a-b)*(a-c)*(a-d)*(b-c)*(b-d)*(c-d));
            }
        };

    }

}

#endif
