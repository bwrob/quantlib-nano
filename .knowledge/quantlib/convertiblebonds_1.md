                                  Real conversionRatio,
                                   const CallabilitySchedule& callability,
                                   const Date& issueDate,
                                   Natural settlementDays,
                                   const std::vector<Rate>& coupons,
                                   const DayCounter& dayCounter,
                                   const Schedule& schedule,
                                   Real redemption = 100,
                                   const Period& exCouponPeriod = Period(),
                                   const Calendar& exCouponCalendar = Calendar(),
                                   BusinessDayConvention exCouponConvention = Unadjusted,
                                   bool exCouponEndOfMonth = false);
    };


    //! convertible floating-rate bond
    /*! \warning Most methods inherited from Bond (such as yield or
                 the yield-based dirtyPrice and cleanPrice) refer to
                 the underlying plain-vanilla bond and do not take
                 convertibility and callability into account.
    */
    class ConvertibleFloatingRateBond : public ConvertibleBond {
      public:
        ConvertibleFloatingRateBond(const ext::shared_ptr<Exercise>& exercise,
                                    Real conversionRatio,
                                    const CallabilitySchedule& callability,
                                    const Date& issueDate,
                                    Natural settlementDays,
                                    const ext::shared_ptr<IborIndex>& index,
                                    Natural fixingDays,
                                    const std::vector<Spread>& spreads,
                                    const DayCounter& dayCounter,
                                    const Schedule& schedule,
                                    Real redemption = 100,
                                    const Period& exCouponPeriod = Period(),
                                    const Calendar& exCouponCalendar = Calendar(),
                                    BusinessDayConvention exCouponConvention = Unadjusted,
                                    bool exCouponEndOfMonth = false);
    };


    class ConvertibleBond::arguments : public PricingEngine::arguments {
      public:
        arguments()
        : conversionRatio(Null<Real>()), settlementDays(Null<Natural>()), redemption(Null<Real>()) {}

        ext::shared_ptr<Exercise> exercise;
        Real conversionRatio;
        std::vector<Date> callabilityDates;
        std::vector<Callability::Type> callabilityTypes;
        std::vector<Real> callabilityPrices;
        std::vector<Real> callabilityTriggers;
        Leg cashflows;
        Date issueDate;
        Date settlementDate;

        Natural settlementDays;
        Real redemption;
        void validate() const override;
    };

    class ConvertibleBond::engine
    : public GenericEngine<ConvertibleBond::arguments, ConvertibleBond::results> {};

}

#endif
