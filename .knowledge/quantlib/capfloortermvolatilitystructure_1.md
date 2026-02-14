                                                       Rate strike,
                                                           bool extrap) const {
        checkRange(d, extrap);
        Time t = timeFromReference(d);
        return volatility(t, strike, extrap);
    }

    inline
    Volatility CapFloorTermVolatilityStructure::volatility(Time t,
                                                           Rate strike,
                                                           bool extrap) const {
        checkRange(t, extrap);
        checkStrike(strike, extrap);
        return volatilityImpl(t, strike);
    }

}

#endif
