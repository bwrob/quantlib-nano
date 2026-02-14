ible");

        Leg leg; leg.reserve(n);

        // the following is not always correct
        const Calendar& calendar = schedule.calendar();

        if (paymentCalendar.empty()) {
            paymentCalendar = calendar;
        }
        Date refStart, start, refEnd, end;
        Date exCouponDate;
        Date lastPaymentDate = paymentCalendar.advance(schedule.date(n), paymentLag, Days, paymentAdj);

        for (Size i=0; i<n; ++i) {
            refStart = start = schedule.date(i);
            refEnd   =   end = schedule.date(i+1);
            Date paymentDate =
                isZero ? lastPaymentDate : paymentCalendar.advance(end, paymentLag, Days, paymentAdj);
            if (i==0   && (schedule.hasIsRegular() && schedule.hasTenor() && !schedule.isRegular(i+1))) {
                BusinessDayConvention bdc = schedule.businessDayConvention();
                refStart = calendar.adjust(end - schedule.tenor(), bdc);
            }
            if (i==n-1 && (schedule.hasIsRegular() && schedule.hasTenor() && !schedule.isRegular(i+1))) {
                BusinessDayConvention bdc = schedule.businessDayConvention();
                refEnd = calendar.adjust(start + schedule.tenor(), bdc);
            }
            if (exCouponPeriod != Period()) {
                if (exCouponCalendar.empty()) {
                    exCouponCalendar = calendar;
                }
                exCouponDate = exCouponCalendar.advance(paymentDate, -exCouponPeriod,
                                                         exCouponAdjustment, exCouponEndOfMonth);
            }
            if (detail::get(gearings, i, 1.0) == 0.0) { // fixed coupon
                leg.push_back(ext::shared_ptr<CashFlow>(new
                    FixedRateCoupon(paymentDate,
                                    detail::get(nominals, i, 1.0),
                                    detail::effectiveFixedRate(spreads,caps,
                                                               floors,i),
                                    paymentDayCounter,
                                    start, end, refStart, refEnd,
						            exCouponDate)));
            } else { // floating coupon
                if (detail::noOption(caps, floors, i))
                    leg.push_back(ext::shared_ptr<CashFlow>(new
                        FloatingCouponType(
                            paymentDate,
                            detail::get(nominals, i, 1.0),
                            start, end,
                            detail::get(fixingDays, i, index->fixingDays()),
                            index,
                            detail::get(gearings, i, 1.0),
                            detail::get(spreads, i, 0.0),
                            refStart, refEnd,
                            paymentDayCounter, isInArrears, exCouponDate)));
                else {
                    leg.push_back(ext::shared_ptr<CashFlow>(new
                        CappedFlooredCouponType(
                               paymentDate,
                               detail::get(nominals, i, 1.0),
                               start, end,
                               detail::get(fixingDays, i, index->fixingDays()),
                               index,
                               detail::get(gearings, i, 1.0),
                               detail::get(spreads, i, 0.0),
                               detail::get(caps,   i, Null<Rate>()),
                               detail::get(floors, i, Null<Rate>()),
                               refStart, refEnd,
                               paymentDayCounter,
                               isInArrears, exCouponDate)));
                }
            }
        }
        return leg;
    }


    template <typename InterestRateIndexType,
              typename FloatingCouponType,
              typename DigitalCouponType>
    Leg FloatingDigitalLeg(
                        const Schedule& schedule,
                        const std::vector<Real>& nominals,

