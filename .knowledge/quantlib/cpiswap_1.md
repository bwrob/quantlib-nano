bool subtractInflationNominal() const;

        // float+spread
        virtual Spread spread() const;
        virtual const DayCounter& floatDayCount() const;
        virtual const Schedule& floatSchedule() const;
        virtual const BusinessDayConvention& floatPaymentRoll() const;
        virtual Natural fixingDays() const;
        virtual const ext::shared_ptr<IborIndex>& floatIndex() const;

        // fixed rate x inflation
        virtual Rate fixedRate() const;
        virtual Real baseCPI() const;
        virtual const DayCounter& fixedDayCount() const;
        virtual const Schedule& fixedSchedule() const;
        virtual const BusinessDayConvention& fixedPaymentRoll() const;
        virtual Period observationLag() const;
        virtual const ext::shared_ptr<ZeroInflationIndex>& fixedIndex() const;
        virtual CPI::InterpolationType observationInterpolation() const;
        virtual Real inflationNominal() const;

        // legs
        virtual const Leg& cpiLeg() const;
        virtual const Leg& floatLeg() const;

        // other
        void setupArguments(PricingEngine::arguments* args) const override;
        void fetchResults(const PricingEngine::results*) const override;

      private:
        void setupExpired() const override;

        Type type_;
        Real nominal_;
        bool subtractInflationNominal_;

        // float+spread leg
        Spread spread_;
        DayCounter floatDayCount_;
        Schedule floatSchedule_;
        BusinessDayConvention floatPaymentRoll_;
        Natural fixingDays_;
        ext::shared_ptr<IborIndex> floatIndex_;

        // fixed x inflation leg
        Rate fixedRate_;
        Real baseCPI_;
        DayCounter fixedDayCount_;
        Schedule fixedSchedule_;
        BusinessDayConvention fixedPaymentRoll_;
        ext::shared_ptr<ZeroInflationIndex> fixedIndex_;
        Period observationLag_;
        CPI::InterpolationType observationInterpolation_;
        Real inflationNominal_;
        // results
        mutable Spread fairSpread_;
        mutable Rate fairRate_;

    };


    //! %Arguments for swap calculation
    class CPISwap::arguments : public Swap::arguments {
    public:
      arguments() : nominal(Null<Real>()) {}
      Type type = Receiver;
      Real nominal;

      void validate() const override;
    };

    //! %Results from swap calculation
    class CPISwap::results : public Swap::results {
    public:
        Rate fairRate;
        Spread fairSpread;
        void reset() override;
    };

    class CPISwap::engine : public GenericEngine<CPISwap::arguments,
                                                 CPISwap::results> {};


    // inline definitions

    // inspectors
    inline  Swap::Type CPISwap::type() const { return type_; }
    inline  Real CPISwap::nominal() const { return nominal_; }
    inline  bool CPISwap::subtractInflationNominal() const { return subtractInflationNominal_; }

    // float+spread
    inline Spread CPISwap::spread() const { return spread_; }
    inline const DayCounter& CPISwap::floatDayCount() const { return floatDayCount_; }
    inline const Schedule& CPISwap::floatSchedule() const { return floatSchedule_; }
    inline const BusinessDayConvention& CPISwap::floatPaymentRoll() const { return floatPaymentRoll_; }
    inline Natural CPISwap::fixingDays() const { return fixingDays_; }
    inline const ext::shared_ptr<IborIndex>& CPISwap::floatIndex() const { return floatIndex_; }

    // fixed rate x inflation
    inline Rate CPISwap::fixedRate() const { return fixedRate_; }
    inline Real CPISwap::baseCPI() const { return baseCPI_; }
    inline const DayCounter& CPISwap::fixedDayCount() const { return fixedDayCount_; }
    inline const Schedule& CPISwap::fixedSchedule() const { return fixedSchedule_; }
    inline const BusinessDayConvention& CPISwap::fixedPaymentRoll() const { return fixedPaymentRoll_; }
    inline Period CPISwap::observationLag() const { return observationLag_; }
    inline const ext::shared_p
