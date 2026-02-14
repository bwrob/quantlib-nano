ide;
        void fetchResults(const PricingEngine::results*) const override;

      private:
        void init();
        void setupExpired() const override;
        Swap::Type type_;
        std::vector<Real> fixedNominal_, floatingNominal_;
        Schedule fixedSchedule_;
        std::vector<Real> fixedRate_;
        DayCounter fixedDayCount_;
        Schedule floatingSchedule_;
        ext::shared_ptr<IborIndex> iborIndex_;
        std::vector<Spread> spread_;
        std::vector<Real> gearing_;
        bool singleSpreadAndGearing_;
        DayCounter floatingDayCount_;
        BusinessDayConvention paymentConvention_;
        const bool intermediateCapitalExchange_;
        const bool finalCapitalExchange_;
        // results
    };

    //! %Arguments for nonstandard swap calculation
    class NonstandardSwap::arguments : public Swap::arguments {
      public:
        arguments() = default;
        Swap::Type type = Swap::Receiver;
        std::vector<Real> fixedNominal, floatingNominal;

        std::vector<Date> fixedResetDates;
        std::vector<Date> fixedPayDates;
        std::vector<Time> floatingAccrualTimes;
        std::vector<Date> floatingResetDates;
        std::vector<Date> floatingFixingDates;
        std::vector<Date> floatingPayDates;

        std::vector<Real> fixedCoupons;
        std::vector<Real> fixedRate;
        std::vector<Spread> floatingSpreads;
        std::vector<Real> floatingGearings;
        std::vector<Real> floatingCoupons;

        ext::shared_ptr<IborIndex> iborIndex;

        std::vector<bool> fixedIsRedemptionFlow;
        std::vector<bool> floatingIsRedemptionFlow;

        void validate() const override;
    };

    //! %Results from nonstandard swap calculation
    class NonstandardSwap::results : public Swap::results {
      public:
        void reset() override;
    };

    class NonstandardSwap::engine
        : public GenericEngine<NonstandardSwap::arguments,
                               NonstandardSwap::results> {};

    // inline definitions

    inline Swap::Type NonstandardSwap::type() const { return type_; }

    inline const std::vector<Real> &NonstandardSwap::fixedNominal() const {
        return fixedNominal_;
    }

    inline const std::vector<Real> &NonstandardSwap::floatingNominal() const {
        return floatingNominal_;
    }

    inline const Schedule &NonstandardSwap::fixedSchedule() const {
        return fixedSchedule_;
    }

    inline const std::vector<Real> &NonstandardSwap::fixedRate() const {
        return fixedRate_;
    }

    inline const DayCounter &NonstandardSwap::fixedDayCount() const {
        return fixedDayCount_;
    }

    inline const Schedule &NonstandardSwap::floatingSchedule() const {
        return floatingSchedule_;
    }

    inline const ext::shared_ptr<IborIndex> &
    NonstandardSwap::iborIndex() const {
        return iborIndex_;
    }

    inline Spread NonstandardSwap::spread() const {
        QL_REQUIRE(singleSpreadAndGearing_,
                   "spread is a vector, use spreads inspector instead");
        return spread_.front();
    }

    inline Real NonstandardSwap::gearing() const {
        QL_REQUIRE(singleSpreadAndGearing_,
                   "gearing is a vector, use gearings inspector instead");
        return gearing_.front();
    }

    inline const std::vector<Spread> &NonstandardSwap::spreads() const {
        return spread_;
    }

    inline const std::vector<Real> &NonstandardSwap::gearings() const {
        return gearing_;
    }

    inline const DayCounter &NonstandardSwap::floatingDayCount() const {
        return floatingDayCount_;
    }

    inline BusinessDayConvention NonstandardSwap::paymentConvention() const {
        return paymentConvention_;
    }

    inline const Leg &NonstandardSwap::fixedLeg() const { return legs_[0]; }

    inline const Leg &NonstandardSwap::floatingLeg() const { return legs_[1]; }
}

#endif