ults*) const override;

      private:
        void setupExpired() const override;

        ext::shared_ptr<Basket> basket_;
        Size n_;
        Protection::Side side_;
        Real nominal_;
        Schedule premiumSchedule_;
        Rate premiumRate_;
        Rate upfrontRate_;
        DayCounter dayCounter_;
        bool settlePremiumAccrual_;

        Leg premiumLeg_;/////////////////// LEG AND SCHEDULE BOTH MEMBERS..... REVISE THIS!

        // results
        mutable Rate premiumValue_;
        mutable Real protectionValue_;
        mutable Real upfrontPremiumValue_;
        mutable Real fairPremium_;
        mutable Real errorEstimate_;
    };



    class NthToDefault::arguments : public virtual PricingEngine::arguments {
    public:
        arguments() : side(Protection::Side(-1)),
                      premiumRate(Null<Real>()),
                      upfrontRate(Null<Real>()) {}
        void validate() const override;

        ext::shared_ptr<Basket> basket;
        Protection::Side side;
        Leg premiumLeg;

        Size ntdOrder;
        bool settlePremiumAccrual;
        Real notional;// ALL NAMES WITH THE SAME WEIGHT, NOTIONAL IS NOT MAPPED TO THE BASKET HERE, this does not have to be that way, its perfectly possible to have irreg notionals...
        Real premiumRate;
        Rate upfrontRate;
    };

    class NthToDefault::results : public Instrument::results {
    public:
      void reset() override;
      Real premiumValue;
      Real protectionValue;
      Real upfrontPremiumValue;
      Real fairPremium;
      Real errorEstimate;
    };

    //! NTD base engine
    class NthToDefault::engine :
        public GenericEngine<NthToDefault::arguments,
                             NthToDefault::results> { };

}

#endif
