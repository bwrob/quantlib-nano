vDate = Date());

        //! NPV and BPS of the cash flows.
        /*! The NPV and BPS of the cash flows calculated
            together for performance reason
        */
        static std::pair<Real, Real> npvbps(const Leg& leg,
                                            const YieldTermStructure& discountCurve,
                                            const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                                            Date settlementDate = Date(),
                                            Date npvDate = Date());

        //! At-the-money rate of the cash flows.
        /*! The result is the fixed rate for which a fixed rate cash flow
            vector, equivalent to the input vector, has the required NPV
            according to the given term structure. If the required NPV is
            not given, the input cash flow vector's NPV is used instead.
        */
        static Rate atmRate(const Leg& leg,
                            const YieldTermStructure& discountCurve,
                            const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                            Date settlementDate = Date(),
                            Date npvDate = Date(),
                            Real npv = Null<Real>());
        //@}

        //! \name Yield (a.k.a. Internal Rate of Return, i.e. IRR) functions
        /*! The IRR is the interest rate at which the NPV of the cash
            flows equals the dirty price.
        */
        //@{
        //! NPV of the cash flows.
        /*! The NPV is the sum of the cash flows, each discounted
            according to the given constant interest rate.  The result
            is affected by the choice of the interest-rate compounding
            and the relative frequency and day counter.
        */
        static Real npv(const Leg& leg,
                        const InterestRate& yield,
                        const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                        Date settlementDate = Date(),
                        Date npvDate = Date());
        static Real npv(const Leg& leg,
                        Rate yield,
                        const DayCounter& dayCounter,
                        Compounding compounding,
                        Frequency frequency,
                        const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                        Date settlementDate = Date(),
                        Date npvDate = Date());
        //! Basis-point sensitivity of the cash flows.
        /*! The result is the change in NPV due to a uniform
            1-basis-point change in the rate paid by the cash
            flows. The change for each coupon is discounted according
            to the given constant interest rate.  The result is
            affected by the choice of the interest-rate compounding
            and the relative frequency and day counter.
        */
        static Real bps(const Leg& leg,
                        const InterestRate& yield,
                        const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                        Date settlementDate = Date(),
                        Date npvDate = Date());
        static Real bps(const Leg& leg,
                        Rate yield,
                        const DayCounter& dayCounter,
                        Compounding compounding,
                        Frequency frequency,
                        const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                        Date settlementDate = Date(),
                        Date npvDate = Date());
        //! Implied internal rate of return.
        /*! The function verifies
            the theoretical existence of an IRR and numerically
            establishes the IRR to the desired precision.
        */
        static Rate yield(const Leg& leg,
                          Real npv,
         