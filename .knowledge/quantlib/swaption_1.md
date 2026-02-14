        void setupArguments(PricingEngine::arguments*) const override;
        //@}
        //! \name Inspectors
        //@{
        Settlement::Type settlementType() const { return settlementType_; }
        Settlement::Method settlementMethod() const {
            return settlementMethod_;
        }
        Swap::Type type() const { return swap_->type(); }
        const ext::shared_ptr<FixedVsFloatingSwap>& underlying() const {
            return swap_;
        }
        //@}
        //! implied volatility
        Volatility impliedVolatility(
                              Real price,
                              const Handle<YieldTermStructure>& discountCurve,
                              Volatility guess,
                              Real accuracy = 1.0e-4,
                              Natural maxEvaluations = 100,
                              Volatility minVol = 1.0e-7,
                              Volatility maxVol = 4.0,
                              VolatilityType type = ShiftedLognormal,
                              Real displacement = 0.0,
                              PriceType priceType = Spot) const;
      private:
        // arguments
        ext::shared_ptr<FixedVsFloatingSwap> swap_;
        //Handle<YieldTermStructure> termStructure_;
        Settlement::Type settlementType_;
        Settlement::Method settlementMethod_;
        // until we remove underlyingSwap();
        ext::shared_ptr<VanillaSwap> vanilla_;
    };

    //! %Arguments for swaption calculation
    class Swaption::arguments : public FixedVsFloatingSwap::arguments,
                                public Option::arguments {
      public:
        arguments() = default;
        ext::shared_ptr<FixedVsFloatingSwap> swap;
        Settlement::Type settlementType = Settlement::Physical;
        Settlement::Method settlementMethod;
        void validate() const override;
    };

    //! base class for swaption engines
    class Swaption::engine
        : public GenericEngine<Swaption::arguments, Swaption::results> {};

}

#endif