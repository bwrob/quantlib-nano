        - Convention should be Following for yield curve and
                    contract cashflows.
                  - The CDS should pay accrued and mature on standard
                    IMM dates, settle on trade date +1 and upfront
                    settle on trade date +3.
        */
        Rate impliedHazardRate(Real targetNPV,
                               const Handle<YieldTermStructure>& discountCurve,
                               const DayCounter& dayCounter,
                               Real recoveryRate = 0.4,
                               Real accuracy = 1.0e-8,
                               PricingModel model = Midpoint) const;

        //! Conventional/standard upfront-to-spread conversion
        /*! Under a standard ISDA model and a set of standardised
            instrument characteristics, it is the running only quoted
            spread that will make a CDS contract have an NPV of 0 when
            quoted for that running only spread.  Refer to: "ISDA
            Standard CDS converter specification." May 2009.

            The conventional recovery rate to apply in the calculation
            is as specified by ISDA, not necessarily equal to the
            market-quoted one.  It is typically 0.4 for SeniorSec and
            0.2 for subordinate.

            \note The conversion employs a flat hazard rate. As a result,
                  you will not recover the market quotes.

            \note This method performs the calculation with the
                  instrument characteristics. It will coincide with
                  the ISDA calculation if your object has the standard
                  characteristics. Notably:
                  - The calendar should have no bank holidays, just
                    weekends.
                  - The yield curve should be LIBOR piecewise constant
                    in fwd rates, with a discount factor of 1 on the
                    calculation date, which coincides with the trade
                    date.
                  - Convention should be Following for yield curve and
                    contract cashflows.
                  - The CDS should pay accrued and mature on standard
                    IMM dates, settle on trade date +1 and upfront
                    settle on trade date +3.
        */
        Rate conventionalSpread(Real conventionalRecovery,
                                const Handle<YieldTermStructure>& discountCurve,
                                const DayCounter& dayCounter,
                                PricingModel model = Midpoint) const;
        //@}
      protected:
        //! \name Instrument interface
        //@{
        void setupExpired() const override;
        //@}
        // data members
        Protection::Side side_;
        Real notional_;
        ext::optional<Rate> upfront_;
        Rate runningSpread_;
        bool settlesAccrual_, paysAtDefaultTime_;
        ext::shared_ptr<Claim> claim_;
        Leg leg_;
        ext::shared_ptr<SimpleCashFlow> upfrontPayment_;
        ext::shared_ptr<SimpleCashFlow> accrualRebate_;
        Date protectionStart_;
        Date tradeDate_;
        Natural cashSettlementDays_;
        Date maturity_;
        // results
        mutable Rate fairUpfront_;
        mutable Rate fairSpread_;
        mutable Real couponLegBPS_, couponLegNPV_;
        mutable Real upfrontBPS_, upfrontNPV_;
        mutable Real defaultLegNPV_;
        mutable Real accrualRebateNPV_;

      private:
        //! Shared initialisation.
        void init(const Schedule& schedule, BusinessDayConvention paymentConvention, const DayCounter& dayCounter,
            const DayCounter& lastPeriodDayCounter, bool rebatesAccrual, const Date& upfrontDate = Date());
    };


    class CreditDefaultSwap::arguments
        : public virtual PricingEngine::arguments {
      public:
        arguments();
        Protection::Side side;
        Real notional;
        ext::optional<Rate> upfront;
        Rate spread;

