Period& initialGap,
        const Period& horizon,
        const std::vector<ext::shared_ptr<IborIndex> >& iborIndexes,
        const std::vector<ext::shared_ptr<SwapIndex> >& swapIndexes,
        const DayCounter& yieldCurveDayCounter,
        Real yieldCurveAccuracy)
    : stats_(std::move(stats)) {
        historicalForwardRatesAnalysis<Traits,
                                       Interpolator>(
                    *stats_,
                    skippedDates_, skippedDatesErrorMessage_,
                    failedDates_, failedDatesErrorMessage_,
                    fixingPeriods_, startDate, endDate, step,
                    fwdIndex, initialGap, horizon,
                    iborIndexes, swapIndexes,
                    yieldCurveDayCounter, yieldCurveAccuracy);
    }
}

#endif
