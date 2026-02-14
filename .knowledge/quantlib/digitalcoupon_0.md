/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
  Copyright (C) 2007 Cristina Duminuco
  Copyright (C) 2007 Giorgio Facchinetti

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

/*! \file digitalcoupon.hpp
    \brief Floating-rate coupon with digital call/put option
*/

#ifndef quantlib_digital_coupon_hpp
#define quantlib_digital_coupon_hpp

#include <ql/cashflows/floatingratecoupon.hpp>
#include <ql/cashflows/couponpricer.hpp>
#include <ql/cashflows/replication.hpp>
#include <ql/position.hpp>
#include <ql/utilities/null.hpp>

namespace QuantLib {

    //! Digital-payoff coupon
    /*! Implementation of a floating-rate coupon with digital call/put option.
        Payoffs:
        - Coupon with cash-or-nothing Digital Call
          rate + csi * payoffRate * Heaviside(rate-strike)
        - Coupon with cash-or-nothing Digital Put
          rate + csi * payoffRate * Heaviside(strike-rate)
        where csi=+1 or csi=-1.
        - Coupon with asset-or-nothing Digital Call
          rate + csi * rate * Heaviside(rate-strike)
        - Coupon with asset-or-nothing Digital Put
          rate + csi * rate * Heaviside(strike-rate)
        where csi=+1 or csi=-1. If nakedOption is true, the rate in the
        payoffs is set to zero.
        The evaluation of the coupon is made using the call/put spread
        replication method.
    */
    /*! \ingroup instruments

        \test
        - the correctness of the returned value in case of Asset-or-nothing
          embedded option is tested by pricing the digital option with
          Cox-Rubinstein formula.
        - the correctness of the returned value in case of deep-in-the-money
          Asset-or-nothing embedded option is tested vs the expected values of
          coupon and option.
        - the correctness of the returned value in case of deep-out-of-the-money
          Asset-or-nothing embedded option is tested vs the expected values of
          coupon and option.
        - the correctness of the returned value in case of Cash-or-nothing
          embedded option is tested by pricing the digital option with
          Reiner-Rubinstein formula.
        - the correctness of the returned value in case of deep-in-the-money
          Cash-or-nothing embedded option is tested vs the expected values of
          coupon and option.
        - the correctness of the returned value in case of deep-out-of-the-money
          Cash-or-nothing embedded option is tested vs the expected values of
          coupon and option.
        - the correctness of the returned value is tested checking the correctness
          of the call-put parity relation.
        - the correctness of the returned value is tested by the relationship
          between prices in case of different replication types.
    */
    class DigitalCoupon : public FloatingRateCoupon {
      public:
        //! \name Constructors
        //@{
        //! general constructor
        DigitalCoupon(const ext::shared_ptr<FloatingRateCoupon>& underlying,
                      Rate callStrike = Null<Rate>(),
                      Position::Type callPosition = Position::Long,
                      bool isCallITMIncluded = false,
                      Rate callDigitalPayoff = Null<Rate>(),
                      Rate putStrike = Null<Rate>(),
                      Position::Typ