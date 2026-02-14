SettlementDateFlows = ext::nullopt,
                               Date settlementDate = Date());
        static Real
        nextCashFlowAmount(const Leg& leg,
                           const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                           Date settlementDate = Date());
        //@}

        //! \name Coupon inspectors
        //@{
        static Rate
        previousCouponRate(const Leg& leg,
                           const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                           Date settlementDate = Date());
        static Rate
        nextCouponRate(const Leg& leg,
                       const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                       Date settlementDate = Date());

        static Real
        nominal(const Leg& leg,
                const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                Date settlementDate = Date());
        static Date
        accrualStartDate(const Leg& leg,
                         const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                         Date settlementDate = Date());
        static Date
        accrualEndDate(const Leg& leg,
                       const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                       Date settlementDate = Date());
        static Date
        referencePeriodStart(const Leg& leg,
                             const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                             Date settlementDate = Date());
        static Date
        referencePeriodEnd(const Leg& leg,
                           const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                           Date settlementDate = Date());
        static Time
        accrualPeriod(const Leg& leg,
                      const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                      Date settlementDate = Date());
        static Date::serial_type
        accrualDays(const Leg& leg,
                    const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                    Date settlementDate = Date());
        static Time
        accruedPeriod(const Leg& leg,
                      const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                      Date settlementDate = Date());
        static Date::serial_type
        accruedDays(const Leg& leg,
                    const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                    Date settlementDate = Date());
        static Real
        accruedAmount(const Leg& leg,
                      const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                      Date settlementDate = Date());
        //@}

        //! \name YieldTermStructure functions
        //@{
        //! NPV of the cash flows.
        /*! The NPV is the sum of the cash flows, each discounted
            according to the given term structure.
        */
        static Real npv(const Leg& leg,
                        const YieldTermStructure& discountCurve,
                        const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                        Date settlementDate = Date(),
                        Date npvDate = Date());
        //! Basis-point sensitivity of the cash flows.
        /*! The result is the change in NPV due to a uniform
            1-basis-point change in the rate paid by the cash
            flows. The change for each coupon is discounted according
            to the given term structure.
        */
        static Real bps(const Leg& leg,
                        const YieldTermStructure& discountCurve,
                        const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                        Date settlementDate = Date(),
                        Date np