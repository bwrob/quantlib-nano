interpolationShifts_;
        VolatilityType volatilityType_;
    };

    // inline definitions

    inline Date SwaptionVolatilityMatrix::maxDate() const {
        return optionDates_.back();
    }

    inline Rate SwaptionVolatilityMatrix::minStrike() const {
        return -QL_MAX_REAL;
    }

    inline Rate SwaptionVolatilityMatrix::maxStrike() const {
        return QL_MAX_REAL;
    }

    inline const Period& SwaptionVolatilityMatrix::maxSwapTenor() const {
        return swapTenors_.back();
    }

    inline Volatility SwaptionVolatilityMatrix::volatilityImpl(Time optionTime,
                                                               Time swapLength,
                                                               Rate) const {
        calculate();
        return interpolation_(swapLength, optionTime, true);
    }

    inline VolatilityType SwaptionVolatilityMatrix::volatilityType() const {
        return volatilityType_;
    }

    inline Real SwaptionVolatilityMatrix::shiftImpl(Time optionTime,
                                                    Time swapLength) const {
        calculate();
        Real tmp = interpolationShifts_(swapLength, optionTime, true);
        return tmp;
    }
} // namespace QuantLib

#endif