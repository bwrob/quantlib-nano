    auto x = this->xBegin_;
                auto y = this->yBegin_;
                std::vector<Real> times, blackVols;
                for ( ; x!=this->xEnd_; ++x, ++y) {
                    times.push_back(*x);
                    blackVols.push_back(*y);
                }
                abcdCalibrator_ = ext::shared_ptr<AbcdCalibration>(
                    new AbcdCalibration(times, blackVols,
                                        a_, b_, c_, d_,
                                        aIsFixed_, bIsFixed_,
                                        cIsFixed_, dIsFixed_,
                                        vegaWeighted_,
                                        endCriteria_,
                                        optMethod_));
                abcdCalibrator_->compute();
                a_ = abcdCalibrator_->a();
                b_ = abcdCalibrator_->b();
                c_ = abcdCalibrator_->c();
                d_ = abcdCalibrator_->d();
                k_ = abcdCalibrator_->k(times, blackVols);
                error_ = abcdCalibrator_->error();
                maxError_ = abcdCalibrator_->maxError();
                abcdEndCriteria_ = abcdCalibrator_->endCriteria();
            }
            Real value(Real x) const override {
                QL_REQUIRE(x>=0.0, "time must be non negative: " <<
                                   x << " not allowed");
                return abcdCalibrator_->value(x);
            }
            Real primitive(Real) const override { QL_FAIL("Abcd primitive not implemented"); }
            Real derivative(Real) const override { QL_FAIL("Abcd derivative not implemented"); }
            Real secondDerivative(Real) const override {
                QL_FAIL("Abcd secondDerivative not implemented");
            }
            Real k(Time t) const {
                LinearInterpolation li(this->xBegin_, this->xEnd_, this->yBegin_);
                return li(t);
            }

          private:
            const ext::shared_ptr<EndCriteria> endCriteria_;
            const ext::shared_ptr<OptimizationMethod> optMethod_;
            bool vegaWeighted_;
            ext::shared_ptr<AbcdCalibration> abcdCalibrator_;

        };

    }

    //! %Abcd interpolation between discrete points.
    /*! \ingroup interpolations
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class AbcdInterpolation : public Interpolation {
      public:
        /*! Constructor */
        template <class I1, class I2>
        AbcdInterpolation(const I1& xBegin,  // x = times
                          const I1& xEnd,
                          const I2& yBegin,  // y = volatilities
                          Real a = -0.06,
                          Real b =  0.17,
                          Real c =  0.54,
                          Real d =  0.17,
                          bool aIsFixed = false,
                          bool bIsFixed = false,
                          bool cIsFixed = false,
                          bool dIsFixed = false,
                          bool vegaWeighted = false,
                          const ext::shared_ptr<EndCriteria>& endCriteria
                              = ext::shared_ptr<EndCriteria>(),
                          const ext::shared_ptr<OptimizationMethod>& optMethod
                              = ext::shared_ptr<OptimizationMethod>()) {

            impl_ = ext::shared_ptr<Interpolation::Impl>(new
                detail::AbcdInterpolationImpl<I1,I2>(xBegin, xEnd, yBegin,
                                                     a, b, c, d,
                                                     aIsFixed, bIsFixed,
                                                     cIsFixed, dIsFixed,
                                                     vegaWeighted,
                                                     endCriteria,
                                                     optMethod));
            impl_->update();
