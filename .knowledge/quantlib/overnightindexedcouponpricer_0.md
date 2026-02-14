/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Roland Lichters
 Copyright (C) 2009 Ferdinando Ametrano
 Copyright (C) 2014 Peter Caspers
 Copyright (C) 2016 Stefano Fondi
 Copyright (C) 2017 Joseph Jeisman
 Copyright (C) 2017 Fabrice Lecuyer

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

/*! \file overnightindexedcouponpricer.hpp
    \brief contains the pricer for an OvernightIndexedCoupon
*/

#ifndef quantlib_overnight_indexed_coupon_pricer_hpp
#define quantlib_overnight_indexed_coupon_pricer_hpp

#include <ql/cashflows/couponpricer.hpp>
#include <ql/cashflows/floatingratecoupon.hpp>
#include <ql/cashflows/overnightindexedcoupon.hpp>
#include <utility>

namespace QuantLib {

    class OptionletVolatilityStructure;

    //! Base pricer for overnight-indexed floating coupons
    /*! This is the base pricer class for coupons indexed to an overnight rate.
        It defines the common pricing interface and provides the foundation for
        more specialized overnight coupon pricers (e.g., compounded, averaged,
        capped/floored variants).

        Derived classes should implement the specific logic for computing the
        rate and optional adjustments, depending on the compounding or
        averaging convention used.
    */
    class OvernightIndexedCouponPricer : public FloatingRateCouponPricer {
      using FloatingRateCouponPricer::capletRate;
      using FloatingRateCouponPricer::floorletRate;
      public:

        explicit OvernightIndexedCouponPricer(
          Handle<OptionletVolatilityStructure> v = Handle<OptionletVolatilityStructure>(),
          bool effectiveVolatilityInput = false);

        void initialize(const FloatingRateCoupon& coupon) override;

        void setCapletVolatility(
                            const Handle<OptionletVolatilityStructure>& v =
                                    Handle<OptionletVolatilityStructure>()) {
            unregisterWith(capletVol_);
            capletVol_ = v;
            registerWith(capletVol_);
            update();
        }

        /*! \brief Returns the handle to the optionlet volatility structure used for caplets/floorlets */
        Handle<OptionletVolatilityStructure> capletVolatility() const {
            return capletVol_;
        }

        void setEffectiveVolatilityInput(const bool effectiveVolatilityInput) {
            effectiveVolatilityInput_ = effectiveVolatilityInput;
        }

        /*! \brief Returns true if the volatility input is interpreted as effective volatility */
        bool effectiveVolatilityInput() const;
        /*! \brief Returns the effective caplet volatility used in the last capletRate() calculation.
            \note Only available after capletRate() was called.
        */
        virtual Real effectiveCapletVolatility() const;
        /*! \brief Returns the effective floorlet volatility used in the last floorletRate() calculation.
            \note Only available after floorletRate() was called.
        */
        virtual Real effectiveFloorletVolatility() const;

        virtual Rate capletRate(Rate effectiveCap, bool dailyCapFloor) const = 0;
        virtual Rate floorletRate(Rate effectiveCap, bool dailyCapFloor) const = 0;
        virtual Rate averageRate(const Date& date) const = 0;

      protected:
        const Overn
