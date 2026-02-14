saddle);
            Real denominator = 1.-pBuffer + midFactor;

            const Real& suma0 = denominator;
            const Real suma1  = lossInDef * midFactor;
            const Real suma2  = lossInDef * suma1;

            // To do: optimize these:
            deriv0 += std::log(suma0);
            //deriv1 += suma1 / suma0;
            deriv2 += suma2 / suma0 - std::pow(suma1 / suma0 , 2.);
        }
        return {deriv0, deriv2};
    }

    // ----- Saddle point search ----------------------------------------------

    template<class CP>
    Real SaddlePointLossModel<CP>::findSaddle(
        const std::vector<Real>& invUncondPs,
        Real lossLevel, // in total portfolio loss fractional unit
        const std::vector<Real>& mktFactor,
        Real accuracy,
        Natural maxEvaluations
        ) const
    {
        // \to do:
        // REQUIRE that loss level is below the max loss attainable in
        //   the portfolio, otherwise theres no solution...
        SaddleObjectiveFunction f(*this, lossLevel, invUncondPs, mktFactor);

        Size nNames = remainingNotionals_.size();
        std::vector<Real> lgds;
        for(Size iName=0; iName<nNames; iName++)
            lgds.push_back(remainingNotionals_[iName] *
            (1.-copula_->conditionalRecoveryInvP(invUncondPs[iName], iName,
                mktFactor)) );

        // computed limits:
        // position of the name with the largest relative exposure loss (i.e.:
        //   largest: N_i LGD_i / N_{total})
        Size iNamMax = std::distance(lgds.begin(),
            std::max_element(lgds.begin(), lgds.end()) );
        // gap to be considered zero at the negative side of the logistic
        //   inversion:
        static const Real deltaMin = 1.e-5;
        //
        Probability pMaxName = copula_->conditionalDefaultProbabilityInvP(
            invUncondPs[iNamMax], iNamMax, mktFactor);
        // approximates the  saddle pt corresponding to this minimum; finds
        //   it by using only the smallest logistic term and thus this is
        //   smaller than the true value:
        Real saddleMin = 1./(lgds[iNamMax]/remainingNotional_) *
            std::log(deltaMin*(1.-pMaxName)/
                (pMaxName*lgds[iNamMax]/remainingNotional_-pMaxName*deltaMin));
        // and the associated minimum loss is approximately: (this is thence
        //   the minimum loss we can resolve/invert)
        Real minLoss =
            CumGen1stDerivativeCond(invUncondPs, saddleMin, mktFactor);

        // If we are below the loss resolution it returns approximating
        //  by the minimum/maximum attainable point. Typically the functionals
        //  to integrate will have a low dependency on this point.
        if(lossLevel < minLoss) return saddleMin;

        Real saddleMax = 1./(lgds[iNamMax]/remainingNotional_) *
            std::log((lgds[iNamMax]/remainingNotional_
                -deltaMin)*(1.-pMaxName)/(pMaxName*deltaMin));
        Real maxLoss =
            CumGen1stDerivativeCond(invUncondPs, saddleMax, mktFactor);
        if(lossLevel > maxLoss) return saddleMax;

        Brent solverBrent;
        Real guess = (saddleMin+saddleMax)/2.;
        /*
            (lossLevel -
                CumGen1stDerivativeCond(invUncondPs, lossLevel, mktFactor))
                /CumGen2ndDerivativeCond(invUncondPs, lossLevel, mktFactor);
        if(guess > saddleMax) guess = (saddleMin+saddleMax)/2.;
        */
        solverBrent.setMaxEvaluations(maxEvaluations);
        return solverBrent.solve(f, accuracy, guess, saddleMin, saddleMax);
    }


    // ----- Statistics -------------------------------------------------------


    template<class CP>
    Real SaddlePointLossModel<CP>::percentile(const Date& d,
        Probability percentile) const
    {
        //this test should be in the calling basket...?
        QL_REQUIRE(percentile >=0. && percentile <=1.,
            "Incorrect percentile value.");

        // still this does not
