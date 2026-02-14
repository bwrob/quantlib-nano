t std::vector<Real>& v1) {
                    return lossProbability(date, notionals, invProbs, v1);
                });
        }
        //! attainable loss points this model provides
        std::vector<Real> lossPoints(const Date&) const;
        //! Returns the cumulative full loss distribution
        std::map<Real, Probability> lossDistribution(const Date& d) const override;
        //! Loss level for this percentile
        Real percentile(const Date& d, Real percentile) const override;
        Real expectedShortfall(const Date& d, Real percentile) const override;
        Real expectedTrancheLoss(const Date& d) const override;

        // Model internal workings ----------------
        //! Average loss per credit.
        Real averageLoss(const Date&, const std::vector<Real>& reminingNots, 
            const std::vector<Real>&) const;
        Real condTrancheLoss(const Date&, const std::vector<Real>& lossVals, 
            const std::vector<Real>& bsktNots,
            const std::vector<Probability>& uncondDefProbs, 
            const std::vector<Real>&) const;
        // expected as in time-value, not average, see literature
        std::vector<Real> expConditionalLgd(const Date& d,
                                            const std::vector<Real>& mktFactors) const
        {
            std::vector<Real> condLgds;
            const std::vector<Size>& evalDateLives = basket_->liveList();
            condLgds.reserve(evalDateLives.size());
            for (unsigned long evalDateLive : evalDateLives)
                condLgds.push_back(1. - copula_->conditionalRecovery(d, evalDateLive, mktFactors));
            return condLgds;
        }

        //! Loss probability density conditional on the market factor value.
        // Heres where the burden of the algorithm setup lies.
        std::vector<Real> lossProbability(      
                const Date& date,
                // expected exposures at the passed date, no wrong way means
                //  no dependence of the exposure with the mkt factor 
                const std::vector<Real>& bsktNots,
                const std::vector<Real>& uncondDefProbInv, 
                            const std::vector<Real>&  mktFactor) const;

        const ext::shared_ptr<LLM> copula_;

        // cached arguments:
        // remaining basket magnitudes:
        mutable Real attachAmount_, detachAmount_;
    };

    //-------------------------------------------------------------------------

    /* The algorithm to compute the prob. of n defaults in the basket is 
        recursive. For this reason theres no sense in returning the prob 
        distribution of a given number of defaults.
    */
    template< class LLM>
    std::vector<Real> BinomialLossModel<LLM>::lossProbability(
        const Date& date, 
        const std::vector<Real>& bsktNots,
        const std::vector<Real>& uncondDefProbInv, 
        const std::vector<Real>& mktFactors) const 
    {   // the model as it is does not model the exposures conditional to the 
        //   mkt factr, otherwise this needs revision
        /// model does not take the unconditional rr
        Size bsktSize = basket_->remainingSize();
        /* The conditional loss per unit notional of each name at time 'date'
            The spot recovery model is returning for all i's:
            \frac{\int_0^t  [1-rr_i(\tau; \xi)] P_{def-i}(0, \tau; \xi) d\tau}
                 {P_{def-i}(0,t;\xi)}
            and the constant recovery model is simply returning: 
            1-RR_i
        */
        // conditional fractional LGD expected as given by the recovery model 
        //   for the ramaining(live) names at the current eval date.
        std::vector<Real> fractionalEL = expConditionalLgd(date, mktFactors);
        std::vector<Real> lgdsLeft;
        std::transform(fractionalEL.begin(), fractionalEL.end(), 
            bsktNots.begin(), std::back_inserter(lgdsLeft), 
            std::multiplies<>());
        Real avgLgd = 
          