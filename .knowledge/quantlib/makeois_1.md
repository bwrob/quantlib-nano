ate:
        Period swapTenor_;
        ext::shared_ptr<OvernightIndex> overnightIndex_;
        Rate fixedRate_;
        Period forwardStart_;

        Natural settlementDays_ = Null<Natural>();
        Date effectiveDate_, terminationDate_;
        Calendar fixedCalendar_, overnightCalendar_;

        Frequency fixedPaymentFrequency_ = Annual;
        Frequency overnightPaymentFrequency_ = Annual;
        Calendar paymentCalendar_;
        BusinessDayConvention paymentAdjustment_ = Following;
        Integer paymentLag_ = 0;

        BusinessDayConvention fixedConvention_ = ModifiedFollowing,
                              fixedTerminationDateConvention_ = ModifiedFollowing,
                              overnightConvention_ = ModifiedFollowing,
                              overnightTerminationDateConvention_ = ModifiedFollowing;
        DateGeneration::Rule fixedRule_ = DateGeneration::Backward;
        DateGeneration::Rule overnightRule_ = DateGeneration::Backward;
        bool fixedEndOfMonth_ = false, overnightEndOfMonth_ = false, isDefaultEOM_ = true;

        Swap::Type type_ = Swap::Payer;
        Real nominal_ = 1.0;

        Spread overnightSpread_ = 0.0;
        DayCounter fixedDayCount_;

        ext::shared_ptr<PricingEngine> engine_;

        bool telescopicValueDates_ = false;
        RateAveraging::Type averagingMethod_ = RateAveraging::Compound;
        Natural lookbackDays_ = Null<Natural>();
        Natural lockoutDays_ = 0;
        bool applyObservationShift_ = false;
    };

}

#endif