  OptimizationMethod& method,
                                        const EndCriteria& endCriteria,
                                        const Array& initialGuess,
                                        Real& alpha,
                                        Real& beta,
                                        Real& omega);

        /*! calibrates GARCH for r^2 with user-defined optimization
            method, end criteria and initial guess */
        static ext::shared_ptr<Problem> calibrate_r2(
                                        const std::vector<Volatility> &r2,
                                        OptimizationMethod& method,
                                        const EndCriteria& endCriteria,
                                        const Array& initialGuess,
                                        Real& alpha,
                                        Real& beta,
                                        Real& omega);

        /*! calibrates GARCH for r^2 with user-defined optimization
            method, end criteria, constraints and initial guess */
        static ext::shared_ptr<Problem> calibrate_r2(
                                        const std::vector<Volatility>& r2,
                                        Real mean_r2,
                                        OptimizationMethod& method,
                                        Constraint& constraints,
                                        const EndCriteria& endCriteria,
                                        const Array& initialGuess,
                                        Real& alpha,
                                        Real& beta,
                                        Real& omega);

        static ext::shared_ptr<Problem> calibrate_r2(
                                        const std::vector<Volatility> &r2,
                                        OptimizationMethod& method,
                                        Constraint& constraints,
                                        const EndCriteria& endCriteria,
                                        const Array& initialGuess,
                                        Real& alpha,
                                        Real& beta,
                                        Real& omega);

        template<class InputIterator>
        static Real costFunction(InputIterator begin, InputIterator end,
                                 Real alpha, Real beta, Real omega) {
            Real retval(0.0);
            Real u2(0.0), sigma2(0.0);
            Size N = 0;
            for (; begin != end; ++begin, ++N) {
                sigma2 = omega + alpha * u2 + beta * sigma2;
                u2 = *begin; u2 *= u2;
                retval += std::log(sigma2) + u2 / sigma2;
            }
            return N > 0 ? Real(retval / (2*N)) : 0.0;
        }
        //@}
      private:
        Real alpha_, beta_, gamma_, vl_;
        Real logLikelihood_;
        Mode mode_;

        template<class InputIterator>
        Real costFunction(InputIterator begin, InputIterator end) const {
            return costFunction(begin, end, alpha(), beta(), omega());
        }
    };

}


#endif
