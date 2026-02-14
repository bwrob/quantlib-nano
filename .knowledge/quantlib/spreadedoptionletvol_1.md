ility::volatilityType() const {
        return baseVol_->volatilityType();
    }

    inline Real SpreadedOptionletVolatility::displacement() const {
        return baseVol_->displacement();
    }
}

#endif
