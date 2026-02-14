        const ext::shared_ptr<InterestRateIndex> &index1() const;
        const ext::shared_ptr<InterestRateIndex> &index2() const;

        std::vector<Real> spread1() const;
        std::vector<Real> spread2() const;

        std::vector<Real> gearing1() const;
        std::vector<Real> gearing2() const;

        std::vector<Rate> cappedRate1() const;
        std::vector<Rate> flooredRate1() const;
        std::vector<Rate> cappedRate2() const;
        std::vector<Rate> flooredRate2() const;

        const DayCounter &dayCount1() const;
        const DayCounter &dayCount2() const;

        BusinessDayConvention paymentConvention1() const;
        BusinessDayConvention paymentConvention2() const;

        const Leg &leg1() const;
        const Leg &leg2() const;
        //@}

        //! \name Results
        //@{
        //@}
        // other
        void setupArguments(PricingEngine::arguments* args) const override;
        void fetchResults(const PricingEngine::results*) const override;

      private:
        void init(ext::optional<BusinessDayConvention> paymentConvention1,
                  ext::optional<BusinessDayConvention> paymentConvention2);
        void setupExpired() const override;
        Swap::Type type_;
        std::vector<Real> nominal1_, nominal2_;
        Schedule schedule1_, schedule2_;
        ext::shared_ptr<InterestRateIndex> index1_, index2_;
        std::vector<Real> gearing1_, gearing2_, spread1_, spread2_;
        std::vector<Real> cappedRate1_, flooredRate1_, cappedRate2_,
            flooredRate2_;
        DayCounter dayCount1_, dayCount2_;
        std::vector<bool> isRedemptionFlow1_, isRedemptionFlow2_;
        BusinessDayConvention paymentConvention1_, paymentConvention2_;
        const bool intermediateCapitalExchange_, finalCapitalExchange_;
    };

    //! %Arguments for float float swap calculation
    class FloatFloatSwap::arguments : public Swap::arguments {
      public:
        arguments() = default;
        Swap::Type type = Swap::Receiver;
        std::vector<Real> nominal1, nominal2;

        std::vector<Date> leg1ResetDates, leg1FixingDates, leg1PayDates;
        std::vector<Date> leg2ResetDates, leg2FixingDates, leg2PayDates;

        std::vector<Real> leg1Spreads, leg2Spreads, leg1Gearings, leg2Gearings;
        std::vector<Real> leg1CappedRates, leg1FlooredRates, leg2CappedRates,
            leg2FlooredRates;

        std::vector<Real> leg1Coupons, leg2Coupons;
        std::vector<Real> leg1AccrualTimes, leg2AccrualTimes;

        ext::shared_ptr<InterestRateIndex> index1, index2;

        std::vector<bool> leg1IsRedemptionFlow, leg2IsRedemptionFlow;

        void validate() const override;
    };

    //! %Results from float float swap calculation
    class FloatFloatSwap::results : public Swap::results {
      public:
        void reset() override;
    };

    class FloatFloatSwap::engine
        : public GenericEngine<FloatFloatSwap::arguments,
                               FloatFloatSwap::results> {};

    // inline definitions

    inline Swap::Type FloatFloatSwap::type() const { return type_; }

    inline const std::vector<Real> &FloatFloatSwap::nominal1() const {
        return nominal1_;
    }

    inline const std::vector<Real> &FloatFloatSwap::nominal2() const {
        return nominal2_;
    }

    inline const Schedule &FloatFloatSwap::schedule1() const {
        return schedule1_;
    }

    inline const Schedule &FloatFloatSwap::schedule2() const {
        return schedule2_;
    }

    inline const ext::shared_ptr<InterestRateIndex> &
    FloatFloatSwap::index1() const {
        return index1_;
    }

    inline const ext::shared_ptr<InterestRateIndex> &
    FloatFloatSwap::index2() const {
        return index2_;
    }

    inline std::vector<Real> FloatFloatSwap::spread1() const { return spread1_; }

    inline std::vector<Real> FloatFloatSwap::spread2() const { return spread2_; }

    inline std::vector<Real> FloatFloatSwap::gearing1() const { return gearing1