nge(t, extrapolate);
        return defaultDensityImpl(t);
    }

    inline
    Rate DefaultProbabilityTermStructure::hazardRate(const Date& d,
                                                     bool extrapolate) const {
        return hazardRate(timeFromReference(d), extrapolate);
    }

   inline
    Rate DefaultProbabilityTermStructure::hazardRateImpl(Time t) const {
        Probability S = survivalProbability(t, true);
        return S == 0.0 ? Rate(0.0) : defaultDensity(t, true)/S;
    }

    inline Rate DefaultProbabilityTermStructure::hazardRate(Time t,
                                                            bool extrapolate) const {
        checkRange(t, extrapolate);
        return hazardRateImpl(t);
    }

    inline
    const std::vector<Date>&
    DefaultProbabilityTermStructure::jumpDates() const {
        return this->jumpDates_;
    }

    inline
    const std::vector<Time>&
    DefaultProbabilityTermStructure::jumpTimes() const {
        return this->jumpTimes_;
    }

    inline void DefaultProbabilityTermStructure::update() {
        TermStructure::update();
        if (referenceDate() != latestReference_)
            setJumps();
    }

}

#endif
