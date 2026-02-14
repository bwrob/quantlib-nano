OfStrikes(),
                       "too few strikes (" << nStrikes_
                                           << ") required are at least "
                                           << requiredNumberOfStrikes());
            SwaptionVolatilityDiscrete::performCalculations();
        }
        //@}
        VolatilityType volatilityType() const override;

      protected:
        void registerWithVolatilitySpread();
        virtual Size requiredNumberOfStrikes() const { return 2; }
        Volatility volatilityImpl(Time optionTime, Time swapLength, Rate strike) const override;
        Volatility
        volatilityImpl(const Date& optionDate, const Period& swapTenor, Rate strike) const override;
        Real shiftImpl(Time optionTime, Time swapLength) const override;
        Handle<SwaptionVolatilityStructure> atmVol_;
        Size nStrikes_;
        std::vector<Spread> strikeSpreads_;
        mutable std::vector<Rate> localStrikes_;
        mutable std::vector<Volatility> localSmile_;
        std::vector<std::vector<Handle<Quote> > > volSpreads_;
        ext::shared_ptr<SwapIndex> swapIndexBase_, shortSwapIndexBase_;
        bool vegaWeightedSmileFit_;
    };

    // inline

    inline VolatilityType SwaptionVolatilityCube::volatilityType() const {
        return atmVol_->volatilityType();
    }

    inline Volatility SwaptionVolatilityCube::volatilityImpl(
                                                        Time optionTime,
                                                        Time swapLength,
                                                        Rate strike) const {
        return smileSectionImpl(optionTime, swapLength)->volatility(strike);
    }

    inline Volatility SwaptionVolatilityCube::volatilityImpl(
                                                    const Date& optionDate,
                                                    const Period& swapTenor,
                                                    Rate strike) const {
        return smileSectionImpl(optionDate, swapTenor)->volatility(strike);
    }

    inline Real SwaptionVolatilityCube::shiftImpl(Time optionTime,
                                                  Time swapLength) const {
        return atmVol_->shift(optionTime, swapLength);
    }
}

#endif