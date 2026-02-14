Date settlementDate = Date());
        static Time accruedPeriod(const Bond& bond,
                                  Date settlementDate = Date());
        static Date::serial_type accruedDays(const Bond& bond,
                                             Date settlementDate = Date());
        static Real accruedAmount(const Bond& bond,
                                  Date settlementDate = Date());
        //@}

        //! \name YieldTermStructure functions
        //@{
        static Real cleanPrice(const Bond& bond,
                               const YieldTermStructure& discountCurve,
                               Date settlementDate = Date());
        static Real dirtyPrice(const Bond& bond,
                               const YieldTermStructure& discountCurve,
                               Date settlementDate = Date());
        static Real bps(const Bond& bond,
                        const YieldTermStructure& discountCurve,
                        Date settlementDate = Date());

        static Rate atmRate(const Bond& bond,
                            const YieldTermStructure& discountCurve,
                            Date settlementDate = Date(),
                            Bond::Price price = {});
        //@}

        //! \name Yield (a.k.a. Internal Rate of Return, i.e. IRR) functions
        //@{
        static Real cleanPrice(const Bond& bond,
                               const InterestRate& yield,
                               Date settlementDate = Date());
        static Real cleanPrice(const Bond& bond,
                               Rate yield,
                               const DayCounter& dayCounter,
                               Compounding compounding,
                               Frequency frequency,
                               Date settlementDate = Date());
        static Real dirtyPrice(const Bond& bond,
                               const InterestRate& yield,
                               Date settlementDate = Date());
        static Real dirtyPrice(const Bond& bond,
                               Rate yield,
                               const DayCounter& dayCounter,
                               Compounding compounding,
                               Frequency frequency,
                               Date settlementDate = Date());
        static Real bps(const Bond& bond,
                        const InterestRate& yield,
                        Date settlementDate = Date());
        static Real bps(const Bond& bond,
                        Rate yield,
                        const DayCounter& dayCounter,
                        Compounding compounding,
                        Frequency frequency,
                        Date settlementDate = Date());
        static Rate yield(const Bond& bond,
                          Bond::Price price,
                          const DayCounter& dayCounter,
                          Compounding compounding,
                          Frequency frequency,
                          Date settlementDate = Date(),
                          Real accuracy = 1.0e-10,
                          Size maxIterations = 100,
                          Rate guess = 0.05);
        template <typename Solver>
        static Rate yield(const Solver& solver,
                          const Bond& bond,
                          Bond::Price price,
                          const DayCounter& dayCounter,
                          Compounding compounding,
                          Frequency frequency,
                          Date settlementDate = Date(),
                          Real accuracy = 1.0e-10,
                          Rate guess = 0.05) {
            if (settlementDate == Date())
                settlementDate = bond.settlementDate();

            QL_REQUIRE(BondFunctions::isTradable(bond, settlementDate),
                       "non tradable at " << settlementDate <<
                       " (maturity being " << bond.maturityDate() << ")");

            