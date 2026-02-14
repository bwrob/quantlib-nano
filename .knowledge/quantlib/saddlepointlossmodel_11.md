     Real saddleTo2 = saddlePt * saddlePt;

        if(saddlePt > 0.) { // <-> (loss > condEL)
            Real exponent = baseVal - relativeLoss * saddlePt + 
                .5 * saddleTo2 * secondVal;
            if( std::abs(exponent) > 700.) return 0.;
            return 
                // dangerous exponential; fix me
                std::exp(exponent)
                /*  std::exp(baseVal - relativeLoss * saddlePt 
                    + .5 * saddleTo2 * secondVal)*/
                * CumulativeNormalDistribution()(-std::abs(saddlePt)*
                    std::sqrt(/*saddleTo2 **/secondVal));
        }else if(saddlePt==0.){// <-> (loss == condEL)
            return .5;
        }else {// <->(loss < condEL)
            Real exponent = baseVal - relativeLoss * saddlePt + 
                .5 * saddleTo2 * secondVal;
            if( std::abs(exponent) > 700.) return 0.;

            return 
                1.-
               /* std::exp(baseVal - relativeLoss * saddlePt 
               + .5 * saddleTo2 * secondVal)*/
                std::exp(exponent)
                * CumulativeNormalDistribution()(-std::abs(saddlePt)*
                    std::sqrt(/*saddleTo2 **/secondVal));
        }
    }


    /*!   NOTICE THIS IS ON THE TOTAL PORTFOLIO ---- UNTRANCHED
    Probability density of having losses in the portfolio due to default 
        events equal to a given value on a given date conditional to the w
        latent model factor.
        Based on the integrals of the expected shortfall. See......refernce.
    */
    template<class CP>
    Probability SaddlePointLossModel<CP>::probDensityCond(
        const std::vector<Real>& invUncondPs,
        Real loss,
        const std::vector<Real>& mktFactor) const 
    {
        if (loss <= QL_EPSILON) return 0.;

        Real relativeLoss = loss / remainingNotional_;
        Real saddlePt = findSaddle(invUncondPs,
            relativeLoss, mktFactor);

        std::tuple<Real, Real, Real, Real> cumulants = 
            CumGen0234DerivCond(invUncondPs,
            saddlePt, mktFactor);
        /// access them directly rather than through this copy
        Real K0Saddle = std::get<0>(cumulants);
        Real K2Saddle = std::get<1>(cumulants);
        Real K3Saddle = std::get<2>(cumulants);
        Real K4Saddle = std::get<3>(cumulants);
        /* see, for instance R.Martin "he saddle point method and portfolio 
        optionalities." in Risk December 2006 p.93 */
        //\todo the exponentials below are dangerous and agressive, tame them.
        return 
            (
            1.
            + K4Saddle
                /(8.*std::pow(K2Saddle, 2.))
            - 5.*std::pow(K3Saddle,2.)
                /(24.*std::pow(K2Saddle, 3.))
            ) * std::exp(K0Saddle - saddlePt * relativeLoss)
             / (std::sqrt(2. * M_PI * K2Saddle));
    }

    /*    NOTICE THIS IS ON THE TOTAL PORTFOLIO ---- UNTRANCHED..
        Sensitivities of the individual names to a given portfolio loss value 
        due to defaults. It returns ratios to the total structure notional, 
        which aggregated add up to the requested loss value.

    see equation 8 in 'VAR: who contributes and how much?' by R.Martin, 
    K.Thompson, and C. Browne in Risk Magazine, August 2001

    The passed loss is the loss amount level at which we want to
    request the sensitivity.  Equivalent to a percentile.
    */
    template<class CP>
    std::vector<Real> SaddlePointLossModel<CP>::splitLossCond(
        const std::vector<Real>& invUncondProbs,
        Real loss, 
        std::vector<Real> mktFactor) const 
    {
        const Size nNames = remainingNotionals_.size();
        std::vector<Real> condContrib(nNames, 0.);
        if (loss <= QL_EPSILON) return condContrib;

        Real saddlePt = findSaddle(invUncondProbs, loss / remainingNotional_, 
            mktFactor);

        for(Size iName=0; iName<nNames; iName++) {
            Probability pBuffer = 
                copula_->conditionalDefaultProbabi