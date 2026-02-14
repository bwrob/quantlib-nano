                            Rate yield,
                              const DayCounter& dayCounter,
                              Compounding compounding,
                              Frequency frequency,
                              const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                              Date settlementDate = Date(),
                              Date npvDate = Date());

        //! Basis-point value
        /*! Obtained by setting dy = 0.0001 in the 2nd-order Taylor
            series expansion.
        */
        static Real basisPointValue(const Leg& leg,
                                    const InterestRate& yield,
                                    const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                                    Date settlementDate = Date(),
                                    Date npvDate = Date());
        static Real basisPointValue(const Leg& leg,
                                    Rate yield,
                                    const DayCounter& dayCounter,
                                    Compounding compounding,
                                    Frequency frequency,
                                    const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                                    Date settlementDate = Date(),
                                    Date npvDate = Date());

        //! Yield value of a basis point
        /*! The yield value of a one basis point change in price is
            the derivative of the yield with respect to the price
            multiplied by 0.01
        */
        static Real yieldValueBasisPoint(const Leg& leg,
                                         const InterestRate& yield,
                                         const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                                         Date settlementDate = Date(),
                                         Date npvDate = Date());
        static Real yieldValueBasisPoint(const Leg& leg,
                                         Rate yield,
                                         const DayCounter& dayCounter,
                                         Compounding compounding,
                                         Frequency frequency,
                                         const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                                         Date settlementDate = Date(),
                                         Date npvDate = Date());
        //@}

        //! \name Z-spread functions
        /*! For details on z-spread refer to:
            "Credit Spreads Explained", Lehman Brothers European Fixed
            Income Research - March 2004, D. O'Kane
        */
        //@{
        //! NPV of the cash flows.
        /*! The NPV is the sum of the cash flows, each discounted
            according to the z-spreaded term structure.  The result
            is affected by the choice of the z-spread compounding
            and the relative frequency and day counter.
        */
        static Real npv(const Leg& leg,
                        const ext::shared_ptr<YieldTermStructure>& discount,
                        Spread zSpread,
                        const DayCounter& dayCounter,
                        Compounding compounding,
                        Frequency frequency,
                        const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                        Date settlementDate = Date(),
                        Date npvDate = Date());
        //! implied Z-spread.
        static Spread zSpread(const Leg& leg,
                              Real npv,
                              const ext::shared_ptr<YieldTermStructure>&,
                              const DayCounter& dayCounter,
                              Compounding compounding,
                              Frequency frequency,

