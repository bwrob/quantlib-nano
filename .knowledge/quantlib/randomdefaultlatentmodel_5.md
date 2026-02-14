turn 0.;// plus basket realized losses

        //GenericRiskStatistics<GeneralStatistics> statsX;
        std::vector<Real> losses;
        for(Size iSim=0; iSim < nSims_; iSim++) {
            const std::vector<simEvent<D<C, URNG> > >& events = getSim(iSim);
            Real portfSimLoss=0.;
            for(Size iEvt=0; iEvt < events.size(); iEvt++) {
                if(val > static_cast<Date::serial_type>(
					  events[iEvt].dayFromRef)) {
                    Size iName = events[iEvt].nameIdx;
                    // ...and is contained in the basket.
                    //if(basket_->pool()->has(copula_->pool()->names()[iName]))
                        portfSimLoss +=
                            basket_->exposure(basket_->names()[iName],
                                Date(events[iEvt].dayFromRef +
                                    today.serialNumber())) *
                                        (1.-getEventRecovery(events[iEvt]));
                }
            }
            portfSimLoss = std::min(std::max(portfSimLoss - attachAmount, 0.),
                detachAmount - attachAmount);
            losses.push_back(portfSimLoss);
        }

        std::sort(losses.begin(), losses.end());
        Real posit = std::ceil(percent * nSims_);
        posit = posit >= 0. ? posit : 0.;
        Size position = static_cast<Size>(posit);
        Real perctlInf = losses[position];//q_{\alpha}

        // the prob of values strictly larger than the quantile value.
        Probability probOverQ =
            static_cast<Real>(std::distance(losses.begin() + position,
                losses.end())) / static_cast<Real>(nSims_);

        return ( perctlInf * (1.-percent-probOverQ) +//<-correction term
            std::accumulate(losses.begin() + position, losses.end(),
			    Real(0.))/nSims_
                )/(1.-percent);

        /* Alternative ESF definition; find the first loss larger than the
        one of the percentile. Notice the choice here, the expected shortfall
        is understood in the sense that we are looking for the average given
        than losses are above a certain value rather than above a certain
        probability:
        (Unlikely to be the algorithm of choice)*/
        /*
        std::vector<Real>::iterator itPastPerc =
            std::find_if(losses.begin() + position, losses.end(),
                         [=](Real x){ return x >= perctlInf; });
        // notice if the sample is flat at the end this might be zero
        Size pointsOverVal = nSims_ - std::distance(itPastPerc, losses.end());
        return pointsOverVal == 0 ? 0. :
            std::accumulate(itPastPerc, losses.end(), 0.) / pointsOverVal;
        */

        /* For the definition of ESF see for instance: 'Quantitative Risk
        Management' by A.J. McNeil, R.Frey and P.Embrechts, princeton series in
        finance, 2005; equations on page 39 sect 2.12:
        $q_{\alpha}(F) = inf{x \in R : F(x) \le \alpha}$
        and equation 2.25 on p. 45:
        $ESF_{\alpha} = \frac{1}{1-\alpha} [E(L; L \ge q_{\alpha} ) +
            q_{\alpha} (1-\alpha-P(L \ge q_{\alpha})) ]$
        The second term accounts for non continuous distributions.
        */
    }


    template<template <class, class> class D, class C, class URNG>
    Real RandomLM<D, C, URNG>::percentile(const Date& d, Real perc) const {
        // need to specify return type in tuples' get is parametric
        return std::get<0>(percentileAndInterval(d, perc));
    }


    /* See Appendix-A of "Evaluating value-at-risk methodologies: Accuracy
        versus computational time.", M. Pritsker, Wharton FIC, November 1996
    Strictly speaking this gives the interval with a 95% probability of
    the true value being within the interval; which is different to the error
    of the stimator just computed. See the reference for a discussion.
    */
    template<template <class, class> class D, class C, class URNG>
    std::tuple<Real, Real, Real> RandomLM<D, C, URNG>::percentileAnd
