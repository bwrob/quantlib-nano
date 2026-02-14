MakeVanillaSwap& withAtParCoupons(bool b = true);
      private:
        Period swapTenor_;
        ext::shared_ptr<IborIndex> iborIndex_;
        Rate fixedRate_;
        Period forwardStart_;

        Natural settlementDays_ = Null<Natural>();
        Date effectiveDate_, terminationDate_;
        Calendar fixedCalendar_, floatCalendar_;

        Swap::Type type_ = Swap::Payer;
        Real nominal_ = 1.0;
        Period fixedTenor_, floatTenor_;
        BusinessDayConvention fixedConvention_ = ModifiedFollowing,
                              fixedTerminationDateConvention_ = ModifiedFollowing;
        BusinessDayConvention floatConvention_, floatTerminationDateConvention_;
        DateGeneration::Rule fixedRule_ = DateGeneration::Backward,
                             floatRule_ = DateGeneration::Backward;
        bool fixedEndOfMonth_ = false, floatEndOfMonth_ = false;
        Date fixedFirstDate_, fixedNextToLastDate_;
        Date floatFirstDate_, floatNextToLastDate_;
        Spread floatSpread_ = 0.0;
        DayCounter fixedDayCount_, floatDayCount_;
        ext::optional<bool> useIndexedCoupons_;
        ext::optional<BusinessDayConvention> paymentConvention_;

        ext::shared_ptr<PricingEngine> engine_;
    };

}

#endif
