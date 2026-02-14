ize iSim=0; iSim < nSims_; iSim++) {
            const std::vector<simEvent<D<C, URNG> > >& events = getSim(iSim);
            std::map<unsigned short, unsigned short> namesDefaulting;
            for(Size iEvt=0; iEvt < events.size(); iEvt++) {
                // if event is within time horizon...
                if(val > events[iEvt].dayFromRef)
                    //...count it. notice insertion sorts by date.
                    namesDefaulting.insert(std::make_pair<unsigned short,
                      unsigned short>(events[iEvt].dayFromRef,
                        events[iEvt].nameIdx));
            }
            if(namesDefaulting.size() >= n) {
                auto
                    itdefs = namesDefaulting.begin();
                // locate nth default in time:
                std::advance(itdefs, n-1);
                // update statistic:
                hitsByDate[itdefs->second]++;
            }
        }
        std::transform(hitsByDate.begin(), hitsByDate.end(),
                       hitsByDate.begin(),
                       [this](Real x){ return x/nSims_; });
        return hitsByDate;
        // \todo Provide confidence interval
    }


    template<template <class, class> class D, class C, class URNG>
    Real RandomLM<D, C, URNG>::defaultCorrelation(const Date& d,
        Size iName, Size jName) const
    {
        // a control variate with the probabilities is possible
        calculate();
        Date today = Settings::instance().evaluationDate();

        QL_REQUIRE(d>today, "Date for statistic must be in the future.");
        // casted to natural to avoid warning, we have just checked the sign
        Natural val = d.serialNumber() - today.serialNumber();

        Real expectedDefiDefj = 0.;// E[1_i 1_j]
        // the rest of magnitudes have known values (probabilities) but that
        //   would distort the simulation results.
        Real expectedDefi = 0.;
        Real expectedDefj = 0.;
        for(Size iSim=0; iSim < nSims_; iSim++) {
            const std::vector<simEvent<D<C, URNG> > >& events = getSim(iSim);
            Real imatch = 0., jmatch = 0.;
            for(Size iEvt=0; iEvt < events.size(); iEvt++) {
                if((val > events[iEvt].dayFromRef) &&
                   (events[iEvt].nameIdx == iName)) imatch = 1.;
                if((val > events[iEvt].dayFromRef) &&
                   (events[iEvt].nameIdx == jName)) jmatch = 1.;
            }
            expectedDefiDefj += imatch * jmatch;
            expectedDefi += imatch;
            expectedDefj += jmatch;
        }
        expectedDefiDefj = expectedDefiDefj / (nSims_-1);// unbiased
        expectedDefi = expectedDefi / nSims_;
        expectedDefj = expectedDefj / nSims_;

        return (expectedDefiDefj - expectedDefi*expectedDefj) /
            std::sqrt((expectedDefi*expectedDefj*(1.-expectedDefi)
                *(1.-expectedDefj)));
        // \todo Provide confidence interval
    }


    template<template <class, class> class D, class C, class URNG>
    Real RandomLM<D, C, URNG>::expectedTrancheLoss(
        const Date& d) const {
            return expectedTrancheLossInterval(d, 0.95).first;
    }


    template<template <class, class> class D, class C, class URNG>
    std::pair<Real, Real> RandomLM<D, C, URNG>::expectedTrancheLossInterval(
        const Date& d, Probability confidencePerc) const
    {
        calculate();
        Date today = Settings::instance().evaluationDate();
        Date::serial_type val = d.serialNumber() - today.serialNumber();

        Real attachAmount = basket_->attachmentAmount();
        Real detachAmount = basket_->detachmentAmount();

        // Real trancheLoss= 0.;
        GeneralStatistics lossStats;
        for(Size iSim=0; iSim < nSims_; iSim++) {
            const std::vector<simEvent<D<C, URNG> > >& events = getSim(iSim);

            Real portfSimLoss=0.;
            for(Size iEvt=0; iEvt < events.size(); iEvt++) {
                // if event is within time horizon...