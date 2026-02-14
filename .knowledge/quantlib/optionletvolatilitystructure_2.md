const {
        checkRange(optionDate, extrapolate);
        checkStrike(strike, extrapolate);
        return volatilityImpl(optionDate, strike);
    }

    inline Volatility
    OptionletVolatilityStructure::volatility(Time optionTime,
                                             Rate strike,
                                             bool extrapolate) const {
        checkRange(optionTime, extrapolate);
        checkStrike(strike, extrapolate);
        return volatilityImpl(optionTime, strike);
    }

    inline ext::shared_ptr<SmileSection>
    OptionletVolatilityStructure::smileSection(const Date& optionDate,
                                               bool extrapolate) const {
        checkRange(optionDate, extrapolate);
        return smileSectionImpl(optionDate);
    }

    inline ext::shared_ptr<SmileSection>
    OptionletVolatilityStructure::smileSection(Time optionTime,
                                               bool extrapolate) const {
        checkRange(optionTime, extrapolate);
        return smileSectionImpl(optionTime);
    }

    // 4. default implementation of Date-based xxxImpl methods
    //    relying on the equivalent Time-based methods
    inline ext::shared_ptr<SmileSection>
    OptionletVolatilityStructure::smileSectionImpl(const Date& optionDate) const {
        return smileSectionImpl(timeFromReference(optionDate));
    }

    inline Volatility
    OptionletVolatilityStructure::volatilityImpl(const Date& optionDate,
                                                 Rate strike) const {
        return volatilityImpl(timeFromReference(optionDate), strike);
    }

    inline VolatilityType
    OptionletVolatilityStructure::volatilityType() const {
        return ShiftedLognormal;
    }

    inline Real OptionletVolatilityStructure::displacement() const {
        return 0.0;
    }
}

#endif