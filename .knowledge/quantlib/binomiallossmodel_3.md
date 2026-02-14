urning for all i's:
            \frac{\int_0^t  [1-rr_i(\tau; \xi)] P_{def-i}(0, \tau; \xi) d\tau}
                 {P_{def-i}(0,t;\xi)}
            and the constant recovery model is simply returning: 
            1-RR_i
        */
        std::vector<Real> fractionalEL = expConditionalLgd(d, mktFctrs);
        Real notBskt = std::accumulate(reminingNots.begin(), 
                                       reminingNots.end(), Real(0.));
        std::vector<Real> lgdsLeft;
        std::transform(fractionalEL.begin(), fractionalEL.end(), 
                       reminingNots.begin(), std::back_inserter(lgdsLeft),
                       std::multiplies<>());
        return std::accumulate(lgdsLeft.begin(), lgdsLeft.end(), Real(0.)) 
            / (bsktSize*notBskt);
    }

    template< class LLM>
    std::vector<Real> BinomialLossModel<LLM>::lossPoints(const Date& d) const 
    {
        std::vector<Real> notionals = basket_->remainingNotionals(d);

        Real aveLossFrct = copula_->integratedExpectedValue(
            [&](const std::vector<Real>& v1) {
                return averageLoss(d, notionals, v1);
            });

        std::vector<Real> data;
        Size dataSize = basket_->remainingSize() + 1;
        data.reserve(dataSize);
        // use std::algorithm
        Real outsNot = basket_->remainingNotional(d);
        for(Size i=0; i<dataSize; i++)
            data.push_back(i * aveLossFrct * outsNot);
        return data;
    }

    template< class LLM>
    Real BinomialLossModel<LLM>::condTrancheLoss(
        const Date& d, 
        const std::vector<Real>& lossVals, 
        const std::vector<Real>& bsktNots,
        const std::vector<Real>& uncondDefProbsInv,
        const std::vector<Real>& mkf) const {

        std::vector<Real> condLProb = 
            lossProbability(d, bsktNots, uncondDefProbsInv, mkf);
        // \to do: move to a do-while over attach to detach
        Real suma = 0.;
        for(Size i=0; i<lossVals.size(); i++) { 
            suma += condLProb[i] * 
                std::min(std::max(lossVals[i]
                 - attachAmount_, 0.), detachAmount_ - attachAmount_);
        }
        return suma;
    }

    template< class LLM>
    Real BinomialLossModel<LLM>::expectedTrancheLoss(const Date& d) const {
        std::vector<Real> lossVals  = lossPoints(d);
        std::vector<Real> notionals = basket_->remainingNotionals(d);
        std::vector<Probability> invProbs = 
            basket_->remainingProbabilities(d);
        for(Size iName=0; iName<invProbs.size(); iName++)
            invProbs[iName] = 
                copula_->inverseCumulativeY(invProbs[iName], iName);
            
        return copula_->integratedExpectedValue(
            [&](const std::vector<Real>& v1) {
                return condTrancheLoss(d, lossVals, notionals, invProbs, v1);
            });
    }


    template< class LLM>
    std::map<Real, Probability> BinomialLossModel<LLM>::lossDistribution(const Date& d) const 
    {
        std::map<Real, Probability> distrib;
        std::vector<Real> lossPts = lossPoints(d);
        std::vector<Real> values  = expectedDistribution(d);
        Real sum = 0.;
        for(Size i=0; i<lossPts.size(); i++) {
            distrib.insert(std::make_pair(lossPts[i], 
                //capped, some situations giving a very small probability over 1
                std::min(sum+values[i],1.)
                ));
            sum+= values[i];
        }
        return distrib;
    }

    template< class LLM>
    Real BinomialLossModel<LLM>::percentile(const Date& d, Real perc) const {
        std::map<Real, Probability> dist = lossDistribution(d);
        // \todo: Use some of the library interpolators instead
        if(// included in test below-> (dist.begin()->second >=1.) ||
            (dist.begin()->second >= perc))return dist.begin()->first;

        // deterministic case (e.g. date requested is todays date)
        if(dist.size() == 1) return dist.begin()->first;

        if(perc == 