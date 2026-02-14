t_ - attachAmount_);
            Real lossHere = std::min(std::max(itDist->first - attachAmount_,
                0.), detachAmount_ - attachAmount_);

            Real val =  lossNxt - (itNxt->second - perctl) * 
                (lossNxt - lossHere) / (itNxt->second - itDist->second); 
            Real suma = (itNxt->second - perctl) * (lossNxt + val) * .5;
            ++itDist; ++itNxt;
            do{
                lossNxt = std::min(std::max(itNxt->first - attachAmount_, 
                    0.), detachAmount_ - attachAmount_);
                lossHere = std::min(std::max(itDist->first - attachAmount_, 
                    0.), detachAmount_ - attachAmount_);
                suma += .5 * (lossHere + lossNxt) * (itNxt->second - 
                    itDist->second);
                ++itDist; ++itNxt;
            }while(itNxt != distrib.end());
            return suma / (1.-perctl);
        }
        return 0.;// well, we are in error....  fix: FAIL
    }

    template<class CP>
    std::map<Real, Probability> RecursiveLossModel<CP>::conditionalLossDistrib(
            const std::vector<Probability>& pDefDate, 
            //const Date& date,
            const std::vector<Real>& mktFactor) const 
    {
        //eq. 10 p.68
        //attainable losses distribution, recursive algorithm
        const std::vector<Probability>& uncDefProb = pDefDate;// alias, remove

        std::map<Real, Probability> pIndepDistrib;
        ////////  K=0
        pIndepDistrib.insert(std::make_pair(0., 1.));
        for(Size iName=0; iName<remainingBsktSize_; ++iName) {
            Probability pDef =
                copula_->conditionalDefaultProbability(uncDefProb[iName], iName,
                                                mktFactor);
            ////// iterate on all possible losses in the distribution:
            std::map<Real, Probability> pDistTemp;
            auto distIt = pIndepDistrib.begin();
            while(distIt != pIndepDistrib.end()) {
              ///   update prob if this name does not default
              auto matchIt = pDistTemp.find(distIt->first);
              if (matchIt != pDistTemp.end()) {
                  matchIt->second += distIt->second * (1. - pDef);
                }else{
                    pDistTemp.insert(std::make_pair(distIt->first,
                        distIt->second * (1.-pDef)));
                }
              ////   and if it does
                matchIt = pDistTemp.find(distIt->first + wk_[iName]);
                if(matchIt != pDistTemp.end()) {
                    matchIt->second += distIt->second * pDef;
                }else{
                    pDistTemp.insert(std::make_pair(
                        distIt->first+wk_[iName], distIt->second * pDef));
                }
                ++distIt;
            }
           /////  copy back
            pIndepDistrib = pDistTemp;
        }
        /* Apply tranche limits now .... mind you this could be done outside*/
        ////  to be done....
        return pIndepDistrib;
    }

    // twice?! rewrite one in terms of the other, this is a duplicate!
    template<class CP>
    std::map<Real, Probability> RecursiveLossModel<CP>::conditionalLossDistribInvP(
            const std::vector<Real>& invpDefDate, 
            //const Date& date,
            const std::vector<Real>& mktFactor) const 
    {
        // eq. 10 p.68
        // attainable losses distribution, recursive algorithm

        std::map<Real, Probability> pIndepDistrib;
        // K=0
        pIndepDistrib.insert(std::make_pair(0., 1.));
        for(Size iName=0; iName<remainingBsktSize_; ++iName) {
            Probability pDef =
                copula_->conditionalDefaultProbabilityInvP(invpDefDate[iName], 
                    iName, mktFactor);

            // iterate on all possible losses in the distribution:
            std::map<Real, Probability> pDistTemp;
            auto distIt = pIndepDistrib.begin();
            while(distIt != pIndepDistrib.end()) {
                // 