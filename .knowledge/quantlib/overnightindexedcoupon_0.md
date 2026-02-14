/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Roland Lichters
 Copyright (C) 2009 Ferdinando Ametrano
 Copyright (C) 2014 Peter Caspers
 Copyright (C) 2017 Joseph Jeisman
 Copyright (C) 2017 Fabrice Lecuyer
 Copyright (C) 2025 Paolo D'Elia

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it
 under the terms of the QuantLib license.  You should have received a
 copy of the license along with this program; if not, please email
 <quantlib-dev@lists.sf.net>. The license is also available online at
 <https://www.quantlib.org/license.shtml>.

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
*/

/*! \file overnightindexedcoupon.hpp
    \brief coupon paying the compounded daily overnight rate
*/

#ifndef quantlib_overnight_indexed_coupon_hpp
#define quantlib_overnight_indexed_coupon_hpp

#include <ql/cashflows/couponpricer.hpp>
#include <ql/cashflows/floatingratecoupon.hpp>
#include <ql/cashflows/rateaveraging.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/time/schedule.hpp>


namespace QuantLib {

    class OvernightIndexedCouponPricer;
    class CompoundingOvernightIndexedCouponPricer;

    //! overnight coupon
    /*! %Coupon paying the interest, depending on the averaging convention,
        due to daily overnight fixings.

        \warning telescopicValueDates optimizes the schedule for calculation speed,
        but might fail to produce correct results if the coupon ages by more than
        a grace period of 7 days. It is therefore recommended not to set this flag
        to true unless you know exactly what you are doing. The intended use is
        rather by the OISRateHelper which is safe, since it reinitialises the
        instrument each time the evaluation date changes.
    */
    class OvernightIndexedCoupon : public FloatingRateCoupon {
      public:
        OvernightIndexedCoupon(
                    const Date& paymentDate,
                    Real nominal,
                    const Date& startDate,
                    const Date& endDate,
                    const ext::shared_ptr<OvernightIndex>& overnightIndex,
                    Real gearing = 1.0,
                    Spread spread = 0.0,
                    const Date& refPeriodStart = Date(),
                    const Date& refPeriodEnd = Date(),
                    const DayCounter& dayCounter = DayCounter(),
                    bool telescopicValueDates = false,
                    RateAveraging::Type averagingMethod = RateAveraging::Compound,
                    Natural lookbackDays = Null<Natural>(),
                    Natural lockoutDays = 0,
                    bool applyObservationShift = false,
                    bool compoundSpread = false,
                    const Date& rateComputationStartDate = Date(),
                    const Date& rateComputationEndDate = Date());
        //! \name Inspectors
        //@{
        //! fixing dates for the rates to be compounded
        const std::vector<Date>& fixingDates() const { return fixingDates_; }
        //! accrual (compounding) periods
        const std::vector<Time>& dt() const { return dt_; }
        //! fixings to be compounded
        const std::vector<Rate>& indexFixings() const;
        //! value dates for the rates to be compounded
        const std::vector<Date>& valueDates() const { return valueDates_; }
        //! interest dates for the rates to be compounded
        const std::vector<Date>& interestDates() const { return interestDates_; }
        //! averaging method
        RateAveraging::Type averagingMethod() const { return averagingMethod_; }
        //! lockout days
        Natural lockoutDays() 