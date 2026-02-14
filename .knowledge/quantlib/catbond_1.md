
        FloatingCatBond(Natural settlementDays,
                        Real faceAmount,
                        const Date& startDate,
                        const Date& maturityDate,
                        Frequency couponFrequency,
                        const Calendar& calendar,
                        const ext::shared_ptr<IborIndex>& iborIndex,
                        const DayCounter& accrualDayCounter,
                        const ext::shared_ptr<NotionalRisk>& notionalRisk,
                        BusinessDayConvention accrualConvention = Following,
                        BusinessDayConvention paymentConvention = Following,
                        Natural fixingDays = Null<Natural>(),
                        const std::vector<Real>& gearings = std::vector<Real>(1, 1.0),
                        const std::vector<Spread>& spreads = std::vector<Spread>(1, 0.0),
                        const std::vector<Rate>& caps = std::vector<Rate>(),
                        const std::vector<Rate>& floors = std::vector<Rate>(),
                        bool inArrears = false,
                        Real redemption = 100.0,
                        const Date& issueDate = Date(),
                        const Date& stubDate = Date(),
                        DateGeneration::Rule rule = DateGeneration::Backward,
                        bool endOfMonth = false);
    };

}

#endif