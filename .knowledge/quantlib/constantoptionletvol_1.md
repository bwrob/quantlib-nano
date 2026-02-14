OptionletVolatility::maxDate() const {
        return Date::maxDate();
    }

    inline Real ConstantOptionletVolatility::minStrike() const {
        return QL_MIN_REAL;
    }

    inline Real ConstantOptionletVolatility::maxStrike() const {
        return QL_MAX_REAL;
    }

    inline VolatilityType
    ConstantOptionletVolatility::volatilityType() const {
        return type_;
    }

    inline Real ConstantOptionletVolatility::displacement() const {
        return displacement_;
    }
}

#endif
