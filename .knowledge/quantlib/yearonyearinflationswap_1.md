sDayConvention paymentConvention_;
        // results
        mutable Rate fairRate_;
        mutable Spread fairSpread_;
    };


    //! %Arguments for YoY swap calculation
    class YearOnYearInflationSwap::arguments : public Swap::arguments {
    public:
      arguments() : nominal(Null<Real>()) {}
      Type type = Receiver;
      Real nominal;

      std::vector<Date> fixedResetDates;
      std::vector<Date> fixedPayDates;
      std::vector<Time> yoyAccrualTimes;
      std::vector<Date> yoyResetDates;
      std::vector<Date> yoyFixingDates;
      std::vector<Date> yoyPayDates;

      std::vector<Real> fixedCoupons;
      std::vector<Spread> yoySpreads;
      std::vector<Real> yoyCoupons;
      void validate() const override;
    };

    //! %Results from YoY swap calculation
    class YearOnYearInflationSwap::results : public Swap::results {
    public:
        Rate fairRate;
        Spread fairSpread;
        void reset() override;
    };

    class YearOnYearInflationSwap::engine : public GenericEngine<YearOnYearInflationSwap::arguments,
                                                                 YearOnYearInflationSwap::results> {};


    // inline definitions

    inline Swap::Type YearOnYearInflationSwap::type() const {
        return type_;
    }

    inline Real YearOnYearInflationSwap::nominal() const {
        return nominal_;
    }

    inline const Schedule& YearOnYearInflationSwap::fixedSchedule() const {
        return fixedSchedule_;
    }

    inline Rate YearOnYearInflationSwap::fixedRate() const {
        return fixedRate_;
    }

    inline const DayCounter& YearOnYearInflationSwap::fixedDayCount() const {
        return fixedDayCount_;
    }

    inline const Schedule& YearOnYearInflationSwap::yoySchedule() const {
        return yoySchedule_;
    }

    inline const ext::shared_ptr<YoYInflationIndex>& YearOnYearInflationSwap::yoyInflationIndex() const {
        return yoyIndex_;
    }

    inline Spread YearOnYearInflationSwap::spread() const {
        return spread_;
    }

    inline const DayCounter& YearOnYearInflationSwap::yoyDayCount() const {
        return yoyDayCount_;
    }

    inline BusinessDayConvention YearOnYearInflationSwap::paymentConvention() const {
        return paymentConvention_;
    }

    inline const Leg& YearOnYearInflationSwap::fixedLeg() const {
        return legs_[0];
    }

    inline const Leg& YearOnYearInflationSwap::yoyLeg() const {
        return legs_[1];
    }

}

#endif
