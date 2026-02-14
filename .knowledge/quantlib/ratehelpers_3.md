red_ptr<IborIndex>& iborIndex,
                        Date customPillarDate);
        void initializeDates() override;
        Natural settlementDays_;
        Period tenor_;
        Date startDate_, endDate_;
        Pillar::Choice pillarChoice_;
        Calendar calendar_;
        BusinessDayConvention fixedConvention_;
        Frequency fixedFrequency_;
        DayCounter fixedDayCount_;
        ext::shared_ptr<IborIndex> iborIndex_;
        ext::shared_ptr<VanillaSwap> swap_;
        RelinkableHandle<YieldTermStructure> termStructureHandle_;
        Handle<Quote> spread_;
        bool endOfMonth_;
        Period fwdStart_;
        Handle<YieldTermStructure> discountHandle_;
        RelinkableHandle<YieldTermStructure> discountRelinkableHandle_;
        ext::optional<bool> useIndexedCoupons_;
        ext::optional<BusinessDayConvention> floatConvention_;
    };


    //! Rate helper for bootstrapping over BMA swap rates
    class BMASwapRateHelper : public RelativeDateRateHelper {
      public:
        BMASwapRateHelper(const Handle<Quote>& liborFraction,
                          const Period& tenor, // swap maturity
                          Natural settlementDays,
                          Calendar calendar,
                          // bma leg
                          const Period& bmaPeriod,
                          BusinessDayConvention bmaConvention,
                          DayCounter bmaDayCount,
                          ext::shared_ptr<BMAIndex> bmaIndex,
                          // ibor leg
                          ext::shared_ptr<IborIndex> index);
        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        void setTermStructure(YieldTermStructure*) override;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
    protected:
      void initializeDates() override;
      Period tenor_;
      Natural settlementDays_;
      Calendar calendar_;
      Period bmaPeriod_;
      BusinessDayConvention bmaConvention_;
      DayCounter bmaDayCount_;
      ext::shared_ptr<BMAIndex> bmaIndex_;
      ext::shared_ptr<IborIndex> iborIndex_;

      ext::shared_ptr<BMASwap> swap_;
      RelinkableHandle<YieldTermStructure> termStructureHandle_;
    };


    //! Rate helper for bootstrapping over Fx Swap rates
    /*! The forward is given by `fwdFx = spotFx + fwdPoint`.

        `isFxBaseCurrencyCollateralCurrency` indicates if the base
        currency of the FX currency pair is the one used as collateral.

        `calendar` is usually the joint calendar of the two currencies
        in the pair.

        `tradingCalendar` can be used when the cross pairs don't
        include the currency of the business center (usually USD; the
        corresponding calendar is `UnitedStates`).  If given, it will
        be used for adjusting the earliest settlement date and for
        setting the latest date. Due to FX spot market conventions, it
        is not sufficient to pass a JointCalendar with UnitedStates
        included as `calendar`; with regard the earliest date, this
        calendar is only used in case the spot date of the two
        currencies is not a US business day.

        \warning The ON fx swaps can be achieved by setting
                 `fixingDays` to 0 and using a tenor of '1d'. The same
                 tenor should be used for TN swaps, with `fixingDays`
                 set to 1.  However, handling ON and TN swaps for
                 cross rates without USD is not trivial and should be
                 treated with caution. If today is a US holiday, ON
                 trade is not possible. If tomorrow is a US Holiday,
                 the ON trade will be at least two business days long
                 in the other countries and the TN trade will not
                 exist. In such cases, if this helper is used for
                 curve construction, probably it is safer not to pass

