wdRates[i] -1.0;
                // add observation
                statistics.add(fwdRatesDiff.begin(), fwdRatesDiff.end());
            }
            else
                isFirst = false;

            // Store last calculated forward rates
            std::swap(prevFwdRates, fwdRates);

        }
    }

    class HistoricalForwardRatesAnalysis {
      public:
        virtual ~HistoricalForwardRatesAnalysis() = default;
        virtual const std::vector<Date>& skippedDates() const = 0;
        virtual const std::vector<std::string>& skippedDatesErrorMessage() const = 0;
        virtual const std::vector<Date>& failedDates() const = 0;
        virtual const std::vector<std::string>& failedDatesErrorMessage() const = 0;
        virtual const std::vector<Period>& fixingPeriods() const = 0;
    };

    //! %Historical correlation class
    template<class Traits, class Interpolator>
    class HistoricalForwardRatesAnalysisImpl : public HistoricalForwardRatesAnalysis {
      public:
        HistoricalForwardRatesAnalysisImpl(
            ext::shared_ptr<SequenceStatistics> stats,
            const Date& startDate,
            const Date& endDate,
            const Period& step,
            const ext::shared_ptr<InterestRateIndex>& fwdIndex,
            const Period& initialGap,
            const Period& horizon,
            const std::vector<ext::shared_ptr<IborIndex> >& iborIndexes,
            const std::vector<ext::shared_ptr<SwapIndex> >& swapIndexes,
            const DayCounter& yieldCurveDayCounter,
            Real yieldCurveAccuracy);
        HistoricalForwardRatesAnalysisImpl() = default;
        ;
        const std::vector<Date>& skippedDates() const override;
        const std::vector<std::string>& skippedDatesErrorMessage() const override;
        const std::vector<Date>& failedDates() const override;
        const std::vector<std::string>& failedDatesErrorMessage() const override;
        const std::vector<Period>& fixingPeriods() const override;
        //const ext::shared_ptr<SequenceStatistics>& stats() const;
      private:
        // calculated data
        ext::shared_ptr<SequenceStatistics> stats_;
        std::vector<Date> skippedDates_;
        std::vector<std::string> skippedDatesErrorMessage_;
        std::vector<Date> failedDates_;
        std::vector<std::string> failedDatesErrorMessage_;
        std::vector<Period> fixingPeriods_;
    };

    // inline
    template<class Traits, class Interpolator>
    const std::vector<Period>&
    HistoricalForwardRatesAnalysisImpl<Traits, Interpolator>::fixingPeriods() const {
        return fixingPeriods_;
    }

    template<class Traits, class Interpolator>
    inline const std::vector<Date>&
    HistoricalForwardRatesAnalysisImpl<Traits, Interpolator>::skippedDates() const {
        return skippedDates_;
    }

    template<class Traits, class Interpolator>
    inline const std::vector<std::string>&
    HistoricalForwardRatesAnalysisImpl<Traits, Interpolator>::skippedDatesErrorMessage() const {
        return skippedDatesErrorMessage_;
    }

    template<class Traits, class Interpolator>
    inline const std::vector<Date>&
    HistoricalForwardRatesAnalysisImpl<Traits, Interpolator>::failedDates() const {
        return failedDates_;
    }

    template<class Traits, class Interpolator>
    inline const std::vector<std::string>&
    HistoricalForwardRatesAnalysisImpl<Traits, Interpolator>::failedDatesErrorMessage() const {
        return failedDatesErrorMessage_;
    }

    //inline const ext::shared_ptr<SequenceStatistics>&
    //HistoricalForwardRatesAnalysis::stats() const {
    //    return stats_;
    //}
    template <class Traits, class Interpolator>
    HistoricalForwardRatesAnalysisImpl<Traits, Interpolator>::HistoricalForwardRatesAnalysisImpl(
        ext::shared_ptr<SequenceStatistics> stats,
        const Date& startDate,
        const Date& endDate,
        const Period& step,
        const ext::shared_ptr<InterestRateIndex>& fwdIndex,
        const 