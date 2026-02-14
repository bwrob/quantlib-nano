/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2011 Chris Kenyon
 Copyright (C) 2022 Quaternion Risk Management Ltd

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

/*! \file cpicoupon.hpp
    \brief Coupon paying a zero-inflation index
*/

#ifndef quantlib_cpicoupon_hpp
#define quantlib_cpicoupon_hpp

#include <ql/cashflows/inflationcoupon.hpp>
#include <ql/cashflows/indexedcashflow.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <ql/time/schedule.hpp>

namespace QuantLib {


    class CPICouponPricer;

    //! %Coupon paying the performance of a CPI (zero inflation) index
    /*! The performance is relative to the index value on the base date.

        The other inflation value is taken from the refPeriodEnd date
        with observation lag, so any roll/calendar etc. will be built
        in by the caller.  By default this is done in the
        InflationCoupon which uses ModifiedPreceding with fixing days
        assumed positive meaning earlier, i.e. always stay in same
        month (relative to referencePeriodEnd).

        This is more sophisticated than an %IndexedCashFlow because it
        does date calculations itself.

        \todo we do not do any convexity adjustment for lags different
              to the natural ZCIIS lag that was used to create the
              forward inflation curve.
    */
    class CPICoupon : public InflationCoupon {
      public:
        //! \name Constructors
        //@{
        /*! This constructor takes the base CPI to be used in the calculations. */
        CPICoupon(Real baseCPI,
                  const Date& paymentDate,
                  Real nominal,
                  const Date& startDate,
                  const Date& endDate,
                  const ext::shared_ptr<ZeroInflationIndex>& index,
                  const Period& observationLag,
                  CPI::InterpolationType observationInterpolation,
                  const DayCounter& dayCounter,
                  Real fixedRate,
                  const Date& refPeriodStart = Date(),
                  const Date& refPeriodEnd = Date(),
                  const Date& exCouponDate = Date());

        /*! This constructor takes a base date; the coupon will use it
            to retrieve the base CPI to be used in the calculations.
        */
        CPICoupon(const Date& baseDate,
                  const Date& paymentDate,
                  Real nominal,
                  const Date& startDate,
                  const Date& endDate,
                  const ext::shared_ptr<ZeroInflationIndex>& index,
                  const Period& observationLag,
                  CPI::InterpolationType observationInterpolation,
                  const DayCounter& dayCounter,
                  Real fixedRate,
                  const Date& refPeriodStart = Date(),
                  const Date& refPeriodEnd = Date(),
                  const Date& exCouponDate = Date());

        /*! This constructor takes both a base CPI and a base date.
            If both are passed, the base CPI is used in the calculations.
        */
        CPICoupon(Real baseCPI,
                  const Date& baseDate,
                  const Date& paymentDate,
                  Real nominal,
                  const Date& startDate,
                  const Date& endDate,

