Interval(const Date& d,
                                                                             Real percentile) const {

        QL_REQUIRE(percentile >= 0. && percentile <= 1.,
            "Incorrect percentile");
        calculate();

        Real attachAmount = basket_->attachmentAmount();
        Real detachAmount = basket_->detachmentAmount();

        std::vector<Real> rankLosses;
        Date today = Settings::instance().evaluationDate();
        Date::serial_type val = d.serialNumber() - today.serialNumber();
        for(Size iSim=0; iSim < nSims_; iSim++) {
            const std::vector<simEvent<D<C, URNG> > >& events = getSim(iSim);
            Real portfSimLoss=0.;
            for(Size iEvt=0; iEvt < events.size(); iEvt++) {
                if(val > static_cast<Date::serial_type>(
					 events[iEvt].dayFromRef)) {
                    Size iName = events[iEvt].nameIdx;
                 //   if(basket_->pool()->has(copula_->pool()->names()[iName]))
                        portfSimLoss +=
                            basket_->exposure(basket_->names()[iName],
                                Date(events[iEvt].dayFromRef +
                                    today.serialNumber())) *
                                        (1.-getEventRecovery(events[iEvt]));
                }
            }
            portfSimLoss = std::min(std::max(portfSimLoss - attachAmount, 0.),
                detachAmount - attachAmount);
            // update dataset for rank stat:
            rankLosses.push_back(portfSimLoss);
        }

        std::sort(rankLosses.begin(), rankLosses.end());
        Size quantilePosition = static_cast<Size>(floor(nSims_*percentile));
        Real quantileValue = rankLosses[quantilePosition];

        // compute confidence interval:
        const Probability confInterval = 0.95;// as an argument?
        Real lowerPercentile, upperPercentile;
        Size r = quantilePosition - 1;
        Size s = quantilePosition + 1;
        bool rLocked = false,
            sLocked = false;
        // Size rfinal = 0,
        //      sfinal = 0;
        for(Size delta=1; delta < quantilePosition; delta++) {
            Real cached =
                incompleteBetaFunction(Real(s), Real(nSims_+1-s),
                                       percentile, 1.e-8, 500);
            Real pMinus =
            /* There was a fix in the repository on the gammadistribution. It
            might impact these, it might be neccesary to multiply these values
            by '-1'*/
                incompleteBetaFunction(Real(r+1), Real(nSims_-r),
                                       percentile, 1.e-8, 500)
                - cached;
            Real pPlus  =
                incompleteBetaFunction(Real(r), Real(nSims_-r+1),
                                       percentile, 1.e-8, 500)
                - cached;
            if((pMinus > confInterval) && !rLocked ) {
                // rfinal = r + 1;
               rLocked = true;
            }
            if((pPlus >= confInterval) && !sLocked) {
                // sfinal = s;
                sLocked = true;
            }
            if(rLocked && sLocked) break;
            r--;
            s++;
            s = std::min(nSims_-1, s);
        }
        lowerPercentile = rankLosses[r];
        upperPercentile = rankLosses[s];

        return std::make_tuple(quantileValue, lowerPercentile, upperPercentile);
    }


    template<template <class, class> class D, class C, class URNG>
    std::vector<Real> RandomLM<D, C, URNG>::splitVaRLevel(
        const Date& date, Real loss) const
    {
        std::vector<Real> varLevels = splitVaRAndError(date, loss, 0.95)[0];
        // turn relative units into absolute:
        std::transform(varLevels.begin(), varLevels.end(), varLevels.begin(),
                       [=](Real x) -> Real { return x * loss; });
        return varLevels;
    }


    // parallelize this one(if possible), it is really expensive
    template<template <class, class> class D, 