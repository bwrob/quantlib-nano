+= (suma3 + (2.*std::pow(suma1, 3.)/suma0 -
                3.*suma1*suma2)/suma0)/suma0;
        }
       return sum;
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::CumGen4thDerivativeCond(
        const std::vector<Real>& invUncondProbs,
        Real saddle,
        const std::vector<Real>&  mktFactor) const
    {
        const Size nNames = remainingNotionals_.size();
        Real sum = 0.;

        for(Size iName=0; iName < nNames; iName++) {
            Probability pBuffer =
                copula_->conditionalDefaultProbabilityInvP(
                    invUncondProbs[iName], iName, mktFactor);
            Real lossInDef = remainingNotionals_[iName] *
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName],
                    iName, mktFactor)) / remainingNotional_;

            Real midFactor = pBuffer * std::exp(lossInDef * saddle);
            Real denominator = 1.-pBuffer + midFactor;

            const Real& suma0 = denominator;
            const Real suma1  = lossInDef * midFactor;
            const Real suma2  = lossInDef * suma1;
            const Real suma3  = lossInDef * suma2;
            const Real suma4  = lossInDef * suma3;

            sum += (suma4 + (-4.*suma1*suma3 - 3.*suma2*suma2 +
                (12.*suma1*suma1*suma2 -
                    6.*std::pow(suma1,4.)/suma0)/suma0)/suma0)/suma0;
        }
       return sum;
    }

    template<class CP>
    std::tuple<Real, Real, Real, Real> SaddlePointLossModel<CP>::CumGen0234DerivCond(
        const std::vector<Real>& invUncondProbs,
        Real saddle,
        const std::vector<Real>&  mktFactor) const
    {
        const Size nNames = remainingNotionals_.size();
        Real deriv0 = 0.,
             //deriv1 = 0.,
             deriv2 = 0.,
             deriv3 = 0.,
             deriv4 = 0.;
        for(Size iName=0; iName < nNames; iName++) {
            Probability pBuffer =
                copula_->conditionalDefaultProbabilityInvP(
                    invUncondProbs[iName], iName, mktFactor);
            Real lossInDef = remainingNotionals_[iName] *
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName],
                    iName, mktFactor)) / remainingNotional_;

            Real midFactor = pBuffer * std::exp(lossInDef * saddle);
            Real denominator = 1.-pBuffer + midFactor;

            const Real& suma0 = denominator;
            const Real suma1  = lossInDef * midFactor;
            const Real suma2  = lossInDef * suma1;
            const Real suma3  = lossInDef * suma2;
            const Real suma4  = lossInDef * suma3;

            // To do: optimize these:
            deriv0 += std::log(suma0);
            //deriv1 += suma1 / suma0;
            deriv2 += suma2 / suma0 - std::pow(suma1 / suma0 , 2.);
            deriv3 += (suma3 + (2.*std::pow(suma1, 3.)/suma0 -
                3.*suma1*suma2)/suma0)/suma0;
            deriv4 += (suma4 + (-4.*suma1*suma3 - 3.*suma2*suma2 +
                (12.*suma1*suma1*suma2 -
                    6.*std::pow(suma1,4.)/suma0)/suma0)/suma0)/suma0;
        }
        return {deriv0, deriv2, deriv3, deriv4};
    }

    template<class CP>
    std::tuple<Real, Real> SaddlePointLossModel<CP>::CumGen02DerivCond(
        const std::vector<Real>& invUncondProbs,
        Real saddle,
        const std::vector<Real>&  mktFactor) const
    {
        const Size nNames = remainingNotionals_.size();
        Real deriv0 = 0.,
             //deriv1 = 0.,
             deriv2 = 0.;
        for(Size iName=0; iName < nNames; iName++) {
            Probability pBuffer =
                copula_->conditionalDefaultProbabilityInvP(
                    invUncondProbs[iName], iName, mktFactor);
            Real lossInDef = remainingNotionals_[iName] *
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName],
                    iName, mktFactor)) / remainingNotional_;

            Real midFactor = pBuffer * std::exp(lossInDef *
