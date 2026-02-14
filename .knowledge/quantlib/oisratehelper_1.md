ateGeneration::Rule rule = DateGeneration::Backward,
          Calendar overnightCalendar = Calendar(),
          BusinessDayConvention convention = ModifiedFollowing);

        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        void setTermStructure(YieldTermStructure*) override;
        //@}
        //! \name inspectors
        //@{
        // NOLINTNEXTLINE(cppcoreguidelines-noexcept-swap,performance-noexcept-swap)
        ext::shared_ptr<OvernightIndexedSwap> swap() const { return swap_; }
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      protected:
        void initialize(const ext::shared_ptr<OvernightIndex>& overnightIndex,
                        Date customPillarDate);
        void initializeDates() override;

        Natural settlementDays_;
        Period tenor_;
        Date startDate_, endDate_;
        ext::shared_ptr<OvernightIndex> overnightIndex_;

        ext::shared_ptr<OvernightIndexedSwap> swap_;
        RelinkableHandle<YieldTermStructure> termStructureHandle_;

        Handle<YieldTermStructure> discountHandle_;
        bool telescopicValueDates_;
        RelinkableHandle<YieldTermStructure> discountRelinkableHandle_;

        Integer paymentLag_;
        BusinessDayConvention paymentConvention_;
        Frequency paymentFrequency_;
        Calendar paymentCalendar_;
        Period forwardStart_;
        Handle<Quote> overnightSpread_;
        Pillar::Choice pillarChoice_;
        RateAveraging::Type averagingMethod_;
        ext::optional<bool> endOfMonth_;
        ext::optional<Frequency> fixedPaymentFrequency_;
        Calendar fixedCalendar_;
        Calendar overnightCalendar_;
        BusinessDayConvention convention_;
        Natural lookbackDays_;
        Natural lockoutDays_;
        bool applyObservationShift_;
        ext::shared_ptr<FloatingRateCouponPricer> pricer_;
        DateGeneration::Rule rule_ = DateGeneration::Backward;

    };

}

#endif
