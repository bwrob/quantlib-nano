swap!=swapIndexes.end(); ++swap) {
            ext::shared_ptr<SimpleQuote> quote(new SimpleQuote);
            swapQuotes.push_back(quote);
            Handle<Quote> quoteHandle(quote);
            rateHelpers.push_back(ext::shared_ptr<RateHelper> (new
                SwapRateHelper(quoteHandle,
                               (*swap)->tenor(),
                               (*swap)->fixingCalendar(),
                               (*swap)->fixedLegTenor().frequency(),
                               (*swap)->fixedLegConvention(),
                               (*swap)->dayCounter(),
                               (*swap)->iborIndex())));
        }

        // Set up the forward rates time grid
        Period indexTenor = fwdIndex->tenor();
        Period fixingPeriod = initialGap;
        while (fixingPeriod<=horizon) {
            fixingPeriods.push_back(fixingPeriod);
            fixingPeriod += indexTenor;
        }

        Size nRates = fixingPeriods.size();
        statistics.reset(nRates);
        std::vector<Rate> fwdRates(nRates);
        std::vector<Rate> prevFwdRates(nRates);
        std::vector<Rate> fwdRatesDiff(nRates);
        DayCounter indexDayCounter = fwdIndex->dayCounter();
        Calendar cal = fwdIndex->fixingCalendar();

        // Bootstrap the yield curve at the currentDate
        Natural settlementDays = 0;
        typename PiecewiseYieldCurve<Traits, Interpolator>::bootstrap_type bootstrap(yieldCurveAccuracy);
        PiecewiseYieldCurve<Traits, Interpolator> yc(settlementDays,
                                                     cal,
                                                     rateHelpers,
                                                     yieldCurveDayCounter,
                                                     std::vector<Handle<Quote> >(),
                                                     std::vector<Date>(),
                                                     i,
                                                     bootstrap);

        // start with a valid business date
        Date currentDate = cal.advance(startDate, 1*Days, Following);
        bool isFirst = true;
        // Loop over the historical dataset
        for (; currentDate<=endDate;
            currentDate = cal.advance(currentDate, step, Following)) {

            // move the evaluationDate to currentDate
            // and update ratehelpers dates...
            Settings::instance().evaluationDate() = currentDate;

            try {
                // update the quotes...
                for (Size i=0; i<iborIndexes.size(); ++i) {
                    Rate fixing = iborIndexes[i]->fixing(currentDate, false);
                    iborQuotes[i]->setValue(fixing);
                }
                for (Size i=0; i<swapIndexes.size(); ++i) {
                    Rate fixing = swapIndexes[i]->fixing(currentDate, false);
                    swapQuotes[i]->setValue(fixing);
                }
            } catch (std::exception& e) {
                skippedDates.push_back(currentDate);
                skippedDatesErrorMessage.emplace_back(e.what());
                continue;
            }

            try {
                for (Size i=0; i<nRates; ++i) {
                    // Time-to-go forwards
                    Date d = currentDate + fixingPeriods[i];
                    fwdRates[i] = yc.forwardRate(d,
                                                 indexTenor,
                                                 indexDayCounter,
                                                 Simple);
                }
            } catch (std::exception& e) {
                failedDates.push_back(currentDate);
                failedDatesErrorMessage.emplace_back(e.what());
                continue;
            }

            // From 2nd step onwards, calculate forward rate
            // relative differences
            if (!isFirst){
                for (Size i=0; i<nRates; ++i)
                    fwdRatesDiff[i] = fwdRates[i]/prevF