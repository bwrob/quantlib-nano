
        // assuming I have the tranched one.
        Real lossPerc = percentile(d, percProb);

        // check the trivial case when the loss is over the detachment limit
        //   to avoid computation:
        Real trancheAmount = basket_->trancheNotional() *
            (detachRatio_-attachRatio_);
        //assumed the amount includes the realized loses
        if(lossPerc >= trancheAmount) return trancheAmount;
        //SHOULD CHECK NOW THE OPPOSITE LIMIT ("zero" losses)....
        std::vector<Real> invUncondProbs =
            basket_->remainingProbabilities(d);
        for(Size i=0; i<invUncondProbs.size(); i++)
            invUncondProbs[i] =
                copula_->inverseCumulativeY(invUncondProbs[i], i);

        // Integrate with the tranche or the portfolio according to the limits.
        return copula_->integratedExpectedValue(
            [&](const std::vector<Real>& v1) {
                return expectedShortfallFullPortfolioCond(invUncondProbs, lossPerc, v1);
            }) / (1.-percProb);

    /* test:?
        return std::inner_product(integrESFPartition.begin(),
        integrESFPartition.end(), remainingNotionals_.begin(), 0.);
    */

    }



}

#endif
