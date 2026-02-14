                                               Time bondLength,
                                                     Rate strike,
                                                     bool extrapolate) const {
        checkRange(optionTime, bondLength, strike, extrapolate);
        return volatilityImpl(optionTime, bondLength, strike);
    }


    inline Real CallableBondVolatilityStructure::blackVariance(
                                                     Time optionTime,
                                                     Time bondLength,
                                                     Rate strike,
                                                     bool extrapolate) const {
        checkRange(optionTime, bondLength, strike, extrapolate);
        Volatility vol = volatilityImpl(optionTime, bondLength, strike);
        return vol*vol*optionTime;
    }


    inline Volatility CallableBondVolatilityStructure::volatility(
                                                     const Date& optionDate,
                                                     const Period& bondTenor,
                                                     Rate strike,
                                                     bool extrapolate) const {
        checkRange(optionDate, bondTenor, strike, extrapolate);
        return volatilityImpl(optionDate, bondTenor, strike);
    }

    inline Real CallableBondVolatilityStructure::blackVariance(
                                                     const Date& optionDate,
                                                     const Period& bondTenor,
                                                     Rate strike,
                                                     bool extrapolate) const {
        Volatility vol =
            volatility(optionDate, bondTenor, strike, extrapolate);
        const std::pair<Time, Time> p = convertDates(optionDate, bondTenor);
        return vol*vol*p.first;
    }

    inline Volatility CallableBondVolatilityStructure::volatility(
                                                    const Period& optionTenor,
                                                    const Period& bondTenor,
                                                    Rate strike,
                                                    bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return volatility(optionDate, bondTenor, strike, extrapolate);
    }

    inline Real CallableBondVolatilityStructure::blackVariance(
                                                    const Period& optionTenor,
                                                    const Period& bondTenor,
                                                    Rate strike,
                                                    bool extrapolate) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        Volatility vol =
            volatility(optionDate, bondTenor, strike, extrapolate);
        const std::pair<Time, Time> p = convertDates(optionDate, bondTenor);
        return vol*vol*p.first;
    }


    inline ext::shared_ptr<SmileSection>
    CallableBondVolatilityStructure::smileSection(
                                              const Period& optionTenor,
                                              const Period& bondTenor) const {
        Date optionDate = optionDateFromTenor(optionTenor);
        return smileSection(optionDate, bondTenor);
    }


    inline void CallableBondVolatilityStructure::checkRange(
        Time optionTime, Time bondLength, Rate k, bool extrapolate) const {
        TermStructure::checkRange(optionTime, extrapolate);
        QL_REQUIRE(bondLength >= 0.0,
                   "negative bondLength (" << bondLength << ") given");
        QL_REQUIRE(extrapolate || allowsExtrapolation() ||
                   bondLength <= maxBondLength(),
                   "bondLength (" << bondLength << ") is past max curve bondLength ("
                   << maxBondLength() << ")");

