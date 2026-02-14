angeRate::Direct);
            if (fromCurrency != exchRate.source())
                return (Real)1 / exchRate.rate();
            return exchRate.rate();
        }
        return 1;
    }

    inline Real CommodityPricingHelper::calculateUnitCost(
                                       const CommodityType& commodityType,
                                       const CommodityUnitCost& unitCost,
                                       const Currency& baseCurrency,
                                       const UnitOfMeasure& baseUnitOfMeasure,
                                       const Date& evaluationDate) {
        if (unitCost.amount().value() != 0) {
            Real unitCostUomConversionFactor =
                calculateUomConversionFactor(commodityType,
                                             unitCost.unitOfMeasure(),
                                             baseUnitOfMeasure);
            Real unitCostFxConversionFactor =
                calculateFxConversionFactor(unitCost.amount().currency(),
                                            baseCurrency, evaluationDate);
            return unitCost.amount().value() * unitCostUomConversionFactor
                 * unitCostFxConversionFactor;
        }
        return 0;
    }

}

#endif