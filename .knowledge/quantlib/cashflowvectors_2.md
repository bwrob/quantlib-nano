                  const ext::shared_ptr<InterestRateIndexType>& index,
                        const DayCounter& paymentDayCounter,
                        BusinessDayConvention paymentAdj,
                        const std::vector<Natural>& fixingDays,
                        const std::vector<Real>& gearings,
                        const std::vector<Spread>& spreads,
                        bool isInArrears,
                        const std::vector<Rate>& callStrikes,
                        Position::Type callPosition,
                        bool isCallATMIncluded,
                        const std::vector<Rate>& callDigitalPayoffs,
                        const std::vector<Rate>& putStrikes,
                        Position::Type putPosition,
                        bool isPutATMIncluded,
                        const std::vector<Rate>& putDigitalPayoffs,
                        const ext::shared_ptr<DigitalReplication>& replication,
                        bool nakedOption = false) {
        Size n = schedule.size()-1;
        QL_REQUIRE(!nominals.empty(), "no notional given");
        QL_REQUIRE(nominals.size() <= n,
                   "too many nominals (" << nominals.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(gearings.size()<=n,
                   "too many gearings (" << gearings.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(spreads.size()<=n,
                   "too many spreads (" << spreads.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(callStrikes.size()<=n,
                   "too many call rates (" << callStrikes.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(putStrikes.size()<=n,
                   "too many put rates (" << putStrikes.size() <<
                   "), only " << n << " required");

        Leg leg; leg.reserve(n);

        // the following is not always correct
        const Calendar& calendar = schedule.calendar();

        Date refStart, start, refEnd, end;
        Date paymentDate;

        for (Size i=0; i<n; ++i) {
            refStart = start = schedule.date(i);
            refEnd   =   end = schedule.date(i+1);
            paymentDate = calendar.adjust(end, paymentAdj);
            if (i==0 && (schedule.hasIsRegular() && schedule.hasTenor() && !schedule.isRegular(i+1))) {
                BusinessDayConvention bdc = schedule.businessDayConvention();
                refStart = calendar.adjust(end - schedule.tenor(), bdc);
            }
            if (i==n-1 && (schedule.hasIsRegular() && schedule.hasTenor() && !schedule.isRegular(i+1))) {
                BusinessDayConvention bdc = schedule.businessDayConvention();
                refEnd = calendar.adjust(start + schedule.tenor(), bdc);
            }
            if (detail::get(gearings, i, 1.0) == 0.0) { // fixed coupon
                leg.push_back(ext::shared_ptr<CashFlow>(new
                    FixedRateCoupon(paymentDate,
                                    detail::get(nominals, i, 1.0),
                                    detail::get(spreads, i, 1.0),
                                    paymentDayCounter,
                                    start, end, refStart, refEnd)));
            } else { // floating digital coupon
                ext::shared_ptr<FloatingCouponType> underlying(new
                    FloatingCouponType(paymentDate,
                                       detail::get(nominals, i, 1.0),
                                       start, end,
                                       detail::get(fixingDays, i, index->fixingDays()),
                                       index,
                                       detail::get(gearings, i, 1.0),
                                       detail::get(spreads, i, 0.0),
                                       refStart, refEnd,
                                       paymentDayCounter, isInArrears));
                leg.push_back(ext::shared_