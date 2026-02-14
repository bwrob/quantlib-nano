astic sense. When the bond settlement date is used the coupon
            is the already-fixed not-yet-paid one.

            The current bond settlement is used if no date is given.
        */
        virtual Rate nextCouponRate(Date d = Date()) const;

        //! Previous coupon already paid at a given date
        /*! Expected previous coupon: depending on (the bond and) the given
            date the coupon can be historic, deterministic or expected in a
            stochastic sense. When the bond settlement date is used the coupon
            is the last paid one.

            The current bond settlement is used if no date is given.
        */
        Rate previousCouponRate(Date d = Date()) const;

        Date nextCashFlowDate(Date d = Date()) const;
        Date previousCashFlowDate(Date d = Date()) const;

      protected:
        void setupExpired() const override;
        void setupArguments(PricingEngine::arguments*) const override;
        void fetchResults(const PricingEngine::results*) const override;

        /*! This method can be called by derived classes in order to
            build redemption payments from the existing cash flows.
            It must be called after setting up the cashflows_ vector
            and will fill the notionalSchedule_, notionals_, and
            redemptions_ data members.

            If given, the elements of the redemptions vector will
            multiply the amount of the redemption cash flow.  The
            elements will be taken in base 100, i.e., a redemption
            equal to 100 does not modify the amount.

            \pre The cashflows_ vector must contain at least one
                 coupon and must be sorted by date.
        */
        void addRedemptionsToCashflows(const std::vector<Real>& redemptions
                                                       = std::vector<Real>());

        /*! This method can be called by derived classes in order to
            build a bond with a single redemption payment.  It will
            fill the notionalSchedule_, notionals_, and redemptions_
            data members.
        */
        void setSingleRedemption(Real notional,
                                 Real redemption,
                                 const Date& date);

        /*! This method can be called by derived classes in order to
            build a bond with a single redemption payment.  It will
            fill the notionalSchedule_, notionals_, and redemptions_
            data members.
        */
        void setSingleRedemption(Real notional,
                                 const ext::shared_ptr<CashFlow>& redemption);

        /*! used internally to collect notional information from the
            coupons. It should not be called by derived classes,
            unless they already provide redemption cash flows (in
            which case they must set up the redemptions_ data member
            independently).  It will fill the notionalSchedule_ and
            notionals_ data members.
        */
        void calculateNotionalsFromCashflows();

        Natural settlementDays_;
        Calendar calendar_;
        std::vector<Date> notionalSchedule_;
        std::vector<Real> notionals_;
        Leg cashflows_; // all cashflows
        Leg redemptions_; // the redemptions

        Date maturityDate_, issueDate_;
        mutable Real settlementValue_;
    };

    class Bond::arguments : public PricingEngine::arguments {
      public:
        Date settlementDate;
        Leg cashflows;
        Calendar calendar;
        void validate() const override;
    };

    class Bond::results : public Instrument::results {
      public:
        Real settlementValue;
        void reset() override {
            settlementValue = Null<Real>();
            Instrument::results::reset();
        }
    };

    class Bond::engine : public GenericEngine<Bond::arguments,
                                              Bond::results> {};


    // inline definitions

    in
