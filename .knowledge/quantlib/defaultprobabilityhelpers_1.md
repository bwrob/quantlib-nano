d to specify an explicit start date for the CDS schedule and the date from which the
                              CDS maturity is calculated via the \p tenor. Useful for off-the-run index schedules.
            @param lastPeriodDayCounter  The day counter for the last fee leg coupon. See comment on \p dayCounter.
            @param rebatesAccrual  Set to \c true if the fee leg accrual is rebated on the cash settlement date. For
                                   CDS after the Big Bang, this is typically \c true.
            @param model  The pricing model to use for the helper.
        */
        CdsHelper(const std::variant<Rate, Handle<Quote>>& quote,
                  const Period& tenor,
                  Integer settlementDays,
                  Calendar calendar,
                  Frequency frequency,
                  BusinessDayConvention paymentConvention,
                  DateGeneration::Rule rule,
                  DayCounter dayCounter,
                  Real recoveryRate,
                  const Handle<YieldTermStructure>& discountCurve,
                  bool settlesAccrual = true,
                  bool paysAtDefaultTime = true,
                  const Date& startDate = Date(),
                  DayCounter lastPeriodDayCounter = DayCounter(),
                  bool rebatesAccrual = true,
                  CreditDefaultSwap::PricingModel model = CreditDefaultSwap::Midpoint);

        void setTermStructure(DefaultProbabilityTermStructure*) override;
        // NOLINTNEXTLINE(cppcoreguidelines-noexcept-swap,performance-noexcept-swap)
        ext::shared_ptr<CreditDefaultSwap> swap() const {
            return swap_;
        }
        void update() override;

      protected:
        void initializeDates() override;
        virtual void resetEngine() = 0;
        Period tenor_;
        Integer settlementDays_;
        Calendar calendar_;
        Frequency frequency_;
        BusinessDayConvention paymentConvention_;
        DateGeneration::Rule rule_;
        DayCounter dayCounter_;
        Real recoveryRate_;
        Handle<YieldTermStructure> discountCurve_;
        bool settlesAccrual_;
        bool paysAtDefaultTime_;
        DayCounter lastPeriodDC_;
        bool rebatesAccrual_;
        CreditDefaultSwap::PricingModel model_;

        Schedule schedule_;
        ext::shared_ptr<CreditDefaultSwap> swap_;
        RelinkableHandle<DefaultProbabilityTermStructure> probability_;
        //! protection effective date.
        Date protectionStart_;
        Date startDate_;
    };

    //! Spread-quoted CDS hazard rate bootstrap helper.
    class SpreadCdsHelper : public CdsHelper {
      public:
        SpreadCdsHelper(const std::variant<Rate, Handle<Quote>>& runningSpread,
                        const Period& tenor,
                        Integer settlementDays,
                        const Calendar& calendar,
                        Frequency frequency,
                        BusinessDayConvention paymentConvention,
                        DateGeneration::Rule rule,
                        const DayCounter& dayCounter,
                        Real recoveryRate,
                        const Handle<YieldTermStructure>& discountCurve,
                        bool settlesAccrual = true,
                        bool paysAtDefaultTime = true,
                        const Date& startDate = Date(),
                        const DayCounter& lastPeriodDayCounter = DayCounter(),
                        bool rebatesAccrual = true,
                        CreditDefaultSwap::PricingModel model = CreditDefaultSwap::Midpoint);

        Real impliedQuote() const override;

      private:
        void resetEngine() override;
    };

    //! Upfront-quoted CDS hazard rate bootstrap helper.
    class UpfrontCdsHelper : public CdsHelper {
      public:
        /*! \note the upfront must be quoted in fractional units. */
        UpfrontCdsHelper(const std::variant<Rate, Handle<Quote>>& upfront,
                         Rate ru
