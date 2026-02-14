hared_ptr<ZeroInflationIndex> index_;
        Period observationLag_;
        CPI::InterpolationType observationInterpolation_;
    };


    class CPICapFloor::arguments : public virtual PricingEngine::arguments {
      public:
        Option::Type type;
        Real nominal;
        Date startDate, fixDate, payDate;
        Real baseCPI;
        Date maturity;
        Calendar fixCalendar, payCalendar;
        BusinessDayConvention fixConvention, payConvention;
        Rate strike;
        ext::shared_ptr<ZeroInflationIndex> index;
        Period observationLag;
        CPI::InterpolationType observationInterpolation;

        void validate() const override;
    };

    class CPICapFloor::engine : public GenericEngine<CPICapFloor::arguments,
                                                     CPICapFloor::results> {};

}


#endif
