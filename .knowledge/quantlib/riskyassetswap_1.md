 tenor_;
        Natural settlementDays_;
        Calendar calendar_;
        BusinessDayConvention fixedConvention_;
        Period fixedPeriod_;
        DayCounter fixedDayCount_;
        BusinessDayConvention floatConvention_;
        Period floatPeriod_;
        DayCounter floatDayCount_;
        Real recoveryRate_;
        RelinkableHandle<YieldTermStructure> yieldTS_;
        Period integrationStepSize_;

        Date evaluationDate_;
        ext::shared_ptr<RiskyAssetSwap> asw_;
        RelinkableHandle<DefaultProbabilityTermStructure> probability_;
    };

}

#endif