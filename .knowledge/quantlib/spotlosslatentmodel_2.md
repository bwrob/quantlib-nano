,
        and this independently of the copula function.
        */
        if (prob < 1.e-10) return 0.;// use library macro...
        return conditionalDefaultProbabilityInvP(
            inverseCumulativeY(prob, iName), iName, mktFactors);
    }

    template<class CP>
    inline Probability
        SpotRecoveryLatentModel<CP>::conditionalDefaultProbabilityInvP(
        Real invCumYProb,
        Size iName,
        const std::vector<Real>& m) const
    {
        Real sumMs =
            std::inner_product(this->factorWeights_[iName].begin(),
                               this->factorWeights_[iName].end(), m.begin(), Real(0.));
        Real res = this->cumulativeZ((invCumYProb - sumMs) /
                this->idiosyncFctrs_[iName] );
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE (res >= 0. && res <= 1.,
                    "conditional probability " << res << "out of range");
        #endif

        return res;
    }

    template<class CP>
    inline Real
        SpotRecoveryLatentModel<CP>::expCondRecovery(const Date& d,
        Size iName,
        const std::vector<Real>& mktFactors) const
    {
    #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(mktFactors.size() == this->numFactors(),
        "Realization of market factors and latent model size do not match");
    #endif
        const ext::shared_ptr<Pool>& pool = basket_->pool();
        Probability pDefUncond =
            pool->get(pool->names()[iName]).
            defaultProbability(basket_->defaultKeys()[iName])
              ->defaultProbability(d);

        return expCondRecoveryP(pDefUncond, iName, mktFactors);
    }

    template<class CP>
    inline Real SpotRecoveryLatentModel<CP>::expCondRecoveryP(
        Real uncondDefP, Size iName, const std::vector<Real>& mktFactors) const
    {
        return expCondRecoveryInvPinvRR(
            inverseCumulativeY(uncondDefP, iName),
            inverseCumulativeY(recoveries_[iName], iName + numNames_),
            iName, mktFactors);
    }

    template<class CP>
    Real SpotRecoveryLatentModel<CP>::expCondRecoveryInvPinvRR(
        Real invUncondDefP,
        Real invUncondRR,
        Size iName,
        const std::vector<Real>& mktFactors) const
    {
        const std::vector<std::vector<Real> >& fctrs_ = factorWeights();
        //Size iRR = iName + basket_->size();// should be live pool
        const Real sumMs =
          std::inner_product(fctrs_[iName].begin(), fctrs_[iName].end(),
              mktFactors.begin(), Real(0.));
        const Real sumBetaLoss =
          std::inner_product(fctrs_[iName + numNames_].begin(),
              fctrs_[iName + numNames_].end(),
              fctrs_[iName + numNames_].begin(),
              Real(0.));
        return this->cumulativeZ((sumMs + std::sqrt(1.-crossIdiosyncFctrs_[iName])
                 * std::sqrt(1.+modelA_*modelA_) *
                   invUncondRR
            - std::sqrt(crossIdiosyncFctrs_[iName]) *
                invUncondDefP
                )
            / std::sqrt(1.- sumBetaLoss + modelA_*modelA_ *
                (1.-crossIdiosyncFctrs_[iName])) );
    }

    template<class CP>
    Real SpotRecoveryLatentModel<CP>::conditionalRecovery(Real latentVarSample,
        Size iName, const Date& d) const
    {
        const ext::shared_ptr<Pool>& pool = basket_->pool();

        // retrieve the default probability for this name
        const Handle<DefaultProbabilityTermStructure>& dfts =
            pool->get(basket_->names()[iName]).defaultProbability(
                basket_->defaultKeys()[iName]);
        const Probability pdef = dfts->defaultProbability(d, true);
        // before asking for -\infty
        if (pdef < 1.e-10) return Real(0.);

        Size iRecovery = iName + numNames_;// should be live pool
        return cumulativeY(
            (latentVarSample - std::sqrt(crossIdiosyncFctrs_[iName])
                * inverseCumulativeY(pdef, iName)) /
                (modelA_ * std::sqrt(
