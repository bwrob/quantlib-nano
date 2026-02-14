Probs,
            const std::vector<Real>& mktFactor) const;

        void resetModel() override {
            remainingNotionals_ = basket_->remainingNotionals();
            remainingNotional_  = basket_->remainingNotional();
            attachRatio_ = std::min(basket_->remainingAttachmentAmount()
                / basket_->remainingNotional(), 1.);
            detachRatio_ = std::min(basket_->remainingDetachmentAmount()
                / basket_->remainingNotional(), 1.);
            copula_->resetBasket(basket_.currentLink());
        }

        const ext::shared_ptr<ConstantLossLatentmodel<CP> > copula_;
        // cached todays arguments values
        mutable Size remainingSize_;
        mutable std::vector<Real> remainingNotionals_;
        mutable Real remainingNotional_;
        // remaining basket levels:
        mutable Real attachRatio_, detachRatio_;
        /*
        // Just for testing the ESF direct integration, not for release,
        //   this is very inneficient:
        class ESFIntegrator {
        public:
            ESFIntegrator(const SaddlePointLossModel& me,
                const Date& date,
                Real lossPercentileFract//,
                //const std::vector<Real>& mktFactor
                )
                : me_(me), date_(date),lossPercentileFract_(lossPercentileFract)
            {}


            Real operator()(Real x) const {
                return me_.densityTrancheLoss(date_, x + lossPercentileFract_)
                    * (x + lossPercentileFract_);
            }

            Real lossPercentileFract_;
            Date date_;
            //  const std::vector<Real>& mktFactor_;
            const SaddlePointLossModel& me_;
        };
        */
    };


    // -- Inlined integrations------------------------------------------------

    // Unconditional Moments and derivatives. --------------------------------
    template<class CP>
    inline Real SaddlePointLossModel<CP>::CumulantGenerating(
        const Date& date, Real s) const
    {
        std::vector<Real> invUncondProbs =
            basket_->remainingProbabilities(date);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] =
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedExpectedValue(
            [&](const std::vector<Real>& v1) {
                return CumulantGeneratingCond(invUncondProbs, s, v1);
            });
    }

    template<class CP>
    inline Real SaddlePointLossModel<CP>::CumGen1stDerivative(
        const Date& date, Real s) const
    {
        std::vector<Real> invUncondProbs =
            basket_->remainingProbabilities(date);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] =
            copula_->inverseCumulativeY(invUncondProbs[i], i);

       return copula_->integratedExpectedValue(
           [&](const std::vector<Real>& v1) {
               return CumGen1stDerivativeCond(invUncondProbs, s, v1);
           });
    }

    template<class CP>
    inline Real SaddlePointLossModel<CP>::CumGen2ndDerivative(
        const Date& date, Real s) const
    {
        std::vector<Real> invUncondProbs =
            basket_->remainingProbabilities(date);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] =
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedExpectedValue(
           [&](const std::vector<Real>& v1) {
               return CumGen2ndDerivativeCond(invUncondProbs, s, v1);
           });
    }

    template<class CP>
    inline Real SaddlePointLossModel<CP>::CumGen3rdDerivative(
        const Date& date, Real s) const
    {
        std::vector<Real> invUncondProbs =
            basket_->remainingProbabilities(date);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] =
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedEx
