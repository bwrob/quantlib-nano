<InterestRate>&);
        FixedRateLeg& withPaymentAdjustment(BusinessDayConvention);
        FixedRateLeg& withFirstPeriodDayCounter(const DayCounter&);
        FixedRateLeg& withLastPeriodDayCounter(const DayCounter&);
        FixedRateLeg& withPaymentCalendar(const Calendar&);
        FixedRateLeg& withPaymentLag(Integer lag);
        FixedRateLeg& withExCouponPeriod(const Period&,
                                         const Calendar&,
                                         BusinessDayConvention,
                                         bool endOfMonth = false);
        operator Leg() const;
      private:
        Schedule schedule_;
        std::vector<Real> notionals_;
        std::vector<InterestRate> couponRates_;
        DayCounter firstPeriodDC_ , lastPeriodDC_;
        Calendar paymentCalendar_;
        BusinessDayConvention paymentAdjustment_ = Following;
        Integer paymentLag_ = 0;
        Period exCouponPeriod_;
        Calendar exCouponCalendar_;
        BusinessDayConvention exCouponAdjustment_ = Following;
        bool exCouponEndOfMonth_ = false;
    };

    inline void FixedRateCoupon::accept(AcyclicVisitor& v) {
        auto* v1 = dynamic_cast<Visitor<FixedRateCoupon>*>(&v);
        if (v1 != nullptr)
            v1->visit(*this);
        else
            Coupon::accept(v);
    }

}


#endif
