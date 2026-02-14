/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Chris Kenyon

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

/*! \file inflationcouponpricer.hpp
 \brief inflation-coupon pricers
 */

#ifndef quantlib_inflation_coupon_pricer_hpp
#define quantlib_inflation_coupon_pricer_hpp

#include <ql/cashflow.hpp>
#include <ql/option.hpp>
#include <ql/cashflows/yoyinflationcoupon.hpp>
#include <ql/termstructures/volatility/inflation/yoyinflationoptionletvolatilitystructure.hpp>

namespace QuantLib {

    //! Base inflation-coupon pricer.
    /*! The main reason we can't use FloatingRateCouponPricer as the
        base is that it takes a FloatingRateCoupon which takes an
        InterestRateIndex and we need an inflation index (these are
        lagged).

        The basic inflation-specific thing that the pricer has to do
        is deal with different lags in the index and the option
        e.g. the option could look 3 months back and the index 2.

        We add the requirement that pricers do inverseCap/Floor-lets.
        These are cap/floor-lets as usually defined, i.e. pay out if
        underlying is above/below a strike.  The non-inverse (usual)
        versions are from a coupon point of view (a capped coupon has
        a maximum at the strike).

        We add the inverse prices so that conventional caps can be
        priced simply.
    */
    class InflationCouponPricer: public virtual Observer,
                                 public virtual Observable {
    public:
      QL_DEPRECATED_DISABLE_WARNING
      InflationCouponPricer() = default;
      ~InflationCouponPricer() override = default;
      QL_DEPRECATED_ENABLE_WARNING
      //! \name Interface
      //@{
      virtual Real swapletPrice() const = 0;
      virtual Rate swapletRate() const = 0;
      virtual Real capletPrice(Rate effectiveCap) const = 0;
      virtual Rate capletRate(Rate effectiveCap) const = 0;
      virtual Real floorletPrice(Rate effectiveFloor) const = 0;
      virtual Rate floorletRate(Rate effectiveFloor) const = 0;
      virtual void initialize(const InflationCoupon&) = 0;
      //@}

      //! \name Observer interface
      //@{
      void update() override { notifyObservers(); }
      //@}
    protected:
      Date paymentDate_;
    };


    void setCouponPricer(const Leg& leg,
                         const ext::shared_ptr<InflationCouponPricer>&);


    //! base pricer for capped/floored YoY inflation coupons
    /*! \note this pricer can already do swaplets but to get
              volatility-dependent coupons you need the descendents.
    */
    class YoYInflationCouponPricer : public InflationCouponPricer {
      public:
        YoYInflationCouponPricer() = default;

        explicit YoYInflationCouponPricer(Handle<YieldTermStructure> nominalTermStructure);

        YoYInflationCouponPricer(Handle<YoYOptionletVolatilitySurface> capletVol,
                                 Handle<YieldTermStructure> nominalTermStructure);

        virtual Handle<YoYOptionletVolatilitySurface> capletVolatility() const{
            return capletVol_;
        }

        virtual Handle<YieldTermStructure> nominalTermStructure() const{
            return nominalTermStructure_;
        }

        virtual void setCapletVolatility(
            const Handle<YoYOptionletVolatilitySurfac
