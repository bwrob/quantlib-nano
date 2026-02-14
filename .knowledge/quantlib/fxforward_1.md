 pay target currency
            \param settlementDays    Number of business days for payment settlement
                                     (0=O/N, 1=T/N, 2=Spot, default=2)
            \param paymentCalendar   Calendar for computing payment date
                                     (defaults to NullCalendar)
        */
        FxForward(Real sourceNominal,
                  const Currency& sourceCurrency,
                  const Currency& targetCurrency,
                  Real forwardRate,
                  const Date& maturityDate,
                  bool paySourceCurrency,
                  Natural settlementDays = 2,
                  const Calendar& paymentCalendar = Calendar());
        //@}

        //! \name Inspectors
        //@{
        //! Source nominal amount
        Real sourceNominal() const { return sourceNominal_; }
        //! Source currency
        const Currency& sourceCurrency() const { return sourceCurrency_; }
        //! Target nominal amount
        Real targetNominal() const { return targetNominal_; }
        //! Target currency
        const Currency& targetCurrency() const { return targetCurrency_; }
        //! Maturity date of the forward contract
        const Date& maturityDate() const { return maturityDate_; }
        //! True if paying source currency
        bool paySourceCurrency() const { return paySourceCurrency_; }
        //! Contracted forward rate (target currency per unit of source currency)
        Real forwardRate() const { return targetNominal_ / sourceNominal_; }
        //! Number of settlement days (0=O/N, 1=T/N, 2=Spot)
        Natural settlementDays() const { return settlementDays_; }
        //! Settlement calendar
        const Calendar& settlementCalendar() const { return paymentCalendar_; }
        //! Settlement date (computed from evaluation date + settlementDays)
        Date settlementDate() const;
        //@}

        //! \name Instrument interface
        //@{
        bool isExpired() const override;
        void setupArguments(PricingEngine::arguments*) const override;
        void fetchResults(const PricingEngine::results*) const override;
        //@}

        //! \name Additional results
        //@{
        //! Fair forward rate (targetCurrency/sourceCurrency), the market-implied fair rate
        //! computed by the engine
        Real fairForwardRate() const;
        //! NPV in source currency terms
        Real npvSourceCurrency() const;
        //! NPV in target currency terms
        Real npvTargetCurrency() const;
        //@}

      private:
        Real sourceNominal_;
        Currency sourceCurrency_;
        Real targetNominal_;
        Currency targetCurrency_;
        Date maturityDate_;
        bool paySourceCurrency_;
        Natural settlementDays_;
        Calendar paymentCalendar_;

        mutable Real fairForwardRate_;
        mutable Real npvSourceCurrency_;
        mutable Real npvTargetCurrency_;
    };

    //! Arguments for FX Forward pricing engine
    class FxForward::arguments : public virtual PricingEngine::arguments {
      public:
        Real sourceNominal = Null<Real>();
        Currency sourceCurrency;
        Real targetNominal = Null<Real>();
        Currency targetCurrency;
        Date maturityDate;
        bool paySourceCurrency = true;
        Date settlementDate;
        void validate() const override;
    };

    //! Results for FX Forward pricing engine
    class FxForward::results : public Instrument::results {
      public:
        Real fairForwardRate = Null<Real>();
        Real npvSourceCurrency = Null<Real>();
        Real npvTargetCurrency = Null<Real>();
        void reset() override;
    };

    //! Base class for FX Forward pricing engines
    class FxForward::engine : public GenericEngine<FxForward::arguments, FxForward::results> {};

}

#endif
