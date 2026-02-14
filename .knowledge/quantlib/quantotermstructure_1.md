BlackVolTS_);
    }

    inline DayCounter QuantoTermStructure::dayCounter() const {
        return underlyingDividendTS_->dayCounter();
    }

    inline Calendar QuantoTermStructure::calendar() const {
        return underlyingDividendTS_->calendar();
    }

    inline Natural QuantoTermStructure::settlementDays() const {
        return underlyingDividendTS_->settlementDays();
    }

    inline const Date& QuantoTermStructure::referenceDate() const {
        return underlyingDividendTS_->referenceDate();
    }

    inline Date QuantoTermStructure::maxDate() const {
        Date maxDate = std::min(underlyingDividendTS_->maxDate(),
                                riskFreeTS_->maxDate());
        maxDate = std::min(maxDate, foreignRiskFreeTS_->maxDate());
        maxDate = std::min(maxDate, underlyingBlackVolTS_->maxDate());
        maxDate = std::min(maxDate, exchRateBlackVolTS_->maxDate());
        return maxDate;
    }

    inline Rate QuantoTermStructure::zeroYieldImpl(Time t) const {
        // warning: here it is assumed that all TS have the same daycount.
        //          It should be QL_REQUIREd
        return underlyingDividendTS_->zeroRate(t, Continuous, NoFrequency, true).rate()
            +            riskFreeTS_->zeroRate(t, Continuous, NoFrequency, true).rate()
            -     foreignRiskFreeTS_->zeroRate(t, Continuous, NoFrequency, true).rate()
            + underlyingExchRateCorrelation_
            * underlyingBlackVolTS_->blackVol(t, strike_, true)
            *   exchRateBlackVolTS_->blackVol(t, exchRateATMlevel_, true);
    }

}


#endif
