
                                         bool endOfMonth,
                                         const ext::shared_ptr<OvernightIndex>& baseIndex,
                                         const ext::shared_ptr<IborIndex>& otherIndex,
                                         Handle<YieldTermStructure> discountHandle = Handle<YieldTermStructure>());

        Real impliedQuote() const override;
        void accept(AcyclicVisitor&) override;
        // NOLINTNEXTLINE(cppcoreguidelines-noexcept-swap,performance-noexcept-swap)
        ext::shared_ptr<Swap> swap() const { return swap_; }
      private:
        void initializeDates() override;
        void setTermStructure(YieldTermStructure*) override;

        Period tenor_;
        Natural settlementDays_;
        Calendar calendar_;
        BusinessDayConvention convention_;
        bool endOfMonth_;
        ext::shared_ptr<OvernightIndex> baseIndex_;
        ext::shared_ptr<IborIndex> otherIndex_;
        Handle<YieldTermStructure> discountHandle_;

        ext::shared_ptr<Swap> swap_;

        RelinkableHandle<YieldTermStructure> termStructureHandle_;
    };

}

#endif