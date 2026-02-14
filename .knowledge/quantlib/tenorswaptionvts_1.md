can return values
        Date maxDate() const override { return baseVTS_->maxDate(); }

        // SwaptionVolatility interface

        //! the minimum strike for which the term structure can return vols
        Rate minStrike() const override { return baseVTS_->minStrike(); }
        //! the maximum strike for which the term structure can return vols
        Rate maxStrike() const override { return baseVTS_->maxStrike(); }


        // SwaptionVolatilityStructure interface

        //! the largest length for which the term structure can return vols
        const Period& maxSwapTenor() const override { return baseVTS_->maxSwapTenor(); }

        ext::shared_ptr<SmileSection> smileSectionImpl(Time optionTime,
                                                       Time swapLength) const override {
            return ext::shared_ptr<SmileSection>(
                new TenorSwaptionSmileSection(*this, optionTime, swapLength));
        }

        Volatility volatilityImpl(Time optionTime, Time swapLength, Rate strike) const override {
            return smileSectionImpl(optionTime, swapLength)->volatility(strike, Normal, 0.0);
        }

        // the methodology is designed for normal volatilities
        VolatilityType volatilityType() const override { return Normal; }
    };

}

#endif