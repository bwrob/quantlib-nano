
                if(val > static_cast<Date::serial_type>(
					   events[iEvt].dayFromRef)) {
                    Size iName = events[iEvt].nameIdx;
                    // ...and is contained in the basket.
                        portfSimLoss +=
                            basket_->exposure(basket_->names()[iName],
                                Date(events[iEvt].dayFromRef +
                                    today.serialNumber())) *
                                        (1.-getEventRecovery(events[iEvt]));
               }
            }
            lossStats.add(// d  ates? current losses? realized defaults, not yet
                std::min(std::max(portfSimLoss - attachAmount, 0.),
                    detachAmount - attachAmount) );
        }
        return std::make_pair(lossStats.mean(), lossStats.errorEstimate() *
            InverseCumulativeNormal::standard_value(0.5*(1.+confidencePerc)));
    }


    template<template <class, class> class D, class C, class URNG>
    std::map<Real, Probability> RandomLM<D, C, URNG>::lossDistribution(const Date& d) const {

        Histogram hist = computeHistogram(d);
        std::map<Real, Probability> distrib;

        // prob of losses less or equal to
        Real suma = hist.frequency(0);
        distrib.insert(std::make_pair(0., suma));
        for(Size i=1; i<hist.bins(); i++) {
            suma += hist.frequency(i);
            distrib.insert(std::make_pair( hist.breaks()[i-1], suma ));
        }
        return distrib;
    }


    template<template <class, class> class D, class C, class URNG>
    Histogram RandomLM<D, C, URNG>::computeHistogram(const Date& d) const {
        std::vector<Real> data;
        std::set<Real> keys;// attainable loss values
        keys.insert(0.);
        Date today = Settings::instance().evaluationDate();
        Date::serial_type val = d.serialNumber() - today.serialNumber();
        // redundant test? should have been tested by the basket caller?
        QL_REQUIRE(d >= today,
            "Requested percentile date must lie after computation date.");
        calculate();

        Real attachAmount = basket_->attachmentAmount();
        Real detachAmount = basket_->detachmentAmount();

        for(Size iSim=0; iSim < nSims_; iSim++) {
            const std::vector<simEvent<D<C, URNG> > >& events = getSim(iSim);

            Real portfSimLoss=0.;
            for(Size iEvt=0; iEvt < events.size(); iEvt++) {
                if(val > static_cast<Date::serial_type>(
					 events[iEvt].dayFromRef)) {
                    Size iName = events[iEvt].nameIdx;
          // test needed (here and the others) to reuse simulations:
          //          if(basket_->pool()->has(copula_->pool()->names()[iName]))
                        portfSimLoss +=
                            basket_->exposure(basket_->names()[iName],
                                Date(events[iEvt].dayFromRef +
                                    today.serialNumber())) *
                                        (1.-getEventRecovery(events[iEvt]));
                }
            }
            data.push_back(std::min(std::max(portfSimLoss - attachAmount, 0.),
                detachAmount - attachAmount));
            keys.insert(data.back());
        }
        // avoid using as many points as in the simulation.
        Size nPts = std::min<Size>(data.size(), 150);// fix
        return Histogram(data.begin(), data.end(), nPts);
    }


    template<template <class, class> class D, class C, class URNG>
    Real RandomLM<D, C, URNG>::expectedShortfall(const Date& d,
        Real percent) const {

        const Date today = Settings::instance().evaluationDate();
        QL_REQUIRE(d >= today,
            "Requested percentile date must lie after computation date.");
        calculate();

        Real attachAmount = basket_->attachmentAmount();
        Real detachAmount = basket_->detachmentAmount();

        Date::serial_type val = d.serialNumber() - today.serialNumber();
        if(val <= 0) re