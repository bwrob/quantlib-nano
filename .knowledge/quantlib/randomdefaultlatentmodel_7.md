class C, class URNG>
    /* FIX ME: some trouble on limit cases, like zero loss or no losses over the
    requested level.*/
    std::vector<std::vector<Real> > RandomLM<D, C, URNG>::splitVaRAndError(const Date& date, Real loss,
                                                                           Probability confInterval) const
    {
        /* Check 'loss' value integrity: i.e. is within tranche limits? (should
            have been done basket...)*/
        calculate();

        Real attachAmount = basket_->attachmentAmount();
        Real detachAmount = basket_->detachmentAmount();
        Size numLiveNames = basket_->remainingSize();

        std::vector<Real> split(numLiveNames, 0.);
        std::vector<GeneralStatistics> splitStats(numLiveNames,
            GeneralStatistics());
        Date today = Settings::instance().evaluationDate();
        Date::serial_type val = date.serialNumber() - today.serialNumber();

        for(Size iSim=0; iSim < nSims_; iSim++) {
            const std::vector<simEvent<D<C, URNG> > >& events = getSim(iSim);
            Real portfSimLoss=0.;
            //std::vector<Real> splitBuffer(numLiveNames_, 0.);
            std::vector<simEvent<D<C, URNG> > > splitEventsBuffer;

            for(Size iEvt=0; iEvt < events.size(); iEvt++) {
                if(val > static_cast<Date::serial_type>(
					 events[iEvt].dayFromRef)) {
                    Size iName = events[iEvt].nameIdx;
                // if(basket_->pool()->has(copula_->pool()->names()[iName])) {
                        portfSimLoss +=
                            basket_->exposure(basket_->names()[iName],
                                Date(events[iEvt].dayFromRef +
                                    today.serialNumber())) *
                                        (1.-getEventRecovery(events[iEvt]));
                        //and will sort later if buffer applies:
                        splitEventsBuffer.push_back(events[iEvt]);
                }
            }
            portfSimLoss = std::min(std::max(portfSimLoss - attachAmount, 0.),
                detachAmount - attachAmount);

            /* second pass; split is conditional to total losses within target
            losses/percentile:  */
            Real ptflCumulLoss = 0.;
            if(portfSimLoss > loss) {
                std::sort(splitEventsBuffer.begin(), splitEventsBuffer.end());
                //NOW THIS:
                split.assign(numLiveNames, 0.);
                /*  if the name triggered a loss in the portf limits assign
                this loss to that name..  */
                for(Size i=0; i<splitEventsBuffer.size(); i++) {
                    Size iName = splitEventsBuffer[i].nameIdx;
                    Real lossName =
            // allows amortizing (others should be like this)
            // basket_->remainingNotionals(Date(simsBuffer_[i].dayFromRef +
            //      today.serialNumber()))[iName] *
                        basket_->exposure(basket_->names()[iName],
                            Date(splitEventsBuffer[i].dayFromRef +
                                today.serialNumber())) *
                                (1.-getEventRecovery(splitEventsBuffer[i]));

                    Real tranchedLossBefore =
                        std::min(std::max(ptflCumulLoss - attachAmount, 0.),
                        detachAmount - attachAmount);
                    ptflCumulLoss += lossName;
                    Real tranchedLossAfter =
                        std::min(std::max(ptflCumulLoss - attachAmount, 0.),
                        detachAmount - attachAmount);
                    // assign new losses:
                    split[iName] += tranchedLossAfter - tranchedLossBefore;
                }
                for(Size iName=0; iName<numLiveNames; iName++) {
                    splitStats[iName].add(split[iName] /
                        std::min(std::max(ptflCumulLoss - attachAmount, 0.),
                            detachAmount - attachAmount)
