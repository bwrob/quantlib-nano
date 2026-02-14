SectionImpl(optionDate, swapTenor);
    }

    inline ext::shared_ptr<SmileSection>
    SwaptionVolatilityStructure::smileSection(Time optionTime,
                                              const Period& swapTenor,
                                              bool extrapolate) const {
        checkSwapTenor(swapTenor, extrapolate);
        checkRange(optionTime, extrapolate);
        return smileSection(optionTime, swapLength(swapTenor));
    }

    inline ext::shared_ptr<SmileSection>
    SwaptionVolatilityStructure::smileSection(const Period& optionTenor,
                                              Time swapLength,
                                              bool extrapolate) const {
        checkSwapTenor(swapLength, extrapolate);
        Date optionDate = optionDateFromTenor(optionTenor);
        checkRange(optionDate, extrapolate);
        return smileSection(optionDate, swapLength);
    }

    inline ext::shared_ptr<SmileSection>
    SwaptionVolatilityStructure::smileSection(const Date& optionDate,
                                              Time swapLength,
                                              bool extrapolate) const {
        checkSwapTenor(swapLength, extrapolate);
        checkRange(optionDate, extrapolate);
        return smileSection(timeFromReference(optionDate), swapLength);
    }

    inline ext::shared_ptr<SmileSection>
    SwaptionVolatilityStructure::smileSection(Time optionTime,
                                              Time swapLength,
                                              bool extrapolate) const {
        checkSwapTenor(swapLength, extrapolate);
        checkRange(optionTime, extrapolate);
        return smileSectionImpl(optionTime, swapLength);
    }

    // 4. default implementation of Date-based xxxImpl methods
    //    relying on the equivalent Time-based methods
    inline ext::shared_ptr<SmileSection>
    SwaptionVolatilityStructure::smileSectionImpl(const Date& optionDate,
                                                  const Period& swapT) const {
        return smileSectionImpl(timeFromReference(optionDate),
                                swapLength(swapT));
    }

    inline Volatility
    SwaptionVolatilityStructure::volatilityImpl(const Date& optionDate,
                                                const Period& swapTenor,
                                                Rate strike) const {
        return volatilityImpl(timeFromReference(optionDate),
                              swapLength(swapTenor),
                              strike);
    }

    inline Real
    SwaptionVolatilityStructure::shiftImpl(const Date &optionDate,
                                           const Period &swapTenor) const {
        return shiftImpl(timeFromReference(optionDate), swapLength(swapTenor));
    }

    inline Real SwaptionVolatilityStructure::shiftImpl(Time, Time) const {
        QL_REQUIRE(
            volatilityType() == ShiftedLognormal,
            "shift parameter only makes sense for lognormal volatilities");
        return 0.0;
    }

    inline Time SwaptionVolatilityStructure::maxSwapLength() const {
        return swapLength(maxSwapTenor());
    }

}

#endif
