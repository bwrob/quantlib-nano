s*) const override;

      private:
        void setupExpired() const override;
        virtual void setupFloatingArguments(arguments* args) const = 0;
        Type type_;
        std::vector<Real> fixedNominals_;
        Schedule fixedSchedule_;
        Rate fixedRate_;
        DayCounter fixedDayCount_;
        std::vector<Real> floatingNominals_;
        Schedule floatingSchedule_;
        ext::shared_ptr<IborIndex> iborIndex_;
        Spread spread_;
        DayCounter floatingDayCount_;
        BusinessDayConvention paymentConvention_;
        // results
        mutable Rate fairRate_;
        mutable Spread fairSpread_;

        bool constantNominals_, sameNominals_;
    };


    //! %Arguments for simple swap calculation
    class FixedVsFloatingSwap::arguments : public Swap::arguments {
      public:
        arguments() : nominal(Null<Real>()) {}
        Type type = Receiver;
        Real nominal;

        std::vector<Real> fixedNominals;
        std::vector<Date> fixedResetDates;
        std::vector<Date> fixedPayDates;
        std::vector<Real> floatingNominals;
        std::vector<Time> floatingAccrualTimes;
        std::vector<Date> floatingResetDates;
        std::vector<Date> floatingFixingDates;
        std::vector<Date> floatingPayDates;

        std::vector<Real> fixedCoupons;
        std::vector<Spread> floatingSpreads;
        std::vector<Real> floatingCoupons;
        void validate() const override;
    };

    //! %Results from simple swap calculation
    class FixedVsFloatingSwap::results : public Swap::results {
      public:
        Rate fairRate;
        Spread fairSpread;
        void reset() override;
    };

    class FixedVsFloatingSwap::engine : public GenericEngine<FixedVsFloatingSwap::arguments,
                                                             FixedVsFloatingSwap::results> {};


    // inline definitions

    inline Swap::Type FixedVsFloatingSwap::type() const {
        return type_;
    }

    inline Real FixedVsFloatingSwap::nominal() const {
        QL_REQUIRE(constantNominals_, "nominal is not constant");
        return fixedNominals_[0];
    }

    inline const std::vector<Real>& FixedVsFloatingSwap::nominals() const {
        QL_REQUIRE(sameNominals_, "different nominals on fixed and floating leg");
        return fixedNominals_;
    }

    inline const std::vector<Real>& FixedVsFloatingSwap::fixedNominals() const {
        return fixedNominals_;
    }

    inline const Schedule& FixedVsFloatingSwap::fixedSchedule() const {
        return fixedSchedule_;
    }

    inline Rate FixedVsFloatingSwap::fixedRate() const {
        return fixedRate_;
    }

    inline const DayCounter& FixedVsFloatingSwap::fixedDayCount() const {
        return fixedDayCount_;
    }

    inline const std::vector<Real>& FixedVsFloatingSwap::floatingNominals() const {
        return floatingNominals_;
    }

    inline const Schedule& FixedVsFloatingSwap::floatingSchedule() const {
        return floatingSchedule_;
    }

    inline const ext::shared_ptr<IborIndex>& FixedVsFloatingSwap::iborIndex() const {
        return iborIndex_;
    }

    inline Spread FixedVsFloatingSwap::spread() const {
        return spread_;
    }

    inline const DayCounter& FixedVsFloatingSwap::floatingDayCount() const {
        return floatingDayCount_;
    }

    inline BusinessDayConvention FixedVsFloatingSwap::paymentConvention() const {
        return paymentConvention_;
    }

    inline const Leg& FixedVsFloatingSwap::fixedLeg() const {
        return legs_[0];
    }

    inline const Leg& FixedVsFloatingSwap::floatingLeg() const {
        return legs_[1];
    }

}

#endif