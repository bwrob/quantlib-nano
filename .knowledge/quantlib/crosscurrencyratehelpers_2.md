xBaseCurrencyLegResettable_;
    };


    //! Rate helper for bootstrapping fixed–vs-floating cross-currency par swaps
    /*!
    This helper represents a par cross-currency swap exchanging a fixed-rate leg
    against a floating-rate leg in a different currency. Since the swap is quoted
    at par, the FX spot cancels out and is not required.

    The collateralOnFixedLeg flag determines which leg is discounted using the provided
    collateral curve, while the other leg’s discount curve is the one being bootstrapped.
    */
    class ConstNotionalCrossCurrencySwapRateHelper : public CrossCurrencySwapRateHelperBase {
      public:
        ConstNotionalCrossCurrencySwapRateHelper(
            const Handle<Quote>& fixedRate,
            const Period& tenor,
            Natural fixingDays,
            const Calendar& calendar,
            BusinessDayConvention convention,
            bool endOfMonth,
            Frequency fixedFrequency,
            DayCounter  fixedDayCount,
            const ext::shared_ptr<IborIndex>& floatIndex,
            const Handle<YieldTermStructure>& collateralCurve,
            bool collateralOnFixedLeg,
            Integer paymentLag = 0);

        Real impliedQuote() const override;
        void accept(AcyclicVisitor&) override;

      protected:
        void initializeDates() override;
        const Handle<YieldTermStructure>& fixedLegDiscountHandle() const;
        const Handle<YieldTermStructure>& floatingLegDiscountHandle() const;

        Frequency fixedFrequency_;
        DayCounter fixedDayCount_;
        ext::shared_ptr<IborIndex> floatIndex_;
        bool collateralOnFixedLeg_;

        Leg fixedLeg_;
        Leg floatLeg_;
    };

}

#endif