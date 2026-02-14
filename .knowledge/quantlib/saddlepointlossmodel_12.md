lityInvP(
                    invUncondProbs[iName], iName, mktFactor);
            Real lossInDef = remainingNotionals_[iName] * 
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName], 
                    iName, mktFactor));
            Real midFactor = pBuffer * 
                std::exp(lossInDef * saddlePt/ remainingNotional_);
            Real denominator = 1.-pBuffer + midFactor;

            condContrib[iName] = lossInDef * midFactor / denominator; 
        }
        return condContrib;
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::conditionalExpectedLoss(
        const std::vector<Real>& invUncondProbs,
        const std::vector<Real>& mktFactor) const 
    {
        const Size nNames = remainingNotionals_.size();
        Real eloss = 0.;
        /// USE STL.....-------------------
        for(Size iName=0; iName < nNames; iName++) {
            Probability pBuffer = copula_->conditionalDefaultProbabilityInvP(
                invUncondProbs[iName], iName, mktFactor);
            eloss += pBuffer * remainingNotionals_[iName] *
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName], 
                    iName, mktFactor));
        }
        return eloss;
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::conditionalExpectedTrancheLoss(
        const std::vector<Real>& invUncondProbs,
        const std::vector<Real>& mktFactor) const 
    {
        const Size nNames = remainingNotionals_.size();
        Real eloss = 0.;
        /// USE STL.....-------------------
        for(Size iName=0; iName < nNames; iName++) {
            Probability pBuffer = copula_->conditionalDefaultProbabilityInvP(
                invUncondProbs[iName], iName, mktFactor);
            eloss += 
                pBuffer * remainingNotionals_[iName] * 
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName], 
                iName, mktFactor));
        }
        return std::min(
            std::max(eloss - attachRatio_ * remainingNotional_, 0.), 
                (detachRatio_ - attachRatio_) * remainingNotional_);
    }

    template<class CP>
    std::vector<Real> SaddlePointLossModel<CP>::expectedShortfallSplitCond(
            const std::vector<Real>& invUncondProbs,
            Real lossPerc, const std::vector<Real>& mktFactor) const 
    {
        const Size nNames = remainingNotionals_.size();
        std::vector<Real> lgds;
        for(Size iName=0; iName<nNames; iName++)
            lgds.push_back(remainingNotionals_[iName] * 
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName],
                    iName, mktFactor))); 
        std::vector<Real> vola(nNames, 0.), mu(nNames, 0.);
        Real volaTot = 0., muTot = 0.;
        for(Size iName=0; iName < nNames; iName++) {
            Probability pBuffer = copula_->conditionalDefaultProbabilityInvP(
                invUncondProbs[iName], iName, mktFactor);
            mu[iName] = lgds[iName] * pBuffer / remainingNotionals_[iName];
            muTot += lgds[iName] * pBuffer;
            vola[iName] = lgds[iName] * lgds[iName] * pBuffer * (1.-pBuffer) 
                / remainingNotionals_[iName];
            volaTot += lgds[iName] * lgds[iName] * pBuffer * (1.-pBuffer) ;
        }
        for (Size iName=0; iName < nNames; iName++)
            vola[iName] = vola[iName] / volaTot;

        std::vector<Real> esfPartition(nNames, 0.);
        for(Size iName=0; iName < nNames; iName++) {
            Real uEdisp = (lossPerc-muTot)/std::sqrt(volaTot);
            esfPartition[iName] = mu[iName]
                * CumulativeNormalDistribution()(uEdisp) // static call?
                + vola[iName] * NormalDistribution()(uEdisp);
        }
        return esfPartition;
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::expectedShortfallTrancheCond(
        const std::vector<Real>& invUncondProbs,
        Real lossPerc, // value 
        Probability percentile,
        const st