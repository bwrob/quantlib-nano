tmForward"] = atmForward;

        Real annuity;
        if (arguments_.settlementType == Settlement::Physical ||
            (arguments_.settlementType == Settlement::Cash &&
             arguments_.settlementMethod ==
                 Settlement::CollateralizedCashPrice)) {
            annuity = std::fabs(swap->fixedLegBPS()) / basisPoint;
        } else if (arguments_.settlementType == Settlement::Cash &&
                   arguments_.settlementMethod == Settlement::ParYieldCurve) {
            DayCounter dayCount = firstCoupon->dayCounter();
            // we assume that the cash settlement date is equal
            // to the swap start date
            Date discountDate = model_ == DiscountCurve
                                    ? firstCoupon->accrualStartDate()
                                    : valuation_date;
            Frequency freq = Annual;
            const Schedule& fixedSchedule = swap->fixedSchedule();
            if (fixedSchedule.hasTenor()) {
                freq = fixedSchedule.tenor().frequency();
            }
            Real fixedLegCashBPS =
                CashFlows::bps(fixedLeg,
                        InterestRate(atmForward, dayCount, Compounded, freq),
                        false, discountDate);
            annuity = std::fabs(fixedLegCashBPS / basisPoint) *
                      discountCurve_->discount(discountDate);
        } else {
            QL_FAIL("invalid (settlementType, settlementMethod) pair");
        }
        results_.additionalResults["annuity"] = annuity;

        const Schedule& floatingSchedule = swap->floatingSchedule();
        Time swapLength =  vol_->swapLength(floatingSchedule.dates().front(),
                                            floatingSchedule.dates().back());

        // swapLength is rounded to whole months. To ensure we can read a variance
        // and a shift from vol_ we floor swapLength at 1/12 here therefore.
        swapLength = std::max(swapLength, 1.0 / 12.0);
        results_.additionalResults["swapLength"] = swapLength;

        Real variance = vol_->blackVariance(exerciseDate, swapLength, strike);

        Real displacement =
            vol_->volatilityType() == ShiftedLognormal ?
            vol_->shift(exerciseDate, swapLength) : 0.0;

        Real stdDev = std::sqrt(variance);
        results_.additionalResults["stdDev"] = stdDev;
        Option::Type w = (swap->type() == Swap::Payer) ? Option::Call : Option::Put;
        results_.value = Spec().value(w, strike, atmForward, stdDev, annuity, displacement);

        Time exerciseTime = vol_->timeFromReference(exerciseDate);
        results_.additionalResults["vega"] = Spec().vega(
            strike, atmForward, stdDev, exerciseTime, annuity, displacement);
        results_.additionalResults["delta"] = Spec().delta(
            w, strike, atmForward, stdDev, annuity, displacement);
        results_.additionalResults["timeToExpiry"] = exerciseTime;
        results_.additionalResults["impliedVolatility"] = Real(stdDev / std::sqrt(exerciseTime));
        results_.additionalResults["forwardPrice"] = Real(results_.value / discountCurve_->discount(exerciseDate));
    }

    }  // namespace detail

}

#endif
