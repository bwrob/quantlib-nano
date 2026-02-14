preadIndex> swapSpreadIndex);
        CmsSpreadLeg& withNotionals(Real notional);
        CmsSpreadLeg& withNotionals(const std::vector<Real>& notionals);
        CmsSpreadLeg& withPaymentDayCounter(const DayCounter&);
        CmsSpreadLeg& withPaymentAdjustment(BusinessDayConvention);
        CmsSpreadLeg& withFixingDays(Natural fixingDays);
        CmsSpreadLeg& withFixingDays(const std::vector<Natural>& fixingDays);
        CmsSpreadLeg& withGearings(Real gearing);
        CmsSpreadLeg& withGearings(const std::vector<Real>& gearings);
        CmsSpreadLeg& withSpreads(Spread spread);
        CmsSpreadLeg& withSpreads(const std::vector<Spread>& spreads);
        CmsSpreadLeg& withCaps(Rate cap);
        CmsSpreadLeg& withCaps(const std::vector<Rate>& caps);
        CmsSpreadLeg& withFloors(Rate floor);
        CmsSpreadLeg& withFloors(const std::vector<Rate>& floors);
        CmsSpreadLeg& inArrears(bool flag = true);
        CmsSpreadLeg& withZeroPayments(bool flag = true);
        operator Leg() const;
      private:
        Schedule schedule_;
        ext::shared_ptr<SwapSpreadIndex> swapSpreadIndex_;
        std::vector<Real> notionals_;
        DayCounter paymentDayCounter_;
        BusinessDayConvention paymentAdjustment_ = Following;
        std::vector<Natural> fixingDays_;
        std::vector<Real> gearings_;
        std::vector<Spread> spreads_;
        std::vector<Rate> caps_, floors_;
        bool inArrears_ = false, zeroPayments_ = false;
    };


    //! base pricer for vanilla CMS spread coupons
    class CmsSpreadCouponPricer : public FloatingRateCouponPricer {
      public:
        explicit CmsSpreadCouponPricer(Handle<Quote> correlation = Handle<Quote>())
        : correlation_(std::move(correlation)) {
            registerWith(correlation_);
        }

        Handle<Quote> correlation() const{
            return correlation_;
        }

        void setCorrelation(
                         const Handle<Quote> &correlation = Handle<Quote>()) {
            unregisterWith(correlation_);
            correlation_ = correlation;
            registerWith(correlation_);
            update();
        }
      private:
        Handle<Quote> correlation_;
    };

}

#endif
