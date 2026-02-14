update prob if this name does not default
                auto matchIt = pDistTemp.find(distIt->first);
                if(matchIt != pDistTemp.end()) {
                    matchIt->second += distIt->second * (1.-pDef);
                }else{
                    pDistTemp.insert(std::make_pair(distIt->first,
                        distIt->second * (1.-pDef)));
                }
                // and if it does
                matchIt = pDistTemp.find(distIt->first + wk_[iName]);
                if(matchIt != pDistTemp.end()) {
                    matchIt->second += distIt->second * pDef;
                }else{
                    pDistTemp.insert(std::make_pair(
                        distIt->first+wk_[iName], distIt->second * pDef));
                }
                ++distIt;
            }
            // copy back
            pIndepDistrib = pDistTemp;
        }
        /* Apply tranche limits now .... mind you this could be done outside*/
        return pIndepDistrib;
    }




    /*
    Bugs here???. The max min on the tranche looks 
    wrong. It is better to have a tranche function since that way we can avoid 
    adding up losses over all the possible losses rather than just over the 
    tranche limits.
    */
    //! Portfolio loss conditional to the market factor value
    template<class CP>
    Real RecursiveLossModel<CP>::expectedConditionalLoss(
        const std::vector<Probability>& pDefDate, 
        //const Date& date,
        const std::vector<Real>& mktFactor) const 
    {
        std::map<Real, Probability> pIndepDistrib =
            conditionalLossDistrib(pDefDate, mktFactor);

        // get the expected value subject to the value of the market
        //   factor.
        Real expLoss = 0.;
        //---------------------------------------------------------------
        /* This is the original (easy to read) loop which I have partially
             unroll below to take profit of the fact that once we go over
             the tranche top the loss amount is fixed:
        */
        auto distIt = pIndepDistrib.begin();

        while(distIt != pIndepDistrib.end()) {
            Real loss = distIt->first * lossUnit_;
     //       loss = std::max(std::min(loss, detachAmount_)-attachAmount_, 0.);
            loss = std::min(std::max(loss - attachAmount_, 0.), 
                detachAmount_ - attachAmount_);
            // MIN MAX BUGS ....??
            expLoss += loss * distIt->second;
            ++distIt;
        }
        return expLoss ;
    }

    template<class CP>
    // again, I am duplicating code.
    Real RecursiveLossModel<CP>::expectedConditionalLossInvP(
                                 const std::vector<Real>& invPDefDate, 
                                 //const Date& date,
                                 const std::vector<Real>& mktFactor) const 
    {
        std::map<Real, Probability> pIndepDistrib =
            conditionalLossDistribInvP(invPDefDate, mktFactor);

        // get the expected value subject to the value of the market
        //   factor.
        Real expLoss = 0.;
        //---------------------------------------------------------------
        /* This is the original (easy to read) loop which I have partially
             unroll below to take profit of the fact that once we go over
             the tranche top the loss amount is fixed:
        */
        auto distIt = pIndepDistrib.begin();

        while(distIt != pIndepDistrib.end()) {
            Real loss = distIt->first * lossUnit_;
   //         loss = std::max(std::min(loss, detachAmount_)-attachAmount_, 0.);
            loss = std::min(std::max(loss - attachAmount_, 0.), 
                detachAmount_ - attachAmount_);
            // MIN MAX BUGS ....???
            expLoss += loss * distIt->second;
            ++distIt;
        }
        return expLoss ;
    }

    template<class CP>
    std::vector<Real> RecursiveLossModel<CP>::conditionalLossProb(
        const std::vector<Probability>& pDefDate, 
     