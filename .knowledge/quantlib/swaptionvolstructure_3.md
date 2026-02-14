e,
                                            bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return volatility(optionDate, swapLength, strike, extrapolate);
    }

    inline
    Real SwaptionVolatilityStructure::blackVariance(const Period& optionTenor,
                                                    const Period& swapTenor,
                                                    Rate strike,
                                                    bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return blackVariance(optionDate, swapTenor, strike, extrapolate);
    }

    inline
    Real SwaptionVolatilityStructure::blackVariance(const Period& optionTenor,
                                                    Time swapLength,
                                                    Rate strike,
                                                    bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return blackVariance(optionDate, swapLength, strike, extrapolate);
    }

    inline
    Real SwaptionVolatilityStructure::shift(const Period& optionTenor,
                                            const Period& swapTenor,
                                            bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return shift(optionDate, swapTenor, extrapolate);
    }

    inline
    Real SwaptionVolatilityStructure::shift(const Period& optionTenor,
                                            Time swapLength,
                                            bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return shift(optionDate, swapLength, extrapolate);
    }

    inline ext::shared_ptr<SmileSection>
    SwaptionVolatilityStructure::smileSection(const Period& optionTenor,
                                              const Period& swapTenor,
                                              bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return smileSection(optionDate, swapTenor, extrapolate);
    }

    // 2. blackVariance methods rely on volatility methods
    inline
    Real SwaptionVolatilityStructure::blackVariance(const Date& optionDate,
                                                    const Period& swapTenor,
                                                    Rate strike,
                                                    bool extrapolate) const {
        Volatility v = volatility(optionDate, swapTenor, strike, extrapolate);
        Time optionTime = timeFromReference(optionDate);
        return v*v*optionTime;
    }

    inline
    Real SwaptionVolatilityStructure::blackVariance(Time optionTime,
                                                    const Period& swapTenor,
                                                    Rate strike,
                                                    bool extrapolate) const {
        Volatility v = volatility(optionTime, swapTenor, strike, extrapolate);
        return v*v*optionTime;
    }

    inline
    Real SwaptionVolatilityStructure::blackVariance(const Date& optionDate,
                                                    Time swapLength,
                                                    Rate strike,
                                                    bool extrapolate) const {
        Volatility v = volatility(optionDate, swapLength, strike, extrapolate);
        Time optionTime = timeFromReference(optionDate);
        return v*v*optionTime;
    }

    inline
    Real SwaptionVolatilityStructure::blackVariance(Time optionTime,
                                                    Time swapLength,
                                                    Rate strike,
                                                    bool extrapolate) const {
        Volatility v = volatility(optionTime, swapLength, strike, extrapolate);
        return v