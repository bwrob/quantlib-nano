sDayConvention convention,
                          bool endOfMonth,
                          const DayCounter& dayCounter);
        DepositRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                          const ext::shared_ptr<IborIndex>& iborIndex);
        DepositRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                          Date fixingDate,
                          const ext::shared_ptr<IborIndex>& iborIndex);
        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        void setTermStructure(YieldTermStructure*) override;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      private:
        void initializeDates() override;
        Date fixingDate_;
        ext::shared_ptr<IborIndex> iborIndex_;
        RelinkableHandle<YieldTermStructure> termStructureHandle_;
    };


    //! Rate helper for bootstrapping over %FRA rates
    class FraRateHelper : public RelativeDateRateHelper {
      public:
        FraRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                      Natural monthsToStart,
                      Natural monthsToEnd,
                      Natural fixingDays,
                      const Calendar& calendar,
                      BusinessDayConvention convention,
                      bool endOfMonth,
                      const DayCounter& dayCounter,
                      Pillar::Choice pillar = Pillar::LastRelevantDate,
                      Date customPillarDate = Date(),
                      bool useIndexedCoupon = true);
        FraRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                      Natural monthsToStart,
                      const ext::shared_ptr<IborIndex>& iborIndex,
                      Pillar::Choice pillar = Pillar::LastRelevantDate,
                      Date customPillarDate = Date(),
                      bool useIndexedCoupon = true);
        FraRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                      Period periodToStart,
                      Natural lengthInMonths,
                      Natural fixingDays,
                      const Calendar& calendar,
                      BusinessDayConvention convention,
                      bool endOfMonth,
                      const DayCounter& dayCounter,
                      Pillar::Choice pillar = Pillar::LastRelevantDate,
                      Date customPillarDate = Date(),
                      bool useIndexedCoupon = true);
        FraRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                      Period periodToStart,
                      const ext::shared_ptr<IborIndex>& iborIndex,
                      Pillar::Choice pillar = Pillar::LastRelevantDate,
                      Date customPillarDate = Date(),
                      bool useIndexedCoupon = true);
        FraRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                      Natural immOffsetStart,
                      Natural immOffsetEnd,
                      const ext::shared_ptr<IborIndex>& iborIndex,
                      Pillar::Choice pillar = Pillar::LastRelevantDate,
                      Date customPillarDate = Date(),
                      bool useIndexedCoupon = true);
        FraRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                      Date startDate,
                      Date endDate,
                      const ext::shared_ptr<IborIndex>& iborIndex,
                      Pillar::Choice pillar = Pillar::LastRelevantDate,
                      Date customPillarDate = Date(),
                      bool useIndexedCoupon = true);
        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        void setTermStructure(YieldTermStructure*) override;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
