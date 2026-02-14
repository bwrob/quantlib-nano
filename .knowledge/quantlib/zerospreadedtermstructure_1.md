d_);
    }

    inline ZeroSpreadedTermStructure::ZeroSpreadedTermStructure(Handle<YieldTermStructure> h,
                                                                Handle<Quote> spread,
                                                                Compounding comp,
                                                                Frequency freq,
                                                                const DayCounter& dc)
    : ZeroSpreadedTermStructure(std::move(h), std::move(spread), comp, freq) {}

    inline DayCounter ZeroSpreadedTermStructure::dayCounter() const {
        return originalCurve_->dayCounter();
    }

    inline Calendar ZeroSpreadedTermStructure::calendar() const {
        return originalCurve_->calendar();
    }

    inline Natural ZeroSpreadedTermStructure::settlementDays() const {
        return originalCurve_->settlementDays();
    }

    inline const Date& ZeroSpreadedTermStructure::referenceDate() const {
        return originalCurve_->referenceDate();
    }

    inline Date ZeroSpreadedTermStructure::maxDate() const {
        return originalCurve_->maxDate();
    }

    inline Time ZeroSpreadedTermStructure::maxTime() const {
        return originalCurve_->maxTime();
    }

    inline void ZeroSpreadedTermStructure::update() {
        if (!originalCurve_.empty()) {
            YieldTermStructure::update();
            enableExtrapolation(originalCurve_->allowsExtrapolation());
        } else {
            /* The implementation inherited from YieldTermStructure
               asks for our reference date, which we don't have since
               the original curve is still not set. Therefore, we skip
               over that and just call the base-class behavior. */
            // NOLINTNEXTLINE(bugprone-parent-virtual-call)
            TermStructure::update();
        }
    }

    inline Rate ZeroSpreadedTermStructure::zeroYieldImpl(Time t) const {
        // to be fixed: user-defined daycounter should be used
        InterestRate zeroRate =
            originalCurve_->zeroRate(t, comp_, freq_, true);
        InterestRate spreadedRate(zeroRate + spread_->value(),
                                  zeroRate.dayCounter(),
                                  zeroRate.compounding(),
                                  zeroRate.frequency());
        return spreadedRate.equivalentRate(Continuous, NoFrequency, t);
    }

    inline Rate ZeroSpreadedTermStructure::forwardImpl(Time t) const {
        return originalCurve_->forwardRate(t, t, comp_, freq_, true)
            + spread_->value();
    }

}

#endif
