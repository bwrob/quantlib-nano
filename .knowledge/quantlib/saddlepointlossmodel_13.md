d::vector<Real>& mktFactor) const 
    {
        /* TO DO: this is too crude, a general expression valid for all 
        situations is possible (with no extra cost as long as the loss limits 
        are checked).
        */
        //tranche correction term:
        Real correctionTerm = 0.;
        Real probLOver = probOverLossPortfCond(invUncondProbs,
            basket_->detachmentAmount(), mktFactor);
        if(basket_->attachmentAmount() > QL_EPSILON) {
            if(lossPerc < basket_->attachmentAmount()) {
                correctionTerm = ( (basket_->detachmentAmount() 
                    - 2.*basket_->attachmentAmount())*
                        probOverLossPortfCond(invUncondProbs, lossPerc, 
                            mktFactor)
                    + basket_->attachmentAmount() * probLOver )/(1.-percentile);
            }else{
                correctionTerm = ( (percentile-1)*basket_->attachmentAmount()
                    + basket_->detachmentAmount() * probLOver
                    )/(1.-percentile);
            }
        }

        return expectedShortfallFullPortfolioCond(invUncondProbs, 
            std::max(lossPerc, basket_->attachmentAmount()), mktFactor)
            + expectedShortfallFullPortfolioCond(invUncondProbs, 
                basket_->detachmentAmount(), mktFactor)
            - correctionTerm;
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::expectedShortfallFullPortfolioCond(
        const std::vector<Real>& invUncondProbs,
        Real lossPerc, // value 
        const std::vector<Real>& mktFactor) const 
    {
        /* This version is based on: Martin 2006 paper and on the expression 
        in 'SaddlePoint approximation of expected shortfall for transformed 
        means' S.A. Broda and M.S.Paolella , Amsterdam School of Economics 
        discussion paper, available online.
        */
        Real lossPercRatio = lossPerc  /remainingNotional_;
        Real elCond = 0.;
        const Size nNames = remainingNotionals_.size();

        /// use stl algorthms
        for(Size iName=0; iName < nNames; iName++) {
            Probability pBuffer = copula_->conditionalDefaultProbabilityInvP(
                invUncondProbs[iName], iName, mktFactor);
            elCond += pBuffer * remainingNotionals_[iName] * 
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName],
                    iName, mktFactor));
        }
        Real saddlePt = findSaddle(invUncondProbs, lossPercRatio, mktFactor);

        // Martin 2006:
        return 
            elCond * probOverLossPortfCond(invUncondProbs, lossPerc, mktFactor)
              + (lossPerc - elCond) * probDensityCond(invUncondProbs, lossPerc,
                    mktFactor) /saddlePt;

        // calling the EL tranche
        // return elCond - expectedEquityLossCond(d, lossPercRatio, mktFactor);

        /*
        // Broda and Paolella:
        Real elCondRatio = elCond / remainingNotional_;

        std::tuple<Real, Real, Real, Real> cumulants = 
            CumGen0234DerivCond(uncondProbs, 
                saddlePt, mktFactor);
        Real K0Saddle = std::get<0>(cumulants);///USE THEM DIRECTLY
        Real K2Saddle = std::get<1>(cumulants);

        Real wq = std::sqrt(2. * saddlePt * lossPercRatio - 2. * K0Saddle);
        //std::sqrt(-2. * saddlePt * lossPerc + 2. * K0Saddle);????
        Real factor = 1.;
        if(saddlePt<0.) {
            wq = -wq;
            factor = -1.;
        }

        Real numNames = static_cast<Real>(nNames);

        Real term1 = CumulativeNormalDistribution()(wq)// * std::sqrt(numNames)
            * elCond ;
        Real term2 = .5 * M_2_SQRTPI * M_SQRT1_2 * (1./std::sqrt(numNames))
            * exp(-wq*wq * numNames/2.)*(elCond/wq - 
                lossPerc/(saddlePt * std::sqrt(K2Saddle)));
        return term1 + term2;
        */
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::expectedShortfall(const Date&d, 
        Probability percProb) const 
    {