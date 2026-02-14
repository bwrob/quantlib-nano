                  const CommodityUnitCost& unitCost,
                               const Date& evaluationDate) const;
        void calculateSecondaryCostAmounts(const CommodityType& commodityType,
                                           Real totalQuantityValue,
                                           const Date& evaluationDate) const;

        CommodityType commodityType_;
    };


    class EnergyCommodity::arguments : public virtual PricingEngine::arguments {
      public:
        Currency currency;
        UnitOfMeasure unitOfMeasure;
        void validate() const override {}
    };

    class EnergyCommodity::results : public Instrument::results {
      public:
        Real NPV;
        Currency currency;
        UnitOfMeasure unitOfMeasure;
        void reset() override { Instrument::results::reset(); }
    };

    class EnergyCommodity::engine
        : public GenericEngine<EnergyCommodity::arguments,
                               EnergyCommodity::results> {};

}

#endif