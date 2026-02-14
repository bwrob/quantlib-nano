> copula_;
        Size nBuckets_;
        mutable Real attach_, detach_, notional_, attachAmount_, detachAmount_;
        mutable std::vector<Real> notionals_;
    private:
        // integration:
        //  \todo move integration to latent model types when moving to a
        //  multifactor version
        const Real max_;// redundant?
        const Real min_;
        const Size nSteps_;
        const Real delta_;
    };
    // \todo Add other loss distribution statistics
    typedef InhomogeneousPoolLossModel<GaussianCopulaPolicy>
        IHGaussPoolLossModel;
    typedef InhomogeneousPoolLossModel<TCopulaPolicy> IHStudentPoolLossModel;

    //-----------------------------------------------------------------------

    template<class CP>
    void InhomogeneousPoolLossModel<CP>::resetModel()
    {
        // need to be capped now since the limit amounts might be over the
        //  remaining notional (think amortizing)
        attach_ = std::min(basket_->remainingAttachmentAmount() /
            basket_->remainingNotional(), 1.);
        detach_ = std::min(basket_->remainingDetachmentAmount() /
            basket_->remainingNotional(), 1.);
        notional_ = basket_->remainingNotional();
        notionals_ = basket_->remainingNotionals();
        attachAmount_ = basket_->remainingAttachmentAmount();
        detachAmount_ = basket_->remainingDetachmentAmount();

        copula_->resetBasket(basket_.currentLink());
    }

    template<class CP>
    Distribution InhomogeneousPoolLossModel<CP>::lossDistrib(
        const Date& d) const
    {
        LossDistBucketing bucktLDistBuff(nBuckets_, detachAmount_);

        std::vector<Real> lgd;// switch to a mutable cache member
        std::vector<Real> recoveries = copula_->recoveries();
        std::transform(recoveries.begin(), recoveries.end(),
                       std::back_inserter(lgd),
                       [](Real x) -> Real { return 1.0-x; });
        std::transform(lgd.begin(), lgd.end(), notionals_.begin(),
                       lgd.begin(), std::multiplies<>());
        std::vector<Real> prob = basket_->remainingProbabilities(d);
        for(Size iName=0; iName<prob.size(); iName++)
            prob[iName] = copula_->inverseCumulativeY(prob[iName], iName);

        // integrate locally (1 factor).
        // use explicitly a 1D latent model object?
        // \todo Use a library integrator here and in the homogeneous case.
        Distribution dist(nBuckets_, 0.0,
            detachAmount_);
            //notional_);
        std::vector<Real> mkft(1, min_ + delta_ /2.);
        for (Size i = 0; i < nSteps_; i++) {
            std::vector<Real> conditionalProbs;
            conditionalProbs.reserve(notionals_.size());
            for(Size iName=0; iName<notionals_.size(); iName++)
                conditionalProbs.push_back(
                copula_->conditionalDefaultProbabilityInvP(prob[iName], iName,
                    mkft));
            Distribution bld = bucktLDistBuff(lgd, conditionalProbs);
            Real densitydm = delta_ * copula_->density(mkft);
            // also, instead of calling the static method it could be wrapped
            // through an inlined call in the latent model
            for (Size j = 0; j < nBuckets_; j++)
                dist.addDensity(j, bld.density(j) * densitydm);
            mkft[0] += delta_;
        }
        return dist;
    }


}

#endif
