aseVol_->maxSwapTenor();
    }

    inline Real SpreadedSwaptionVolatility::shiftImpl(Time optionTime,
                                                  Time swapLength) const {
        return baseVol_->shift(optionTime, swapLength, true);
    }

    inline VolatilityType SpreadedSwaptionVolatility::volatilityType() const {
        return baseVol_->volatilityType();
    }



}

#endif
