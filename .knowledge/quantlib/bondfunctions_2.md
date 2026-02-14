Real amount = price.amount();

            if (price.type() == Bond::Price::Clean)
                amount += bond.accruedAmount(settlementDate);

            amount /= 100.0 / bond.notional(settlementDate);

            return CashFlows::yield<Solver>(solver, bond.cashflows(), amount, dayCounter,
                                            compounding,
                                            frequency, false, settlementDate,
                                            settlementDate, accuracy, guess);
        }
        static Time duration(const Bond& bond,
                             const InterestRate& yield,
                             Duration::Type type = Duration::Modified,
                             Date settlementDate = Date() );
        static Time duration(const Bond& bond,
                             Rate yield,
                             const DayCounter& dayCounter,
                             Compounding compounding,
                             Frequency frequency,
                             Duration::Type type = Duration::Modified,
                             Date settlementDate = Date() );
        static Real convexity(const Bond& bond,
                              const InterestRate& yield,
                              Date settlementDate = Date());
        static Real convexity(const Bond& bond,
                              Rate yield,
                              const DayCounter& dayCounter,
                              Compounding compounding,
                              Frequency frequency,
                              Date settlementDate = Date());
        static Real basisPointValue(const Bond& bond,
                                    const InterestRate& yield,
                                    Date settlementDate = Date());
        static Real basisPointValue(const Bond& bond,
                                    Rate yield,
                                    const DayCounter& dayCounter,
                                    Compounding compounding,
                                    Frequency frequency,
                                    Date settlementDate = Date());
        static Real yieldValueBasisPoint(const Bond& bond,
                                         const InterestRate& yield,
                                         Date settlementDate = Date());
        static Real yieldValueBasisPoint(const Bond& bond,
                                         Rate yield,
                                         const DayCounter& dayCounter,
                                         Compounding compounding,
                                         Frequency frequency,
                                         Date settlementDate = Date());
        //@}

        //! \name Z-spread functions
        //@{
        static Real cleanPrice(const Bond& bond,
                               const ext::shared_ptr<YieldTermStructure>& discount,
                               Spread zSpread,
                               const DayCounter& dayCounter,
                               Compounding compounding,
                               Frequency frequency,
                               Date settlementDate = Date());
        static Real dirtyPrice(const Bond& bond,
                               const ext::shared_ptr<YieldTermStructure>& discount,
                               Spread zSpread,
                               const DayCounter& dayCounter,
                               Compounding compounding,
                               Frequency frequency,
                               Date settlementDate = Date());
        static Spread zSpread(const Bond& bond,
                              Bond::Price price,
                              const ext::shared_ptr<YieldTermStructure>&,
                              const DayCounter& dayCounter,
                              Compounding compounding,
                              Frequency frequency,
                              Date s
