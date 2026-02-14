Calendar lastRecentPeriodCalendar_;
        std::vector<Date> paymentDates_;
        ext::shared_ptr<OvernightIndexedCouponPricer> couponPricer_;
    };

}

#endif