emiaBS.push_back(blackFormula(Option::Call, this->xBegin_[i], fwd_, atmVol_ * std::sqrt(T_), dDiscount_));
                    premiaMKT.push_back(blackFormula(Option::Call, this->xBegin_[i], fwd_, this->yBegin_[i] * std::sqrt(T_), dDiscount_));
                    vegas.push_back(vega(this->xBegin_[i]));
                }
            }
            Real value(Real k) const override {
                Real x1 = vega(k)/vegas[0]
                    * (std::log(this->xBegin_[1]/k) * std::log(this->xBegin_[2]/k))
                    / (std::log(this->xBegin_[1]/this->xBegin_[0]) * std::log(this->xBegin_[2]/this->xBegin_[0]));
                Real x2 = vega(k)/vegas[1]
                    * (std::log(k/this->xBegin_[0]) * std::log(this->xBegin_[2]/k))
                    / (std::log(this->xBegin_[1]/this->xBegin_[0]) * std::log(this->xBegin_[2]/this->xBegin_[1]));
                Real x3 = vega(k)/vegas[2]
                    * (std::log(k/this->xBegin_[0]) * std::log(k/this->xBegin_[1]))
                    / (std::log(this->xBegin_[2]/this->xBegin_[0]) * std::log(this->xBegin_[2]/this->xBegin_[1]));

                Real cBS = blackFormula(Option::Call, k, fwd_, atmVol_ * std::sqrt(T_), dDiscount_);
                Real c = cBS + x1*(premiaMKT[0] - premiaBS[0]) + x2*(premiaMKT[1] - premiaBS[1]) + x3*(premiaMKT[2] - premiaBS[2]);
                Real std = blackFormulaImpliedStdDev(Option::Call, k, fwd_, c, dDiscount_);
                return std / sqrt(T_);
            }
            Real primitive(Real) const override {
                QL_FAIL("Vanna Volga primitive not implemented");
            }
            Real derivative(Real) const override {
                QL_FAIL("Vanna Volga derivative not implemented");
            }
            Real secondDerivative(Real) const override {
                QL_FAIL("Vanna Volga secondDerivative not implemented");
            }

          private:
            std::vector<Real> premiaBS;
            std::vector<Real> premiaMKT;
            std::vector<Real> vegas;
            Real atmVol_;
            Real spot_;
            Real fwd_;
            DiscountFactor dDiscount_;
            DiscountFactor fDiscount_;
            Time T_;

            Real vega(Real k) const {
                Real d1 = (std::log(fwd_/k) + 0.5 * std::pow(atmVol_, 2.0) * T_)/(atmVol_ * std::sqrt(T_));
                NormalDistribution norm;
                return spot_ * dDiscount_ * std::sqrt(T_) * norm(d1);
            }
        };

    }

}

#endif