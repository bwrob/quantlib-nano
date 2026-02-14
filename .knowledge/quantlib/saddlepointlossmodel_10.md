dProbs,
            relativeLoss, mktFactor);

        std::tuple<Real, Real, Real, Real> cumulants =
            CumGen0234DerivCond(invUncondProbs,
                saddlePt, mktFactor);
        Real baseVal = std::get<0>(cumulants);
        Real secondVal = std::get<1>(cumulants);
        Real K3Saddle = std::get<2>(cumulants);
        Real K4Saddle = std::get<3>(cumulants);

        Real saddleTo2 = saddlePt * saddlePt;
        Real saddleTo3 = saddleTo2 * saddlePt;
        Real saddleTo4 = saddleTo3 * saddlePt;
        Real saddleTo6 = saddleTo4 * saddleTo2;
        Real K3SaddleTo2 = K3Saddle*K3Saddle;

        if(saddlePt > 0.) { // <-> (loss > condEL)
            Real exponent = baseVal - relativeLoss * saddlePt +
                .5 * saddleTo2 * secondVal;
            if( std::abs(exponent) > 700.) return 0.;
            return
                std::exp(exponent)
                * CumulativeNormalDistribution()(-std::abs(saddlePt)*
                    std::sqrt(/*saddleTo2 **/secondVal))

                // high order corrections:
                * (1. - saddleTo3*K3Saddle/6. + saddleTo4*K4Saddle/24. +
                    saddleTo6*K3SaddleTo2/72.)
                /*
                // FIX ME: this term introduces at times numerical
                //   instabilty (shows up in percentile computation)
                + (3.*secondVal*(1.-secondVal*saddleTo2)*
                        (saddlePt*K4Saddle-4.*K3Saddle)
                    - saddlePt*K3SaddleTo2*(3.-saddleTo2*secondVal +
                            saddleTo4*secondVal*secondVal))
                     / (72.*M_SQRTPI*M_SQRT_2*std::pow(secondVal, 5./2.) )
                 */
                 ;
        }else if(saddlePt==0.){// <-> (loss == condEL)
            return .5;
        }else {// <->(loss < condEL)
            Real exponent = baseVal - relativeLoss * saddlePt +
                .5 * saddleTo2 * secondVal;
            if( std::abs(exponent) > 700.) return 0.;
            return
                1.-
                std::exp(exponent)
                * CumulativeNormalDistribution()(-std::abs(saddlePt)
                    * std::sqrt(/*saddleTo2 **/secondVal))// static call?

                // high order corrections:
                * (1. - saddleTo3*K3Saddle/6. + saddleTo4*K4Saddle/24. +
                    saddleTo6*K3SaddleTo2/72.)
                /*
                  + (3.*secondVal*(1.-secondVal*saddleTo2)*
                    (saddlePt*K4Saddle-4.*K3Saddle)
                  - saddlePt*K3SaddleTo2*(3.-saddleTo2*secondVal +
                        saddleTo4*secondVal*secondVal))
                    / (72.*M_SQRTPI*M_SQRT_2*std::pow(secondVal, 5./2.) )
                */
                ;
        }
    }

    template<class CP>
    // cheaper; less terms retained; yet the cost lies in the saddle point calc
    Probability SaddlePointLossModel<CP>::probOverLossPortfCond1stOrder(
        const std::vector<Real>& invUncondPs,
        Real loss,
        const std::vector<Real>& mktFactor) const
    {
        if (loss <= QL_EPSILON) return 1.;
        const Size nNames = remainingNotionals_.size();

        Real relativeLoss = loss / remainingNotional_;
        if(relativeLoss >= 1.-QL_EPSILON) return 0.;

        // only true for constant recovery models......?
        Real averageRecovery_ = 0.;
        for(Size iName=0; iName < nNames; iName++)
            averageRecovery_ +=
            copula_->conditionalRecoveryInvP(invUncondPs[iName], iName,
            mktFactor);
        averageRecovery_ = averageRecovery_ / nNames;

        Real maxAttLossFract = 1.-averageRecovery_;
        if(relativeLoss > maxAttLossFract) return 0.;

        Real saddlePt = findSaddle(invUncondPs,
            relativeLoss, mktFactor);

        std::tuple<Real, Real> cumulants =
            CumGen02DerivCond(invUncondPs,
                saddlePt, mktFactor);
        Real baseVal = std::get<0>(cumulants);
        Real secondVal = std::get<1>(cumulants);


