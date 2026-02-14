eroCouponInflationSwapHelper(
            const Handle<Quote>& quote,
            const Period& swapObsLag,
            const Date& startDate,
            const Date& endDate,
            Calendar calendar,
            BusinessDayConvention paymentConvention,
            DayCounter dayCounter,
            const ext::shared_ptr<ZeroInflationIndex>& zii,
            CPI::InterpolationType observationInterpolation,
            Handle<YieldTermStructure> nominalTermStructure);
    };


    //! Year-on-year inflation-swap bootstrap helper
    class YearOnYearInflationSwapHelper
        : public RelativeDateBootstrapHelper<YoYInflationTermStructure> {
      public:
        YearOnYearInflationSwapHelper(const Handle<Quote>& quote,
                                      const Period& swapObsLag,
                                      const Date& maturity,
                                      Calendar calendar,
                                      BusinessDayConvention paymentConvention,
                                      DayCounter dayCounter,
                                      const ext::shared_ptr<YoYInflationIndex>& yii,
                                      CPI::InterpolationType interpolation,
                                      Handle<YieldTermStructure> nominalTermStructure);

        YearOnYearInflationSwapHelper(const Handle<Quote>& quote,
                                      const Period& swapObsLag,
                                      const Date& startDate,
                                      const Date& endDate,
                                      Calendar calendar,
                                      BusinessDayConvention paymentConvention,
                                      DayCounter dayCounter,
                                      const ext::shared_ptr<YoYInflationIndex>& yii,
                                      CPI::InterpolationType interpolation,
                                      Handle<YieldTermStructure> nominalTermStructure);

        void setTermStructure(YoYInflationTermStructure*) override;
        Real impliedQuote() const override;
        //! \name inspectors
        //@{
        // NOLINTNEXTLINE(cppcoreguidelines-noexcept-swap,performance-noexcept-swap)
        ext::shared_ptr<YearOnYearInflationSwap> swap() const { return yyiis_; }
        //@}
      protected:
        void initializeDates() override;

        Period swapObsLag_;
        Date startDate_, maturity_;
        Calendar calendar_;
        BusinessDayConvention paymentConvention_;
        DayCounter dayCounter_;
        ext::shared_ptr<YoYInflationIndex> yii_;
        CPI::InterpolationType interpolation_;
        ext::shared_ptr<YearOnYearInflationSwap> yyiis_;
        Handle<YieldTermStructure> nominalTermStructure_;
        RelinkableHandle<YoYInflationTermStructure> termStructureHandle_;
    };

}


#endif
