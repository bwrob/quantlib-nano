1.-crossIdiosyncFctrs_[iName]))
            // cache the sqrts
            // cache this factor.
            +std::sqrt(1.+ 1./(modelA_*modelA_)) *
                inverseCumulativeY(recoveries_[iName], iRecovery)
            , iRecovery);
    }

    template<class CP>
    inline Real SpotRecoveryLatentModel<CP>::latentRRVarValue(
        const std::vector<Real>& allFactors,
        Size iName) const
    {
        Size iRecovery = iName + numNames_;// should be live pool
        return latentVarValue(allFactors, iRecovery);
    }

    template<class CP>
    inline Real SpotRecoveryLatentModel<CP>::conditionalExpLossRR(const Date& d,
        Size iName,
        const std::vector<Real>& mktFactors) const
    {
        const ext::shared_ptr<Pool>& pool = basket_->pool();
        Probability pDefUncond =
            pool->get(pool->names()[iName]).
            defaultProbability(basket_->defaultKeys()[iName])
              ->defaultProbability(d);

        Real invP = inverseCumulativeY(pDefUncond, iName);
        Real invRR = inverseCumulativeY(recoveries_[iName], iName + numNames_);

        return conditionalExpLossRRInv(invP, invRR, iName, mktFactors);
    }

    template<class CP>
    inline Real SpotRecoveryLatentModel<CP>::conditionalExpLossRRInv(
        Real invP,
        Real invRR,
        Size iName,
        const std::vector<Real>& mktFactors) const
    {
        return conditionalDefaultProbabilityInvP(invP, iName, mktFactors)
            * (1.-this->conditionalRecoveryInvPinvRR(invP, invRR, iName, mktFactors));
    }

    template<class CP>
    inline Real SpotRecoveryLatentModel<CP>::expectedLoss(const Date& d,
        Size iName) const
    {
        const ext::shared_ptr<Pool>& pool = basket_->pool();
        Probability pDefUncond =
            pool->get(pool->names()[iName]).
            defaultProbability(basket_->defaultKeys()[iName])
              ->defaultProbability(d);

        Real invP = inverseCumulativeY(pDefUncond, iName);
        Real invRR = inverseCumulativeY(recoveries_[iName], iName + numNames_);

        return integratedExpectedValue(
            [&](const std::vector<Real>& v){
                return conditionalExpLossRRInv(invP, invRR, iName, v);
            });
    }

    template<class CP>
    SpotRecoveryLatentModel<CP>::SpotRecoveryLatentModel(
        const std::vector<std::vector<Real> >& factorWeights,
        const std::vector<Real>& recoveries,
        Real modelA,
        LatentModelIntegrationType::LatentModelIntegrationType integralType,
        const typename CP::initTraits& ini
        )
    : LatentModel<CP>(factorWeights, ini),
      recoveries_(recoveries),
      modelA_(modelA),
      numNames_(factorWeights.size()/2),
      integration_(LatentModel<CP>::IntegrationFactory::
        createLMIntegration(factorWeights[0].size(), integralType))
    {
        QL_REQUIRE(factorWeights.size() % 2 == 0,
         "Number of RR variables must be equal to number of default variables");
        QL_REQUIRE(recoveries.size() == numNames_ ,
         "Number of recoveries does not match number of defaultable entities.");

        // reminder: first betas are default, last ones are recovery
        for(Size iName=0; iName<numNames_; iName++) /// USE STL
            /* Corresponds to: (k denotes factor, i denotes modelled
                variable -default and recoveries))
                \sum_k a^2_{i,k} a^2_{N+i,k}
            */
        {
            Real cumul = Real(0.);
            for(Size iB=0; iB<factorWeights[iName].size(); iB++)
                // actually this size is unique
                cumul += factorWeights[iName][iB] *
                    factorWeights[iName][iB] *
                    factorWeights[iName + numNames_][iB] *
                    factorWeights[iName + numNames_][iB];
            crossIdiosyncFctrs_.push_back(cumul);
        }

    }


}

#endif
