the \p cashSettlementDays to determine 
                              the date on which the cash settlement amount is paid if \p upfrontDate is empty. If not 
                              given, the trade date is guessed from the protection start date and \p schedule date 
                              generation rule.
            @param cashSettlementDays  The number of business days from \p tradeDate to cash settlement date.
        */
        CreditDefaultSwap(Protection::Side side,
                          Real notional,
                          Rate upfront,
                          Rate spread,
                          const Schedule& schedule,
                          BusinessDayConvention paymentConvention,
                          const DayCounter& dayCounter,
                          bool settlesAccrual = true,
                          bool paysAtDefaultTime = true,
                          const Date& protectionStart = Date(),
                          const Date& upfrontDate = Date(),
                          ext::shared_ptr<Claim> = ext::shared_ptr<Claim>(),
                          const DayCounter& lastPeriodDayCounter = DayCounter(),
                          bool rebatesAccrual = true,
                          const Date& tradeDate = Date(),
                          Natural cashSettlementDays = 3);
        //@}
        //! \name Instrument interface
        //@{
        bool isExpired() const override;
        void setupArguments(PricingEngine::arguments*) const override;
        void fetchResults(const PricingEngine::results*) const override;
        //@}
        //! \name Inspectors
        //@{
        Protection::Side side() const;
        Real notional() const;
        Rate runningSpread() const;
        ext::optional<Rate> upfront() const;
        bool settlesAccrual() const;
        bool paysAtDefaultTime() const;
        const Leg& coupons() const;
        //! The first date for which defaults will trigger the contract
        const Date& protectionStartDate() const;
        //! The last date for which defaults will trigger the contract
        const Date& protectionEndDate() const;
        bool rebatesAccrual() const { return accrualRebate_ != nullptr; }
        const ext::shared_ptr<SimpleCashFlow>& upfrontPayment() const;
        const ext::shared_ptr<SimpleCashFlow>& accrualRebate() const;
        const Date& tradeDate() const;
        Natural cashSettlementDays() const;
        //@}
        //! \name Results
        //@{
        /*! Returns the upfront spread that, given the running spread
            and the quoted recovery rate, will make the instrument
            have an NPV of 0.
        */
        Rate fairUpfront() const;
        /*! Returns the running spread that, given the quoted recovery
            rate, will make the running-only CDS have an NPV of 0.

            \note This calculation does not take any upfront into
                  account, even if one was given.
        */
        Rate fairSpread() const;
        /*! Returns the variation of the fixed-leg value given a
            one-basis-point change in the running spread.
        */
        Real couponLegBPS() const;
        Real upfrontBPS() const;
        Real couponLegNPV() const;
        Real defaultLegNPV() const;
        Real upfrontNPV() const;
        Real accrualRebateNPV() const;

        //! Implied hazard rate calculation
        /*! \note This method performs the calculation with the
                  instrument characteristics. It will coincide with
                  the ISDA calculation if your object has the standard
                  characteristics. Notably:
                  - The calendar should have no bank holidays, just
                    weekends.
                  - The yield curve should be LIBOR piecewise constant
                    in fwd rates, with a discount factor of 1 on the
                    calculation date, which coincides with the trade
                    date.
          