cross-currency basis swaps
    /*!
    Unlike marked-to-market cross currency swaps, both notionals
    expressed in base and quote currency remain constant throughout
    the lifetime of the swap.

    Note on used conventions. Consider a currency pair EUR-USD.
    EUR is the base currency, while USD is the quote currency.
    The quote currency indicates the amount to be paid in that
    currency for one unit of base currency.
    Hence, for a cross currency swap we define a base currency
    leg and a quote currency leg. The parameters of the instrument,
    e.g. collateral currency, basis, resetting  or constant notional
    legs are defined relative to what base and quote currencies are.
    For example, in case of EUR-USD basis swaps the collateral is paid
    in quote currency (USD), the basis is given on the base currency
    leg (EUR), etc.

    For more details see:
    N. Moreni, A. Pallavicini (2015)
    FX Modelling in Collateralized Markets: foreign measures, basis curves
    and pricing formulae.
    */
    class ConstNotionalCrossCurrencyBasisSwapRateHelper : public CrossCurrencyBasisSwapRateHelperBase {
      public:
        ConstNotionalCrossCurrencyBasisSwapRateHelper(
            const Handle<Quote>& basis,
            const Period& tenor,
            Natural fixingDays,
            const Calendar& calendar,
            BusinessDayConvention convention,
            bool endOfMonth,
            const ext::shared_ptr<IborIndex>& baseCurrencyIndex,
            const ext::shared_ptr<IborIndex>& quoteCurrencyIndex,
            const Handle<YieldTermStructure>& collateralCurve,
            bool isFxBaseCurrencyCollateralCurrency,
            bool isBasisOnFxBaseCurrencyLeg,
            Frequency paymentFrequency = NoFrequency,
            Integer paymentLag = 0);
        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
    };


    //! Rate helper for bootstrapping over market-to-market cross-currency basis swaps
    /*!
    Helper for a cross currency swap with resetting notional.
    This means that at each interest payment the notional on the MtM
    leg is being reset to reflect the changes in the FX rate - reducing
    the counterparty and FX risk of the structure.

    For more details see:
    N. Moreni, A. Pallavicini (2015)
    FX Modelling in Collateralized Markets: foreign measures, basis curves
    and pricing formulae.
    */
    class MtMCrossCurrencyBasisSwapRateHelper : public CrossCurrencyBasisSwapRateHelperBase {
      public:
        MtMCrossCurrencyBasisSwapRateHelper(const Handle<Quote>& basis,
                                            const Period& tenor,
                                            Natural fixingDays,
                                            const Calendar& calendar,
                                            BusinessDayConvention convention,
                                            bool endOfMonth,
                                            const ext::shared_ptr<IborIndex>& baseCurrencyIndex,
                                            const ext::shared_ptr<IborIndex>& quoteCurrencyIndex,
                                            const Handle<YieldTermStructure>& collateralCurve,
                                            bool isFxBaseCurrencyCollateralCurrency,
                                            bool isBasisOnFxBaseCurrencyLeg,
                                            bool isFxBaseCurrencyLegResettable,
                                            Frequency paymentFrequency = NoFrequency,
                                            Integer paymentLag = 0);
        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      private:
        bool isF
