->remainingProbabilities(date);
        return copula_->integratedExpectedValueV(
            [&](const std::vector<Real>& v1) {
                return conditionalLossProb(uncDefProb, v1);
            });
    }

    // -------------------------------------------------------------------

    template<class CP>
    void RecursiveLossModel<CP>::resetModel() {
        // basket update:
        notionals_ = basket_->remainingNotionals();
        notional_  = basket_->remainingNotional();
        attachAmount_ = basket_->remainingAttachmentAmount();
        detachAmount_ = basket_->remainingDetachmentAmount();
        // model parameters:
        remainingBsktSize_ = notionals_.size();

        copula_->resetBasket(basket_.currentLink());

        std::vector<Real> lgdsTmp, lgds;
        for(Size i=0; i<remainingBsktSize_; ++i)
            lgds.push_back(notionals_[i]*(1.-copula_->recoveries()[i]));
        lgdsTmp = lgds;
        ///////////////std::remove(lgds.begin(), lgds.end(), 0.);
        lgds.erase(std::remove(lgds.begin(), lgds.end(), 0.), lgds.end());
        lossUnit_ = *(std::min_element(lgds.begin(), lgds.end()))
            / nBuckets_;
        for(Size i=0; i<remainingBsktSize_; ++i)
            wk_.push_back(std::floor(lgdsTmp[i]/lossUnit_ + .5));
    }

    // make it return a distribution object?
    template<class CP>
    std::map<Real, Probability> RecursiveLossModel<CP>::lossDistribution(const Date& d) const 
    {
        std::map<Real, Probability> distrib;
        std::vector<Real> values  = lossProbability(d);
        Real sum = 0.;
        for(Size i=0; i<values.size(); ++i) {
            distrib.insert(std::make_pair<Real, Probability>(i * lossUnit_, 
                sum + values[i]));
            sum += values[i];
        }
        return distrib;
    }

    // Integrate then search rather than search and then integrate?
    // Here I am not using a search because the point might be not attainable 
    //   (loss distrib is not continuous) 
    template<class CP>
    Real RecursiveLossModel<CP>::percentile(const Date& d, 
        Real percentile) const 
    {
        std::map<Real, Probability> dist = lossDistribution(d);

        if(dist.begin()->second >=1.) return dist.begin()->first;

        // deterministic case (e.g. date requested is todays date)
        if(dist.size() == 1) return dist.begin()->first;

        if(percentile == 1.) return dist.rbegin()->second;
        if(percentile == 0.) return dist.begin()->second;
        std::map<Real, Probability>::const_iterator itdist = dist.begin();
        while (itdist->second <= percentile) ++itdist;
        Real valPlus = itdist->second;
        Real xPlus   = itdist->first;
        --itdist;  //we're never 1st or last, because of tests above
        Real valMin  = itdist->second;
        Real xMin    = itdist->first;

        // return xPlus-(xPlus-xMin)*(valPlus-percentile)/(valPlus-valMin);
        Real portfLoss =  xPlus-(xPlus-xMin)*(valPlus-percentile)
            /(valPlus-valMin);
        return //remainingNotional_ * 
            std::min(std::max(portfLoss - attachAmount_, 0.), 
                detachAmount_ - attachAmount_);/////(detach_ - attach_);
    }

    template<class CP>
    Real RecursiveLossModel<CP>::expectedShortfall(const Date& d, 
        Real perctl) const 
    {
        if(d == Settings::instance().evaluationDate()) return 0.;
        std::map<Real, Probability> distrib = lossDistribution(d);

        std::map<Real, Probability>::iterator itNxt, itDist = 
            distrib.begin();
        for(; itDist != distrib.end(); ++itDist)
            if(itDist->second >= perctl) break;
        itNxt = itDist;
        --itDist; // what if we are on the first one?!!!

        // One could linearly triangulate the exact point and get extra 
        // precission on the first(broken) period.
        if(itNxt != distrib.end()) { 
            Real lossNxt = std::min(std::max(itNxt->first - attachAmount_, 
                0.), detachAmoun