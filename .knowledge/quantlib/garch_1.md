nd(),
                      method, endCriteria, initialGuess);
        }

        template <typename ForwardIterator>
        void calibrate(ForwardIterator begin, ForwardIterator end) {
            std::vector<Volatility> r2;
            Real mean_r2 = to_r2(begin, end, r2);
            ext::shared_ptr<Problem> p =
                calibrate_r2(mode_, r2, mean_r2, alpha_, beta_, vl_);
            gamma_ = 1 - alpha_ - beta_;
            vl_ /= gamma_;
            logLikelihood_ = p ? -p->functionValue() :
                                 -costFunction(begin, end);
        }

        template <typename ForwardIterator>
        void calibrate(ForwardIterator begin, ForwardIterator end,
                       OptimizationMethod& method,
                       EndCriteria endCriteria) {
            std::vector<Volatility> r2;
            Real mean_r2 = to_r2(begin, end, r2);
            ext::shared_ptr<Problem> p =
                calibrate_r2(mode_, r2, mean_r2, method,
                             endCriteria, alpha_, beta_, vl_);
            gamma_ = 1 - alpha_ - beta_;
            vl_ /= gamma_;
            logLikelihood_ = p ? -p->functionValue() :
                                 -costFunction(begin, end);
        }

        template <typename ForwardIterator>
        void calibrate(ForwardIterator begin, ForwardIterator end,
                       OptimizationMethod& method,
                       EndCriteria endCriteria,
                       const Array& initialGuess) {
            std::vector<Volatility> r2;
            to_r2(begin, end, r2);
            ext::shared_ptr<Problem> p =
                calibrate_r2(r2, method, endCriteria, initialGuess,
                             alpha_, beta_, vl_);
            gamma_ = 1 - alpha_ - beta_;
            vl_ /= gamma_;
            logLikelihood_ = p ? -p->functionValue() :
                                 -costFunction(begin, end);
        }

        Real forecast(Real r, Real sigma2) const {
            return gamma_* vl_ + alpha_ * r * r + beta_ * sigma2;
        }

        // a helper for calculation of r^2 and <r^2>
        template <typename InputIterator>
        static Real to_r2(InputIterator begin, InputIterator end,
                          std::vector<Volatility>& r2) {
            Real u2(0.0), mean_r2(0.0), w(1.0);
            for (; begin != end; ++begin) {
                u2 = *begin; u2 *= u2;
                mean_r2 = (1.0 - w) * mean_r2 + w * u2;
                r2.push_back(u2);
                w /= (w + 1.0);
            }
            return mean_r2;
        }

        /*! calibrates GARCH for r^2 */
        static ext::shared_ptr<Problem> calibrate_r2(
                                        Mode mode,
                                        const std::vector<Volatility>& r2,
                                        Real mean_r2,
                                        Real& alpha,
                                        Real& beta,
                                        Real& omega);

        /*! calibrates GARCH for r^2 with user-defined optimization
            method and end criteria */
        static ext::shared_ptr<Problem> calibrate_r2(
                                        Mode mode,
                                        const std::vector<Volatility>& r2,
                                        Real mean_r2,
                                        OptimizationMethod& method,
                                        const EndCriteria& endCriteria,
                                        Real& alpha,
                                        Real& beta,
                                        Real& omega);

        /*! calibrates GARCH for r^2 with user-defined optimization
            method, end criteria and initial guess */
        static ext::shared_ptr<Problem> calibrate_r2(
                                        const std::vector<Volatility>& r2,
                                        Real mean_r2,
                                      