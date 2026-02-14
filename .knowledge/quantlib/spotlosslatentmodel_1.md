remember that \f$\rho_l Z \f$ there is here
        (multiple betas):
        \f$ \sum_k \beta_{ik}^l Z_k \f$ and that \f$ \rho_d \rho_l \f$ there is
        here:
        \f$ \sum_k \beta_{ik}^d \beta_{ik}^l \f$ \par
        (d,l corresponds to first and last set of betas)
        */
        Real expCondRecovery/*conditionalRecovery*/(const Date& d, Size iName,
                                 const std::vector<Real>& mktFactors) const;
        Real expCondRecoveryP(Real uncondDefP, Size iName,
                                 const std::vector<Real>& mktFactors) const;
        Real expCondRecoveryInvPinvRR(Real invUncondDefP, Real invUncondRR,
            Size iName, const std::vector<Real>& mktFactors) const;
        /*! Implements equation 42 on p.14 (second).
            Remember that for this call to make sense the sample used must be
            one leading to a default. Theres no check on this. This member
            typically to be used within a simulation.
        */
        Real conditionalRecovery(Real latentVarSample, Size iName,
            const Date& d) const;
        /*! Due to the way the latent model is splitted in two parts, we call
        the base class for the default sample and the LM owned here for the RR
        model sample. This sample only makes sense if it led to a default.
        @param allFactors All sampled factors, default and RR valiables.
        @param iName The index of the name for which we want the RR sample

        \todo Write vector version for all names' RRs
        */
        Real latentRRVarValue(const std::vector<Real>& allFactors,
            Size iName) const;
        Real conditionalExpLossRR(const Date& d, Size iName,
            const std::vector<Real>& mktFactors) const;
        Real conditionalExpLossRRInv(Real invP, Real invRR, Size iName,
            const std::vector<Real>& mktFactors) const;
        /*! Single name expected loss.\par
        The main reason of this method is for the testing of this model. The
        model is coherent in that it preserves the single name expected loss
        and thus is coherent with the single name CDS market when used in the
        pricing context. i.e. it should match: \f$pdef_i(d) \times RR_i \f$
        */
        Real expectedLoss(const Date& d, Size iName) const;
    };


    typedef SpotRecoveryLatentModel<GaussianCopulaPolicy> GaussianSpotLossLM;
    typedef SpotRecoveryLatentModel<TCopulaPolicy> TSpotLossLM;


    // ------------------------------------------------------------------------

    template <class CP>
    inline void
    SpotRecoveryLatentModel<CP>::resetBasket(const ext::shared_ptr<Basket>& basket) const {
        basket_ = basket;
        // in the future change 'size' to 'liveSize'
        QL_REQUIRE(basket_->size() == numNames_,
            "Incompatible new basket and model sizes.");
    }

    template<class CP>
    inline Probability
        SpotRecoveryLatentModel<CP>::conditionalDefaultProbability(
        const Date& date,
        Size iName, const std::vector<Real>& mktFactors) const
    {
        const ext::shared_ptr<Pool>& pool = basket_->pool();
        Probability pDefUncond =
            pool->get(pool->names()[iName]).
            defaultProbability(basket_->defaultKeys()[iName])
              ->defaultProbability(date);
        return conditionalDefaultProbability(pDefUncond, iName, mktFactors);
    }

    template<class CP>
    inline Probability
        SpotRecoveryLatentModel<CP>::conditionalDefaultProbability(
        Probability prob,
        Size iName, const std::vector<Real>& mktFactors) const
    {
        // we can be called from the outside (from an integrable loss model)
        //   but we are called often at integration points. This or
        //   consider a list of friends.
    #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(basket_, "No portfolio basket set.");
    #endif
        /*Avoid redundant call to minimum value inversion (might be \infty)
