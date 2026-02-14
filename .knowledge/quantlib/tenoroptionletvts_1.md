 // constructor
        TenorOptionletVTS(const Handle<OptionletVolatilityStructure>& baseVTS,
                          ext::shared_ptr<IborIndex> baseIndex,
                          ext::shared_ptr<IborIndex> targIndex,
                          ext::shared_ptr<CorrelationStructure> correlation);

        // Termstructure interface

        //! the latest date for which the curve can return values
        Date maxDate() const override { return baseVTS_->maxDate(); }

        // VolatilityTermstructure interface

        //! implements the actual smile calculation in derived classes
        ext::shared_ptr<SmileSection> smileSectionImpl(Time optionTime) const override {
            return ext::shared_ptr<SmileSection>(new TenorOptionletSmileSection(*this, optionTime));
        }
        //! implements the actual volatility calculation in derived classes
        Volatility volatilityImpl(Time optionTime, Rate strike) const override {
            return smileSection(optionTime)->volatility(strike);
        }


        //! the minimum strike for which the term structure can return vols
        Rate minStrike() const override { return baseVTS_->minStrike(); }
        //! the maximum strike for which the term structure can return vols
        Rate maxStrike() const override { return baseVTS_->maxStrike(); }

        // the methodology is designed for normal volatilities
        VolatilityType volatilityType() const override { return Normal; }
    };

    typedef TenorOptionletVTS::CorrelationStructure TenorOptionletVTSCorrelationStructure;

}

#endif
