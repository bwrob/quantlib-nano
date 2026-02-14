 and expensive to perform the call to the probabilities in
        these methods since they are integrands.
       ---------------------------------------------------------------------- */

    template<class CP>
    Real SaddlePointLossModel<CP>::CumulantGeneratingCond(
        const std::vector<Real>& invUncondProbs,
        Real lossFraction,
        const std::vector<Real>&  mktFactor) const
    {
        const Size nNames = remainingNotionals_.size();
        Real sum = 0.;

        for(Size iName=0; iName < nNames; iName++) {
            Probability pBuffer =
                copula_->conditionalDefaultProbabilityInvP(
                    invUncondProbs[iName], iName, mktFactor);
            sum += std::log(1. - pBuffer +
                pBuffer * std::exp(remainingNotionals_[iName] *
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName],
                    iName, mktFactor)) * lossFraction / remainingNotional_));
        }
       return sum;
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::CumGen1stDerivativeCond(
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
            // loss in fractional units
            Real lossInDef = remainingNotionals_[iName] *
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName],
                    iName, mktFactor)) / remainingNotional_;
            Real midFactor = pBuffer * std::exp(lossInDef * saddle);
            sum += lossInDef * midFactor / (1.-pBuffer + midFactor);
        }
       return sum;
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::CumGen2ndDerivativeCond(
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
            // loss in fractional units
            Real lossInDef = remainingNotionals_[iName] *
                (1.-copula_->conditionalRecoveryInvP(invUncondProbs[iName],
                    iName, mktFactor)) / remainingNotional_;
            Real midFactor = pBuffer * std::exp(lossInDef * saddle);
            Real denominator = 1.-pBuffer + midFactor;
            sum += lossInDef * lossInDef * midFactor / denominator -
                std::pow(lossInDef * midFactor / denominator , 2.);
        }
       return sum;
    }

    template<class CP>
    Real SaddlePointLossModel<CP>::CumGen3rdDerivativeCond(
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

            const Real midFactor = pBuffer * std::exp(lossInDef * saddle);
            const Real denominator = 1.-pBuffer + midFactor;

            const Real& suma0 = denominator;
            const Real suma1  = lossInDef * midFactor;
            const Real suma2  = lossInDef * suma1;
            const Real suma3  = lossInDef * suma2;

            sum
