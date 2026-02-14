:vector<Real>&  mktFactor) const;

        /* Unconditional cumulants. Because this class integrates the various
          statistics it provides in indirect mode they are never used. 
          Provided for completeness/extendability */
        /*! Returns the cumulant generating function (zero-th order expansion
          term) weighting the conditional value by the prob density of the 
          market factor, called by integrations */
        Real CumulantGenerating(const Date& date, Real s) const;
        Real CumGen1stDerivative(const Date& date, Real s) const;
        Real CumGen2ndDerivative(const Date& date, Real s) const;
        Real CumGen3rdDerivative(const Date& date, Real s) const;
        Real CumGen4thDerivative(const Date& date, Real s) const;
        
        // -------- Saddle point search functions ---------------------------
        class SaddleObjectiveFunction {
            const SaddlePointLossModel& me_;
            Real targetValue_;
            const std::vector<Real>& mktFactor_;
            const std::vector<Real>& invUncondProbs_;
        public:
            //! The passed target is in fractional loss units
            SaddleObjectiveFunction(const SaddlePointLossModel& me,
                                    const Real target,
                                    const std::vector<Real>& invUncondProbs,
                                    const std::vector<Real>& mktFactor
                                    )
            : me_(me), 
              targetValue_(target), 
              mktFactor_(mktFactor), 
              invUncondProbs_(invUncondProbs)
            {}
            Real operator()(const Real x) const {
                return me_.CumGen1stDerivativeCond(invUncondProbs_, x, 
                    mktFactor_) - targetValue_;
            }
            Real derivative(Real x) const {
                return me_.CumGen2ndDerivativeCond(invUncondProbs_, x, 
                    mktFactor_);
            }
        };

        /*! Calculates the mkt-fct-conditional saddle point for the loss level 
            given and the probability passed. 
            The date is implicitly given through the probability. Performance 
            requires to pass the probabilities for that date. Otherwise once we
            integrate this over the market factor we would be computing the same
            probabilities over and over. While this works fine here some models
            of the recovery rate might require the date.

            The passed lossLevel is in total portfolio loss fractional units.

            \todo Improve convergence speed (which is bad at the moment).See 
            discussion in several places; references above and The Oxford 
            Handbook of CD, sect 2.9
        */
        Real findSaddle(
            const std::vector<Real>& invUncondProbs,
            Real lossLevel,
            const std::vector<Real>& mktFactor, 
            Real accuracy = 1.0e-3,//1.e-4
            Natural maxEvaluations = 50
            ) const;

        class SaddlePercObjFunction {
            const SaddlePointLossModel& me_;
            Real targetValue_;
            Date date_;
        public:
            SaddlePercObjFunction(
                const SaddlePointLossModel& me,
                const Real target,
                const Date& date)
            : me_(me), targetValue_(1.-target), date_(date) {}
            /*! The passed x is the _tranche_ loss fraction */
            Real operator()(const Real x) const {
                return me_.probOverLoss(date_, x) - targetValue_;
            }
        };
        // Functionality, Provides various portfolio statistics---------------
    public:
        /*! Returns the loss amount at the requested date for which the 
        probability of lossing that amount or less is equal to the value passed.
        */
      Real percentile(const Date& d, Probability percentile) const override;

    protected:
        /*! Conditional (on the mkt factor) prob 