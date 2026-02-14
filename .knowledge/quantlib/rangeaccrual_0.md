/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*

 Copyright (C) 2006, 2007 Giorgio Facchinetti
 Copyright (C) 2006, 2007 Mario Pucci

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

/*! \file rangeaccrual.hpp
    \brief range-accrual coupon
*/

#ifndef quantlib_range_accrual_h
#define quantlib_range_accrual_h

#include <ql/termstructures/volatility/smilesection.hpp>
#include <ql/cashflows/couponpricer.hpp>
#include <ql/cashflows/floatingratecoupon.hpp>
#include <ql/time/schedule.hpp>
#include <vector>

namespace QuantLib {

    class IborIndex;

    class RangeAccrualFloatersCoupon : public FloatingRateCoupon {

      public:
        RangeAccrualFloatersCoupon(const Date& paymentDate,
                                   Real nominal,
                                   const ext::shared_ptr<IborIndex>& index,
                                   const Date& startDate,
                                   const Date& endDate,
                                   Natural fixingDays,
                                   const DayCounter& dayCounter,
                                   Real gearing,
                                   Rate spread,
                                   const Date& refPeriodStart,
                                   const Date& refPeriodEnd,
                                   Schedule observationsSchedule,
                                   Real lowerTrigger,
                                   Real upperTrigger);

        /*! \deprecated Use the overload taking a Schedule instead.
                        Deprecated in version 1.40.
        */
        [[deprecated("Use the overload taking a Schedule instead")]]
        RangeAccrualFloatersCoupon(const Date& paymentDate,
                                   Real nominal,
                                   const ext::shared_ptr<IborIndex>& index,
                                   const Date& startDate,
                                   const Date& endDate,
                                   Natural fixingDays,
                                   const DayCounter& dayCounter,
                                   Real gearing,
                                   Rate spread,
                                   const Date& refPeriodStart,
                                   const Date& refPeriodEnd,
                                   const ext::shared_ptr<Schedule>& observationsSchedule,
                                   Real lowerTrigger,
                                   Real upperTrigger)
        : RangeAccrualFloatersCoupon(paymentDate, nominal, index, startDate, endDate,
                                     fixingDays, dayCounter, gearing, spread,
                                     refPeriodStart, refPeriodEnd,
                                     *observationsSchedule,
                                     lowerTrigger, upperTrigger) {}

        Real startTime() const {return startTime_; }
        Real endTime() const {return endTime_; }
        Real lowerTrigger() const {return lowerTrigger_; }
        Real upperTrigger() const {return upperTrigger_; }
        Size observationsNo() const {return observationsNo_; }
        const std::vector<Date>& observationDates() const {
            return observationDates_;
        }
        const std::vector<Real>& observationTimes() const {
            return observat