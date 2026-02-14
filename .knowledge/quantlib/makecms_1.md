ion_;
        BusinessDayConvention floatConvention_, floatTerminationDateConvention_;
        DateGeneration::Rule cmsRule_, floatRule_;
        bool cmsEndOfMonth_, floatEndOfMonth_;
        Date cmsFirstDate_, cmsNextToLastDate_;
        Date floatFirstDate_, floatNextToLastDate_;
        DayCounter cmsDayCount_, floatDayCount_;

        ext::shared_ptr<PricingEngine> engine_;
        ext::shared_ptr<CmsCouponPricer> couponPricer_;
    };

}

#endif
