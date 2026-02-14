*v*optionTime;
    }

    // 3. relying on xxxImpl methods
    inline Volatility
    SwaptionVolatilityStructure::volatility(const Date& optionDate,
                                            const Period& swapTenor,
                                            Rate strike,
                                            bool extrapolate) const {
        checkSwapTenor(swapTenor, extrapolate);
        checkRange(optionDate, extrapolate);
        checkStrike(strike, extrapolate);
        return volatilityImpl(optionDate, swapTenor, strike);
    }

    inline Volatility
    SwaptionVolatilityStructure::volatility(const Date& optionDate,
                                            Time swapLength,
                                            Rate strike,
                                            bool extrapolate) const {
        checkSwapTenor(swapLength, extrapolate);
        checkRange(optionDate, extrapolate);
        checkStrike(strike, extrapolate);
        Time optionTime = timeFromReference(optionDate);
        return volatilityImpl(optionTime, swapLength, strike);
    }

    inline Volatility
    SwaptionVolatilityStructure::volatility(Time optionTime,
                                            const Period& swapTenor,
                                            Rate strike,
                                            bool extrapolate) const {
        checkSwapTenor(swapTenor, extrapolate);
        checkRange(optionTime, extrapolate);
        checkStrike(strike, extrapolate);
        Time length = swapLength(swapTenor);
        return volatilityImpl(optionTime, length, strike);
    }

    inline Volatility
    SwaptionVolatilityStructure::volatility(Time optionTime,
                                            Time swapLength,
                                            Rate strike,
                                            bool extrapolate) const {
        checkSwapTenor(swapLength, extrapolate);
        checkRange(optionTime, extrapolate);
        checkStrike(strike, extrapolate);
        return volatilityImpl(optionTime, swapLength, strike);
    }

    inline Real
    SwaptionVolatilityStructure::shift(const Date& optionDate,
                                            const Period& swapTenor,
                                            bool extrapolate) const {
        checkSwapTenor(swapTenor, extrapolate);
        checkRange(optionDate, extrapolate);
        return shiftImpl(optionDate, swapTenor);
    }

    inline Real
    SwaptionVolatilityStructure::shift(const Date& optionDate,
                                            Time swapLength,
                                            bool extrapolate) const {
        checkSwapTenor(swapLength, extrapolate);
        checkRange(optionDate, extrapolate);
        Time optionTime = timeFromReference(optionDate);
        return shiftImpl(optionTime, swapLength);
    }

    inline Real
    SwaptionVolatilityStructure::shift(Time optionTime,
                                            const Period& swapTenor,
                                            bool extrapolate) const {
        checkSwapTenor(swapTenor, extrapolate);
        checkRange(optionTime, extrapolate);
        Time length = swapLength(swapTenor);
        return shiftImpl(optionTime, length);
    }

    inline Real
    SwaptionVolatilityStructure::shift(Time optionTime,
                                            Time swapLength,
                                            bool extrapolate) const {
        checkSwapTenor(swapLength, extrapolate);
        checkRange(optionTime, extrapolate);
        return shiftImpl(optionTime, swapLength);
    }

    inline ext::shared_ptr<SmileSection>
    SwaptionVolatilityStructure::smileSection(const Date& optionDate,
                                              const Period& swapTenor,
                                              bool extrapolate) const {
        checkSwapTenor(swapTenor, extrapolate);
        checkRange(optionDate, extrapolate);
        return smile
