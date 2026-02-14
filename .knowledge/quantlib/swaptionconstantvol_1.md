mpl(const Date&, const Period&, Rate) const override;
        Volatility volatilityImpl(Time, Time, Rate) const override;
        Real shiftImpl(Time optionTime, Time swapLength) const override;

      private:
        Handle<Quote> volatility_;
        Period maxSwapTenor_;
        VolatilityType volatilityType_;
        Real shift_;
    };


    // inline definitions

    inline Date ConstantSwaptionVolatility::maxDate() const {
        return Date::maxDate();
    }

    inline Real ConstantSwaptionVolatility::minStrike() const {
        return QL_MIN_REAL;
    }

    inline Real ConstantSwaptionVolatility::maxStrike() const {
        return QL_MAX_REAL;
    }

    inline const Period& ConstantSwaptionVolatility::maxSwapTenor() const {
        return maxSwapTenor_;
    }

    inline VolatilityType ConstantSwaptionVolatility::volatilityType() const {
        return volatilityType_;
    }

    inline Real ConstantSwaptionVolatility::shiftImpl(Time optionTime, Time swapLength) const {
        // consistency check
        SwaptionVolatilityStructure::shiftImpl(optionTime, swapLength);
        return shift_;
    }

}

#endif