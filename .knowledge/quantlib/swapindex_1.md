 fixedLegConvention_;
        bool exogenousDiscount_;
        Handle<YieldTermStructure> discount_;
        // cache data to avoid swap recreation when the same fixing date
        // is used multiple time to forecast changing fixing
        mutable ext::shared_ptr<VanillaSwap> lastSwap_;
        mutable Date lastFixingDate_;
    };


    //! base class for overnight indexed swap indexes
    class OvernightIndexedSwapIndex : public SwapIndex {
      public:
        OvernightIndexedSwapIndex(
                  const std::string& familyName,
                  const Period& tenor,
                  Natural settlementDays,
                  const Currency& currency,
                  const ext::shared_ptr<OvernightIndex>& overnightIndex,
                  bool telescopicValueDates = false,
                  RateAveraging::Type averagingMethod = RateAveraging::Compound);
        //! \name Inspectors
        //@{
        ext::shared_ptr<OvernightIndex> overnightIndex() const;
        /*! \warning Relinking the term structure underlying the index will
                     not have effect on the returned swap.
        */
        ext::shared_ptr<OvernightIndexedSwap> underlyingSwap(
                                                const Date& fixingDate) const;
        //@}
      protected:
        ext::shared_ptr<OvernightIndex> overnightIndex_;
        bool telescopicValueDates_;
        RateAveraging::Type averagingMethod_;
        // cache data to avoid swap recreation when the same fixing date
        // is used multiple time to forecast changing fixing
        mutable ext::shared_ptr<OvernightIndexedSwap> lastSwap_;
        mutable Date lastFixingDate_;
    };

    // inline definitions

    inline BusinessDayConvention SwapIndex::fixedLegConvention() const {
        return fixedLegConvention_;
    }

    inline bool SwapIndex::exogenousDiscount() const {
        return exogenousDiscount_;
    }

    inline ext::shared_ptr<OvernightIndex>
    OvernightIndexedSwapIndex::overnightIndex() const {
        return overnightIndex_;
    }

}

#endif
