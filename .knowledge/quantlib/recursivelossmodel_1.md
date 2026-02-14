 the first equation on page 70 (not numbered)
            Notice that while we want to compute:
            \f[
            EL(t) = \sum_{l_k}l_k P(l;t) =
              \sum_{l_k}l_k \int P(l_k;t|\omega) d\omega q(\omega)
            \f]
            One can invert the sumation and the integral order to:
            \f[
            EL(t) = \int\,q(\omega)\,d\omega\,\sum_{l_k}\,l_k\,P(l_k;t|\omega) =
              \int\,q(\omega)\,d\omega\,EL(t|\omega)
            \f]
            and this is the way it is integrated here. The recursion formula 
            makes it easier this way.
        */
      Real expectedTrancheLoss(const Date& date) const override;
      std::vector<Real> lossProbability(const Date& date) const;
      // REMEBER THIS HAS TO BE MOVED TO A DISTRIBUTION OBJECT.............
      std::map<Real, Probability> lossDistribution(const Date& d) const override;
      // INTEGRATE THEN SEARCH RATHER THAN SEARCH AND THEN INTEGRATE:
      // Here I am not using a search because the point might not be attainable
      //  (loss distrib is not continuous)
      Real percentile(const Date& d, Real percentile) const override;
      Real expectedShortfall(const Date& d, Real perctl) const override;

    protected:
        const ext::shared_ptr<ConstantLossLatentmodel<copulaPolicy> > copula_;
    private:
        // loss model descriptor members
        const Size nBuckets_;
        mutable std::vector<Real> wk_;
        mutable Real lossUnit_;
        //! name to name factor. In the single factor copula:
        //    correl = beta * beta
        // When constructing through a single correlation number the factor is
        //   taken to be the positive swuare root of this number in the copula.
        ////////in the latent model now: mutable std::vector<Real> oneFactorCorrels_;
        // cached remaining basket magnitudes:
        mutable Real attachAmount_, 
            detachAmount_,
            notional_;
        mutable Size remainingBsktSize_;
        mutable std::vector<Real> notionals_;
    };


    typedef RecursiveLossModel<GaussianCopulaPolicy> RecursiveGaussLossModel;

    // Inlines ------------------------------------------------

    template<class CP>
    inline Real RecursiveLossModel<CP>::expectedTrancheLoss(
        const Date& date) const 
    {
/*
        std::map<Real, Probability> dist = lossDistribution(date);

        Real expLoss = 0.;
        std::map<Real, Probability>::iterator distIt = dist.begin();

        while(distIt != dist.end()) {
            Real loss = distIt->first * lossUnit_;
            loss = std::max(std::min(loss, detachAmount_)-attachAmount_, 0.);
            // MIN MAX BUGS ....??
            expLoss += loss * distIt->second;
            distIt++;
        }
        return expLoss ;




    ///////////////////////////////////////////////////////////////////////

        // calculate inverted unconditional Ps first so we save the inversion:
        // TO DO : turn to STL algorithm code
        std::vector<Probability> uncDefProb = 
            basket_->remainingProbabilities(date);

        return copula_->integratedExpectedValue(
            [&](const std::vector<Real>& v1) {
                return expectedConditionalLoss(uncDefProb, v1);
            });
            */

        std::vector<Probability> uncDefProb = 
            basket_->remainingProbabilities(date);
        std::vector<Real> invProb;
        for(Size i=0; i<uncDefProb.size(); ++i)
           invProb.push_back(copula_->inverseCumulativeY(uncDefProb[i], i));
           ///  invProb.push_back(CP::inverseCumulativeY(uncDefProb[i], i));//<-static call
        return copula_->integratedExpectedValue(
            [&](const std::vector<Real>& v1) {
                return expectedConditionalLossInvP(invProb, v1);
            });
    }

    template<class CP>
    inline std::vector<Real> RecursiveLossModel<CP>::lossProbability(const Date& date) const {

        std::vector<Probability> uncDefProb = 
            basket_