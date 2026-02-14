                 const DayCounter& dayCounter,
                          Compounding compounding,
                          Frequency frequency,
                          const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                          Date settlementDate = Date(),
                          Date npvDate = Date(),
                          Real accuracy = 1.0e-10,
                          Size maxIterations = 100,
                          Rate guess = 0.05);

        template <typename Solver>
        static Rate yield(const Solver& solver,
                          const Leg& leg,
                          Real npv,
                          const DayCounter& dayCounter,
                          Compounding compounding,
                          Frequency frequency,
                          const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                          Date settlementDate = Date(),
                          Date npvDate = Date(),
                          Real accuracy = 1.0e-10,
                          Rate guess = 0.05) {
            IrrFinder objFunction(leg, npv, dayCounter, compounding,
                                  frequency, includeSettlementDateFlows,
                                  settlementDate, npvDate);
            return solver.solve(objFunction, accuracy, guess, guess/10.0);
        }

        //! Cash-flow duration.
        /*! The simple duration of a string of cash flows is defined as
            \f[
            D_{\mathrm{simple}} = \frac{\sum t_i c_i B(t_i)}{\sum c_i B(t_i)}
            \f]
            where \f$ c_i \f$ is the amount of the \f$ i \f$-th cash
            flow, \f$ t_i \f$ is its payment time, and \f$ B(t_i) \f$
            is the corresponding discount according to the passed yield.

            The modified duration is defined as
            \f[
            D_{\mathrm{modified}} = -\frac{1}{P} \frac{\partial P}{\partial y}
            \f]
            where \f$ P \f$ is the present value of the cash flows
            according to the given IRR \f$ y \f$.

            The Macaulay duration is defined for a compounded IRR as
            \f[
            D_{\mathrm{Macaulay}} = \left( 1 + \frac{y}{N} \right)
                                    D_{\mathrm{modified}}
            \f]
            where \f$ y \f$ is the IRR and \f$ N \f$ is the number of
            cash flows per year.
        */
        static Time duration(const Leg& leg,
                             const InterestRate& yield,
                             Duration::Type type,
                             const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                             Date settlementDate = Date(),
                             Date npvDate = Date());
        static Time duration(const Leg& leg,
                             Rate yield,
                             const DayCounter& dayCounter,
                             Compounding compounding,
                             Frequency frequency,
                             Duration::Type type,
                             const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                             Date settlementDate = Date(),
                             Date npvDate = Date());

        //! Cash-flow convexity
        /*! The convexity of a string of cash flows is defined as
            \f[
            C = \frac{1}{P} \frac{\partial^2 P}{\partial y^2}
            \f]
            where \f$ P \f$ is the present value of the cash flows
            according to the given IRR \f$ y \f$.
        */
        static Real convexity(const Leg& leg,
                              const InterestRate& yield,
                              const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                              Date settlementDate = Date(),
                              Date npvDate = Date());
        static Real convexity(const Leg& leg,

