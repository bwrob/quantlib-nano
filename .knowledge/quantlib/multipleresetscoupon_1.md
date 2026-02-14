atingRateCouponPricer {
      public:
        Rate swapletPrice() const override;
        Real capletPrice(Rate effectiveCap) const override;
        Rate capletRate(Rate effectiveCap) const override;
        Real floorletPrice(Rate effectiveFloor) const override;
        Rate floorletRate(Rate effectiveFloor) const override;
        void initialize(const FloatingRateCoupon& coupon) override;

      protected:
        const MultipleResetsCoupon* coupon_;
        std::vector<Real> subPeriodFixings_;
    };

    class AveragingMultipleResetsPricer: public MultipleResetsPricer {
      public:
        Real swapletRate() const override;
    };

    class CompoundingMultipleResetsPricer: public MultipleResetsPricer {
      public:
        Real swapletRate() const override;
    };


    //! helper class building a sequence of multiple-reset coupons
    class MultipleResetsLeg {
      public:
        /*! \param fullResetSchedule the full schedule specifying reset periods for all coupons.
            \param index             the index whose fixings will be used; it should have the
                                     same tenor as the resets.
            \param resetsPerCoupon   the number of resets for each coupon; the number of periods
                                     in the schedule should be divided exactly by this number.
        */
        MultipleResetsLeg(Schedule fullResetSchedule,
                          ext::shared_ptr<IborIndex> index,
                          Size resetsPerCoupon);
        MultipleResetsLeg& withNotionals(Real notional);
        MultipleResetsLeg& withNotionals(const std::vector<Real>& notionals);
        MultipleResetsLeg& withPaymentDayCounter(const DayCounter&);
        MultipleResetsLeg& withPaymentAdjustment(BusinessDayConvention);
        MultipleResetsLeg& withPaymentCalendar(const Calendar&);
        MultipleResetsLeg& withPaymentLag(Integer lag);
        MultipleResetsLeg& withFixingDays(Natural fixingDays);
        MultipleResetsLeg& withFixingDays(const std::vector<Natural>& fixingDays);
        MultipleResetsLeg& withGearings(Real gearing);
        MultipleResetsLeg& withGearings(const std::vector<Real>& gearings);
        MultipleResetsLeg& withCouponSpreads(Spread spread);
        MultipleResetsLeg& withCouponSpreads(const std::vector<Spread>& spreads);
        MultipleResetsLeg& withRateSpreads(Spread spread);
        MultipleResetsLeg& withRateSpreads(const std::vector<Spread>& spreads);
        MultipleResetsLeg& withExCouponPeriod(const Period&,
                                              const Calendar&,
                                              BusinessDayConvention,
                                              bool endOfMonth = false);
        MultipleResetsLeg& withAveragingMethod(RateAveraging::Type averagingMethod);
        operator Leg() const;

      private:
        Schedule schedule_;
        ext::shared_ptr<IborIndex> index_;
        Size resetsPerCoupon_;
        std::vector<Real> notionals_;
        DayCounter paymentDayCounter_;
        Calendar paymentCalendar_;
        BusinessDayConvention paymentAdjustment_ = Following;
        Integer paymentLag_ = 0;
        std::vector<Natural> fixingDays_;
        std::vector<Real> gearings_;
        std::vector<Spread> couponSpreads_;
        std::vector<Spread> rateSpreads_;
        RateAveraging::Type averagingMethod_ = RateAveraging::Compound;
        Period exCouponPeriod_;
        Calendar exCouponCalendar_;
        BusinessDayConvention exCouponAdjustment_ = Unadjusted;
        bool exCouponEndOfMonth_ = false;
    };

}

#endif
