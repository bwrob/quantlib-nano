      private:
        void initializeDates() override;
        Date fixingDate_;
        ext::optional<Period> periodToStart_;
        ext::optional<Natural> immOffsetStart_, immOffsetEnd_;
        Pillar::Choice pillarChoice_;
        ext::shared_ptr<IborIndex> iborIndex_;
        RelinkableHandle<YieldTermStructure> termStructureHandle_;
        bool useIndexedCoupon_;
        Real spanningTime_;
    };


    //! Rate helper for bootstrapping over swap rates
    /*! \todo use input SwapIndex to create the swap */
    class SwapRateHelper : public RelativeDateRateHelper {
      public:
        SwapRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                       const ext::shared_ptr<SwapIndex>& swapIndex,
                       Handle<Quote> spread = {},
                       const Period& fwdStart = 0 * Days,
                       // exogenous discounting curve
                       Handle<YieldTermStructure> discountingCurve = {},
                       Pillar::Choice pillar = Pillar::LastRelevantDate,
                       Date customPillarDate = Date(),
                       bool endOfMonth = false,
                       const ext::optional<bool>& useIndexedCoupons = ext::nullopt);
        SwapRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                       const Period& tenor,
                       Calendar calendar,
                       // fixed leg
                       Frequency fixedFrequency,
                       BusinessDayConvention fixedConvention,
                       DayCounter fixedDayCount,
                       // floating leg
                       const ext::shared_ptr<IborIndex>& iborIndex,
                       Handle<Quote> spread = {},
                       const Period& fwdStart = 0 * Days,
                       // exogenous discounting curve
                       Handle<YieldTermStructure> discountingCurve = {},
                       Natural settlementDays = Null<Natural>(),
                       Pillar::Choice pillar = Pillar::LastRelevantDate,
                       Date customPillarDate = Date(),
                       bool endOfMonth = false,
                       const ext::optional<bool>& useIndexedCoupons = ext::nullopt,
                       const ext::optional<BusinessDayConvention>& floatConvention = ext::nullopt);
        SwapRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                       const Date& startDate,
                       const Date& endDate,
                       Calendar calendar,
                       // fixed leg
                       Frequency fixedFrequency,
                       BusinessDayConvention fixedConvention,
                       DayCounter fixedDayCount,
                       // floating leg
                       const ext::shared_ptr<IborIndex>& iborIndex,
                       Handle<Quote> spread = {},
                       // exogenous discounting curve
                       Handle<YieldTermStructure> discountingCurve = {},
                       Pillar::Choice pillar = Pillar::LastRelevantDate,
                       Date customPillarDate = Date(),
                       bool endOfMonth = false,
                       const ext::optional<bool>& useIndexedCoupons = ext::nullopt,
                       const ext::optional<BusinessDayConvention>& floatConvention = ext::nullopt);
        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        void setTermStructure(YieldTermStructure*) override;
        //@}
        //! \name SwapRateHelper inspectors
        //@{
        Spread spread() const;
        // NOLINTNEXTLINE(cppcoreguidelines-noexcept-swap,performance-noexcept-swap)
        ext::shared_ptr<VanillaSwap> swap() const;
        const Period& forwardStart() const;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      protected:
        void initialize(const ext::sha
