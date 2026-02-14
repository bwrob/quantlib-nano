pectedValue(
           [&](const std::vector<Real>& v1) {
               return CumGen3rdDerivativeCond(invUncondProbs, s, v1);
           });
    }

    template<class CP>
    inline Real SaddlePointLossModel<CP>::CumGen4thDerivative(
        const Date& date, Real s) const 
    {
        std::vector<Real> invUncondProbs = 
            basket_->remainingProbabilities(date);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] = 
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedExpectedValue(
           [&](const std::vector<Real>& v1) {
               return CumGen4thDerivativeCond(invUncondProbs, s, v1);
           });
    }

    template<class CP>
    inline Probability SaddlePointLossModel<CP>::probOverLoss(
        const Date& d, Real trancheLossFract) const 
    {
        // avoid computation:
        if (trancheLossFract >= 
            // time dependent soon:
            basket_->detachmentAmount()) return 0.;

        std::vector<Real> invUncondProbs = 
            basket_->remainingProbabilities(d);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] = 
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedExpectedValue(
           [&](const std::vector<Real>& v1) {
               return probOverLossCond(invUncondProbs, trancheLossFract, v1);
           });
    }

    template<class CP>
    inline Probability SaddlePointLossModel<CP>::probOverPortfLoss(
        const Date& d, Real loss) const 
    {
        std::vector<Probability> invUncondProbs = 
            basket_->remainingProbabilities(d);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] = 
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedExpectedValue(
           [&](const std::vector<Real>& v1) {
               return probOverLossPortfCond(invUncondProbs, loss, v1);
           });
    }

    template<class CP>
    inline Real SaddlePointLossModel<CP>::expectedTrancheLoss(
        const Date& d) const 
    {
        std::vector<Real> invUncondProbs = 
            basket_->remainingProbabilities(d);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] = 
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedExpectedValue(
           [&](const std::vector<Real>& v1) {
               return conditionalExpectedTrancheLoss(invUncondProbs, v1);
           });
    }

    template<class CP>
    inline Probability SaddlePointLossModel<CP>::probDensity(
        const Date& d, Real loss) const 
    {
        std::vector<Real> invUncondProbs = 
            basket_->remainingProbabilities(d);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] = 
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedExpectedValue(
           [&](const std::vector<Real>& v1) {
               return probDensityCond(invUncondProbs, loss, v1);
           });
    }

    template<class CP>
    inline std::vector<Real> SaddlePointLossModel<CP>::splitVaRLevel(const Date& date, Real s) const 
    {
        std::vector<Real> invUncondProbs = 
            basket_->remainingProbabilities(date);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] = 
            copula_->inverseCumulativeY(invUncondProbs[i], i);

        return copula_->integratedExpectedValueV(
           [&](const std::vector<Real>& v1) {
               return splitLossCond(invUncondProbs, s, v1);
           });
    }







    /* ------------------------------------------------------------------------
                    Conditional Moments and derivatives. 

        Notice that in all this methods the date dependence is implicitly
        present in the unconditional probabilities. But, as in other LMs, it
        is redundant