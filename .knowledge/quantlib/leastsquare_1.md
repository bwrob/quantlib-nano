                            Size maxiter,
                             ext::shared_ptr<OptimizationMethod> om);
        //! Destructor
        ~NonLinearLeastSquare() = default;

        //! Solve least square problem using numerix solver
        Array& perform(LeastSquareProblem& lsProblem);

        void setInitialValue(const Array& initialValue) {
            initialValue_ = initialValue;
        }

        //! return the results
        Array& results() { return results_; }

        //! return the least square residual norm
        Real residualNorm() const { return resnorm_; }

        //! return last function value
        Real lastValue() const { return bestAccuracy_; }

        //! return exit flag
        Integer exitFlag() const { return exitFlag_; }

        //! return the performed number of iterations
        Integer iterationsNumber() const { return nbIterations_; }

      private:
        //! solution vector
        Array results_, initialValue_;
        //! least square residual norm
        Real resnorm_;
        //! Exit flag of the optimization process
        Integer exitFlag_;
        //! required accuracy of the solver
        Real accuracy_, bestAccuracy_;
        //! maximum and real number of iterations
        Size maxIterations_, nbIterations_;
        //! Optimization method
        ext::shared_ptr<OptimizationMethod> om_;
        //constraint
        Constraint& c_;

    };

}

#endif