         : section_(section), targetPrice_(targetPrice), type_(type) {}
            Real operator()(Real strike) const {
                return section_->optionPrice(strike, type_) - targetPrice_;
            };
            const SmileSection *section_;
            const Real targetPrice_;
            const Option::Type type_;
        };

        void initialize(const FloatingRateCoupon& coupon) override;
        Real optionletPrice(Option::Type optionType, Real strike) const;
        Real strikeFromVegaRatio(Real ratio, Option::Type optionType,
                                 Real referenceStrike) const;
        Real strikeFromPrice(Real price, Option::Type optionType,
                             Real referenceStrike) const;

        Handle<Quote> meanReversion_;

        Handle<YieldTermStructure> forwardCurve_, discountCurve_;
        Handle<YieldTermStructure> couponDiscountCurve_;

        const CmsCoupon *coupon_;

        Date today_, paymentDate_, fixingDate_;

        Real gearing_, spread_;

        Period swapTenor_;
        Real spreadLegValue_, swapRateValue_, couponDiscountRatio_, discountCurvePaymentDiscount_,
            annuity_;

        ext::shared_ptr<SwapIndex> swapIndex_;
        ext::shared_ptr<FixedVsFloatingSwap> swap_;
        ext::shared_ptr<SmileSection> smileSection_;

        Settings settings_;
        DayCounter volDayCounter_;
        ext::shared_ptr<Integrator> integrator_;

        Real adjustedLowerBound_, adjustedUpperBound_;
    };
}

#endif