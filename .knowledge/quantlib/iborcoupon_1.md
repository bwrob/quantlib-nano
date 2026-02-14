meIndexMaturity_;

      public:
        // IborCoupon::Settings forward declaration
        class Settings;
    };


    //! Per-session settings for IborCoupon class
    class IborCoupon::Settings : public Singleton<IborCoupon::Settings> {
        friend class Singleton<IborCoupon::Settings>;
      private:
        Settings() = default;

      public:
        //! When called, IborCoupons are created as indexed coupons instead of par coupons.
        void createAtParCoupons();

        //! When called, IborCoupons are created as par coupons instead of indexed coupons.
        void createIndexedCoupons();

        /*! If true the IborCoupons are created as par coupons and vice versa.
            The default depends on the compiler flag QL_USE_INDEXED_COUPON and can be overwritten by
            createAtParCoupons() and createIndexedCoupons() */
        bool usingAtParCoupons() const;

      private:
        #ifndef QL_USE_INDEXED_COUPON
        bool usingAtParCoupons_ = true;
        #else
        bool usingAtParCoupons_ = false;
        #endif
    };

    //! helper class building a sequence of capped/floored ibor-rate coupons
    class IborLeg {
      public:
        IborLeg(Schedule schedule, ext::shared_ptr<IborIndex> index);
        IborLeg& withNotionals(Real notional);
        IborLeg& withNotionals(const std::vector<Real>& notionals);
        IborLeg& withPaymentDayCounter(const DayCounter&);
        IborLeg& withPaymentAdjustment(BusinessDayConvention);
        IborLeg& withPaymentLag(Integer lag);
        IborLeg& withPaymentCalendar(const Calendar&);
        IborLeg& withFixingDays(Natural fixingDays);
        IborLeg& withFixingDays(const std::vector<Natural>& fixingDays);
        IborLeg& withGearings(Real gearing);
        IborLeg& withGearings(const std::vector<Real>& gearings);
        IborLeg& withSpreads(Spread spread);
        IborLeg& withSpreads(const std::vector<Spread>& spreads);
        IborLeg& withCaps(Rate cap);
        IborLeg& withCaps(const std::vector<Rate>& caps);
        IborLeg& withFloors(Rate floor);
        IborLeg& withFloors(const std::vector<Rate>& floors);
        IborLeg& inArrears(bool flag = true);
        IborLeg& withZeroPayments(bool flag = true);
        IborLeg& withExCouponPeriod(const Period&,
                                    const Calendar&,
                                    BusinessDayConvention,
                                    bool endOfMonth = false);
        IborLeg& withIndexedCoupons(ext::optional<bool> b = true);
        IborLeg& withAtParCoupons(bool b = true);
        operator Leg() const;

      private:
        Schedule schedule_;
        ext::shared_ptr<IborIndex> index_;
        std::vector<Real> notionals_;
        DayCounter paymentDayCounter_;
        BusinessDayConvention paymentAdjustment_ = Following;
        Integer paymentLag_ = 0;
        Calendar paymentCalendar_;
        std::vector<Natural> fixingDays_;
        std::vector<Real> gearings_;
        std::vector<Spread> spreads_;
        std::vector<Rate> caps_, floors_;
        bool inArrears_ = false, zeroPayments_ = false;
        Period exCouponPeriod_;
        Calendar exCouponCalendar_;
        BusinessDayConvention exCouponAdjustment_ = Unadjusted;
        bool exCouponEndOfMonth_ = false;
        ext::optional<bool> useIndexedCoupons_;
    };

}

#endif