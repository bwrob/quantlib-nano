l {

        template <class Spec>
        BlackStyleSwaptionEngine<Spec>::BlackStyleSwaptionEngine(
            Handle<YieldTermStructure> discountCurve,
            Volatility vol,
            const DayCounter& dc,
            Real displacement,
            CashAnnuityModel model)
        : discountCurve_(std::move(discountCurve)),
          vol_(ext::shared_ptr<SwaptionVolatilityStructure>(new ConstantSwaptionVolatility(
              0, NullCalendar(), Following, vol, dc, Spec().type, displacement))),
          model_(model) {
            registerWith(discountCurve_);
        }

        template <class Spec>
        BlackStyleSwaptionEngine<Spec>::BlackStyleSwaptionEngine(
            Handle<YieldTermStructure> discountCurve,
            const Handle<Quote>& vol,
            const DayCounter& dc,
            Real displacement,
            CashAnnuityModel model)
        : discountCurve_(std::move(discountCurve)),
          vol_(ext::shared_ptr<SwaptionVolatilityStructure>(new ConstantSwaptionVolatility(
              0, NullCalendar(), Following, vol, dc, Spec().type, displacement))),
          model_(model) {
            registerWith(discountCurve_);
            registerWith(vol_);
        }

        template <class Spec>
        BlackStyleSwaptionEngine<Spec>::BlackStyleSwaptionEngine(
            Handle<YieldTermStructure> discountCurve,
            Handle<SwaptionVolatilityStructure> volatility,
            CashAnnuityModel model)
        : discountCurve_(std::move(discountCurve)), vol_(std::move(volatility)), model_(model) {
            registerWith(discountCurve_);
            registerWith(vol_);
        }

    template<class Spec>
    void BlackStyleSwaptionEngine<Spec>::calculate() const {
        static const Spread basisPoint = 1.0e-4;

        QL_REQUIRE(arguments_.exercise->type() == Exercise::European,
                   "not a European option");

        Date exerciseDate = arguments_.exercise->date(0);

        // The part of the swap preceding exerciseDate should be truncated to avoid taking into
        // account unwanted cashflows. For the moment we add a check avoiding this situation.
        // Furthermore, we take a copy of the underlying swap. This avoids notifying the swaption
        // when we set a pricing engine on the swap below.
        auto swap = arguments_.swap;

        const Leg& fixedLeg = swap->fixedLeg();
        ext::shared_ptr<FixedRateCoupon> firstCoupon =
            ext::dynamic_pointer_cast<FixedRateCoupon>(fixedLeg[0]);
        QL_REQUIRE(firstCoupon->accrualStartDate() >= exerciseDate,
                   "swap start (" << firstCoupon->accrualStartDate() << ") before exercise date ("
                                  << exerciseDate << ") not supported in Black swaption engine");

        Rate strike = swap->fixedRate();

        // using the discounting curve
        // swap.iborIndex() might be using a different forwarding curve
        auto engine = ext::make_shared<DiscountingSwapEngine>(discountCurve_, false);
        ObservableSettings::instance().disableUpdates();
        swap->setPricingEngine(engine);
        ObservableSettings::instance().enableUpdates();
        Date valuation_date = results_.valuationDate  = swap->valuationDate();
        Rate atmForward = swap->fairRate();

        // Volatilities are quoted for zero-spreaded swaps.
        // Therefore, any spread on the floating leg must be removed
        // with a corresponding correction on the fixed leg.
        Real spread = swap->spread();
        if (spread!=0.0) {
            Spread correction =
                spread * std::fabs(swap->floatingLegBPS() / swap->fixedLegBPS());
            strike -= correction;
            atmForward -= correction;
            results_.additionalResults["spreadCorrection"] = correction;
        } else {
            results_.additionalResults["spreadCorrection"] = Real(0.0);
        }
        results_.additionalResults["strike"] = strike;
        results_.additionalResults["a