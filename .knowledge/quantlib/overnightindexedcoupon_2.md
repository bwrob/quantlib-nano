ity() const;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;

        bool isCapped() const { return cap_ != Null<Real>(); }
        bool isFloored() const { return floor_ != Null<Real>(); }

        void setPricer(const ext::shared_ptr<FloatingRateCouponPricer>& pricer) override; 

        ext::shared_ptr<OvernightIndexedCoupon> underlying() const { return underlying_; }
        bool nakedOption() const { return nakedOption_; }
        bool dailyCapFloor() const { return dailyCapFloor_; }
        bool compoundSpreadDaily() const { return underlying_->compoundSpreadDaily(); }
        //! averaging method
        RateAveraging::Type averagingMethod() const { return underlying_->averagingMethod(); }

    protected:
        ext::shared_ptr<OvernightIndexedCoupon> underlying_;
        Rate cap_, floor_;
        bool nakedOption_;
        bool dailyCapFloor_;
        mutable Real effectiveCapletVolatility_;
        mutable Real effectiveFloorletVolatility_;
    };

    //! helper class building a sequence of overnight coupons
    class OvernightLeg {
      public:
        OvernightLeg(Schedule  schedule, const ext::shared_ptr<OvernightIndex>& overnightIndex);
        OvernightLeg& withNotionals(Real notional);
        OvernightLeg& withNotionals(const std::vector<Real>& notionals);
        OvernightLeg& withPaymentDayCounter(const DayCounter&);
        OvernightLeg& withPaymentAdjustment(BusinessDayConvention);
        OvernightLeg& withPaymentCalendar(const Calendar&);
        OvernightLeg& withPaymentLag(Integer lag);
        OvernightLeg& withGearings(Real gearing);
        OvernightLeg& withGearings(const std::vector<Real>& gearings);
        OvernightLeg& withSpreads(Spread spread);
        OvernightLeg& withSpreads(const std::vector<Spread>& spreads);
        OvernightLeg& withTelescopicValueDates(bool telescopicValueDates);
        OvernightLeg& withAveragingMethod(RateAveraging::Type averagingMethod);
        OvernightLeg& withLookbackDays(Natural lookbackDays);
        OvernightLeg& withLockoutDays(Natural lockoutDays);
        OvernightLeg& withObservationShift(bool applyObservationShift = true);
        OvernightLeg& compoundingSpreadDaily(bool compoundSpreadDaily = true);
        OvernightLeg& withLookback(const Period& lookback);
        OvernightLeg& withCaps(Rate cap);
        OvernightLeg& withCaps(const std::vector<Rate>& caps);
        OvernightLeg& withFloors(Rate floor);
        OvernightLeg& withFloors(const std::vector<Rate>& floors);
        OvernightLeg& withNakedOption(bool nakedOption);
        OvernightLeg& withDailyCapFloor(bool dailyCapFloor = true);
        OvernightLeg& inArrears(bool inArrears);
        OvernightLeg& withLastRecentPeriod(const ext::optional<Period>& lastRecentPeriod);
        OvernightLeg& withLastRecentPeriodCalendar(const Calendar& lastRecentPeriodCalendar);
        OvernightLeg& withPaymentDates(const std::vector<Date>& paymentDates);
        OvernightLeg& withCouponPricer(const ext::shared_ptr<OvernightIndexedCouponPricer>& couponPricer);

        operator Leg() const;
      private:
        Schedule schedule_;
        ext::shared_ptr<OvernightIndex> overnightIndex_;
        std::vector<Real> notionals_;
        DayCounter paymentDayCounter_;
        Calendar paymentCalendar_;
        BusinessDayConvention paymentAdjustment_ = Following;
        Integer paymentLag_ = 0;
        std::vector<Real> gearings_;
        std::vector<Spread> spreads_;
        bool telescopicValueDates_ = false;
        RateAveraging::Type averagingMethod_ = RateAveraging::Compound;
        Natural lookbackDays_ = Null<Natural>();
        Natural lockoutDays_ = 0;
        bool applyObservationShift_ = false;
        bool compoundSpreadDaily_ = false;
        std::vector<Rate> caps_, floors_;
        bool nakedOption_ = false;
        bool dailyCapFloor_ = false;
        bool inArrears_ = true;
        ext::optional<Period> lastRecentPeriod_;
        