 tackle the situation where we have cumulated 
        //   losses from previous defaults:
        if(d <= Settings::instance().evaluationDate()) return 0.;

        // Trivial cases when the percentile is outside the prob range 
        //   associated to the tranche limits:
        if(percentile <= 1.-probOverLoss(d, 0.)) return 0.;
        if(percentile >= 1.-probOverLoss(d, 1.)) 
            return basket_->remainingTrancheNotional();

        SaddlePercObjFunction f(*this, percentile, d);
        Brent solver;
        solver.setMaxEvaluations(100);
        Real minVal = QL_EPSILON;

        Real maxVal = 1.-QL_EPSILON; 
        Real guess = 0.5;

        Real solut = solver.solve(f, 1.e-4, guess, minVal, maxVal);
        return basket_->remainingTrancheNotional() * solut;
    }

    template<class CP>
    Probability SaddlePointLossModel<CP>::probOverLossCond(
        const std::vector<Real>& invUncondPs,
        Real trancheLossFract, 
        const std::vector<Real>& mktFactor) const {
        Real portfFract = attachRatio_ + trancheLossFract * 
            (detachRatio_-attachRatio_);// these are remaining ratios
        
        // for non-equity losses add the probability jump at zero tranche 
        //   losses (since this method returns prob of losing more or 
        //   equal to)
        ////////////////---       if(trancheLossFract <= QL_EPSILON) return 1.;
        return 
            probOverLossPortfCond(invUncondPs,
            //below; should substract realized loses. Use remaining amounts??
                portfFract * basket_->basketNotional(),
                mktFactor);
    }

    template<class CP>
    std::map<Real, Probability> SaddlePointLossModel<CP>::lossDistribution(const Date& d) const {
        std::map<Real, Probability> distrib;
        static constexpr double numPts = 500.;
        for(Real lossFraction=1./numPts; lossFraction<0.45; 
            lossFraction+= 1./numPts)
            distrib.insert(std::make_pair<Real, Probability>(
                lossFraction * remainingNotional_ , 
                  1.-probOverPortfLoss(d, lossFraction* remainingNotional_ )));
        return distrib;
    }

    /*  NOTICE THIS IS ON THE TOTAL PORTFOLIO ---- UNTRANCHED..............
        Probability of having losses in the portfolio due to default 
        events equal or larger than a given absolute loss value on a 
        given date conditional to the latent model factor.
        The integral expression on the expansion is the first order 
        integration as presented in several references, see for instance; 
        equation 8 in R.Martin, K.Thompson, and C. Browne 's 
        'Taking to the Saddle', Risk Magazine, June 2001, page 91

        The loss is passed in absolute value.
    */
    template<class CP>
    Probability SaddlePointLossModel<CP>::probOverLossPortfCond(
        const std::vector<Real>& invUncondProbs,
        Real loss, 
        const std::vector<Real>& mktFactor) const 
    {
        /* This is taking in the unconditional probabilites non inverted. See if
        the callers can be written taking the inversion already; if they are 
        performing it thats a perf hit. At least this can be seen to be true
        for the recovery call (but rand rr are not intended to be used yet)
        */
       // return probOverLossPortfCond1stOrder(d, loss, mktFactor);
        if (loss <= QL_EPSILON) return 1.;

        Real relativeLoss = loss / remainingNotional_;
        if (relativeLoss >= 1.-QL_EPSILON) return 0.;

        const Size nNames = remainingNotionals_.size();

        Real averageRecovery_ = 0.;
        for(Size iName=0; iName < nNames; iName++)
            averageRecovery_ += copula_->conditionalRecoveryInvP(
                invUncondProbs[iName], iName, mktFactor);
        averageRecovery_ = averageRecovery_ / nNames;

        Real maxAttLossFract = 1.-averageRecovery_;
        if(relativeLoss > maxAttLossFract) return 0.;

        Real saddlePt = findSaddle(invUncon