       a trading calendar to the ON and TN helpers and
                 provide fwdPoints that will yield proper level of
                 discount factors.
    */
    class FxSwapRateHelper : public RelativeDateRateHelper {
      public:
        FxSwapRateHelper(const Handle<Quote>& fwdPoint,
                         Handle<Quote> spotFx,
                         const Period& tenor,
                         Natural fixingDays,
                         Calendar calendar,
                         BusinessDayConvention convention,
                         bool endOfMonth,
                         bool isFxBaseCurrencyCollateralCurrency,
                         Handle<YieldTermStructure> collateralCurve,
                         Calendar tradingCalendar = Calendar());
        FxSwapRateHelper(const Handle<Quote>& fwdPoint,
                         Handle<Quote> spotFx,
                         const Date& startDate,
                         const Date& endDate,
                         bool isFxBaseCurrencyCollateralCurrency,
                         Handle<YieldTermStructure> collateralCurve);
        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        void setTermStructure(YieldTermStructure*) override;
        //@}
        //! \name FxSwapRateHelper inspectors
        //@{
        Real spot() const { return spot_->value(); }
        Period tenor() const { return tenor_; }
        Natural fixingDays() const { return fixingDays_; }
        Calendar calendar() const { return cal_; }
        BusinessDayConvention businessDayConvention() const { return conv_; }
        bool endOfMonth() const { return eom_; }
        bool isFxBaseCurrencyCollateralCurrency() const {
                                return isFxBaseCurrencyCollateralCurrency_; }
        Calendar tradingCalendar() const { return tradingCalendar_; }
        Calendar adjustmentCalendar() const { return jointCalendar_; }
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
    private:
      void initializeDates() override;
      Handle<Quote> spot_;
      Period tenor_;
      Natural fixingDays_;
      Calendar cal_;
      BusinessDayConvention conv_;
      bool eom_;
      bool isFxBaseCurrencyCollateralCurrency_;

      RelinkableHandle<YieldTermStructure> termStructureHandle_;

      Handle<YieldTermStructure> collHandle_;
      RelinkableHandle<YieldTermStructure> collRelinkableHandle_;

      Calendar tradingCalendar_;
      Calendar jointCalendar_;
    };

    // inline

    inline Spread SwapRateHelper::spread() const {
        return spread_.empty() ? 0.0 : spread_->value();
    }

    // NOLINTNEXTLINE(cppcoreguidelines-noexcept-swap,performance-noexcept-swap)
    inline ext::shared_ptr<VanillaSwap> SwapRateHelper::swap() const {
        return swap_;
    }

    inline const Period& SwapRateHelper::forwardStart() const {
        return fwdStart_;
    }

}

#endif