at factor.

            \todo: allow for extra payment flags, arbitrary upfront
                   payment date...
        */
        SyntheticCDO (const ext::shared_ptr<Basket>& basket,
                      Protection::Side side,
                      Schedule schedule,
                      Rate upfrontRate,
                      Rate runningRate,
                      const DayCounter& dayCounter,
                      BusinessDayConvention paymentConvention,
                      ext::optional<Real> notional = ext::nullopt);

        const ext::shared_ptr<Basket>& basket() const { return basket_; }

        bool isExpired() const override;
        Rate fairPremium() const;
        Rate fairUpfrontPremium() const;
        Rate premiumValue () const;
        Rate protectionValue () const;
        Real premiumLegNPV() const;
        Real protectionLegNPV() const;
        /*!
          Total outstanding tranche notional, not wiped out
        */
        Real remainingNotional() const;
        /*! The number of times the contract contains the portfolio tranched
                notional.
        */
        Real leverageFactor() const {
            return leverageFactor_;
        }
        //! Last protection date.
        const Date& maturity() const {
            return ext::dynamic_pointer_cast<FixedRateCoupon>(
                normalizedLeg_.back())->accrualEndDate();
        }
        /*! The Gaussian Copula LHP implied correlation that makes the
            contract zero value. This is for a flat correlation along
            time and portfolio loss level.
        */
        Real implicitCorrelation(const std::vector<Real>& recoveries,
            const Handle<YieldTermStructure>& discountCurve,
            Real targetNPV = 0.,
            Real accuracy = 1.0e-3) const;

        /*!
          Expected tranche loss for all payment dates
         */
        std::vector<Real> expectedTrancheLoss() const;
        Size error () const;

        void setupArguments(PricingEngine::arguments*) const override;
        void fetchResults(const PricingEngine::results*) const override;

      private:
        void setupExpired() const override;

        ext::shared_ptr<Basket> basket_;
        Protection::Side side_;
        Leg normalizedLeg_;

        Rate upfrontRate_;
        Rate runningRate_;
        const Real leverageFactor_;
        DayCounter dayCounter_;
        BusinessDayConvention paymentConvention_;

        mutable Real premiumValue_;
        mutable Real protectionValue_;
        mutable Real upfrontPremiumValue_;
        mutable Real remainingNotional_;
        mutable Size error_;
        mutable std::vector<Real> expectedTrancheLoss_;
    };

    class SyntheticCDO::arguments : public virtual PricingEngine::arguments {
    public:
        arguments() : side(Protection::Side(-1)),
                      upfrontRate(Null<Real>()),
                      runningRate(Null<Real>()) {}
        void validate() const override;

        ext::shared_ptr<Basket> basket;
        Protection::Side side;
        Leg normalizedLeg;

        Rate upfrontRate;
        Rate runningRate;
        Real leverageFactor;
        DayCounter dayCounter;
        BusinessDayConvention paymentConvention;
    };

    class SyntheticCDO::results : public Instrument::results {
    public:
      void reset() override;
      Real premiumValue;
      Real protectionValue;
      Real upfrontPremiumValue;
      Real remainingNotional;
      Real xMin, xMax;
      Size error;
      /* Expected tranche losses affecting this tranche coupons. Notice this
      number might be below the actual basket losses, since the cdo protection
      might start after basket inception (forward start CDO)*/
      std::vector<Real> expectedTrancheLoss;
    };


    //! CDO base engine
    class SyntheticCDO::engine :
        public GenericEngine<SyntheticCDO::arguments,
                             SyntheticCDO::results> { };

}

#endif

#endif