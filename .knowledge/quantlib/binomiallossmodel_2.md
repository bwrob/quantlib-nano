  std::accumulate(lgdsLeft.begin(), lgdsLeft.end(), Real(0.)) /
                bsktSize;

        std::vector<Probability> condDefProb(bsktSize, 0.);
        for(Size j=0; j<bsktSize; j++)//transform
            condDefProb[j] =
                copula_->conditionalDefaultProbabilityInvP(uncondDefProbInv[j],
                    j, mktFactors);
        // of full portfolio:
        Real avgProb = avgLgd <= QL_EPSILON ? Real(0.) : // only if all are 0
                std::inner_product(condDefProb.begin(),
                    condDefProb.end(), lgdsLeft.begin(), Real(0.))
                / (avgLgd * bsktSize);
        // model parameters:
        Real m = avgProb * bsktSize;
        Real floorAveProb = std::min(Real(bsktSize-1), std::floor(Real(m)));
        Real ceilAveProb = floorAveProb + 1.;
        // nu_A
        Real varianceBinom = avgProb * (1. - avgProb)/bsktSize;
        // nu_E
        std::vector<Probability> oneMinusDefProb;//: 1.-condDefProb[j]
        std::transform(condDefProb.begin(), condDefProb.end(),
                       std::back_inserter(oneMinusDefProb),
                       [](Real x) -> Real { return 1.0-x; });

        //breaks condDefProb and lgdsLeft to spare memory
        std::transform(condDefProb.begin(), condDefProb.end(),
            oneMinusDefProb.begin(), condDefProb.begin(),
            std::multiplies<>());
        std::transform(lgdsLeft.begin(), lgdsLeft.end(),
            lgdsLeft.begin(), lgdsLeft.begin(), std::multiplies<>());
        Real variance = std::inner_product(condDefProb.begin(),
            condDefProb.end(), lgdsLeft.begin(), Real(0.));

        variance = avgLgd <= QL_EPSILON ? Real(0.) :
            variance / (bsktSize * bsktSize * avgLgd * avgLgd );
        Real sumAves = -std::pow(ceilAveProb-m, 2)
            - (std::pow(floorAveProb-m, 2) - std::pow(ceilAveProb,2.))
                * (ceilAveProb-m);
        Real alpha = (variance * bsktSize + sumAves)
            / (varianceBinom * bsktSize + sumAves);
        // Full distribution:
        // ....DO SOMETHING CHEAPER at least go up to the loss tranche limit.
        std::vector<Probability> lossProbDensity(bsktSize+1, 0.);
        if(avgProb >= 1.-QL_EPSILON) {
           lossProbDensity[bsktSize] = 1.;
        }else if(avgProb <= QL_EPSILON) {
           lossProbDensity[0] = 1.;
        }else{
            /* FIX ME: With high default probabilities one only gets tiny values
            at the end and the sum of probabilities in the
            conditional distribution does not add up to one. It might be due to
            the fact that recursion should be done in the other direction as
            pointed out in the book. This is numerical.
            */
            Probability probsRatio = avgProb/(1.-avgProb);
            lossProbDensity[0] = std::pow(1.-avgProb,
                static_cast<Real>(bsktSize));
            for(Size i=1; i<bsktSize+1; i++) // recursive to avoid factorial
                lossProbDensity[i] = lossProbDensity[i-1] * probsRatio
                    * (bsktSize-i+1.)/i;
            // redistribute probability:
            for(Size i=0; i<bsktSize+1; i++)
                lossProbDensity[i] *= alpha;
            // adjust average
            Real epsilon = (1.-alpha)*(ceilAveProb-m);
            Real epsilonPlus = 1.-alpha-epsilon;
            lossProbDensity[static_cast<Size>(floorAveProb)] += epsilon;
            lossProbDensity[static_cast<Size>(ceilAveProb)]  += epsilonPlus;
        }
        return lossProbDensity;
    }

    //-------------------------------------------------------------------------

    template< class LLM>
    Real BinomialLossModel<LLM>::averageLoss(
        const Date& d,
        const std::vector<Real>& reminingNots,
        const std::vector<Real>& mktFctrs) const
    {
        Size bsktSize = basket_->remainingSize();
        /* The conditional loss per unit notional of each name at time 'date'
            The spot recovery model is ret
