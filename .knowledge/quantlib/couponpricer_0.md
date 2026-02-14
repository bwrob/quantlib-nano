/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Giorgio Facchinetti
 Copyright (C) 2007 Cristina Duminuco
 Copyright (C) 2011 Ferdinando Ametrano
 Copyright (C) 2015 Peter Caspers

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

/*! \file couponpricer.hpp
    \brief Coupon pricers
*/

#ifndef quantlib_coupon_pricer_hpp
#define quantlib_coupon_pricer_hpp

#include <ql/cashflow.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/option.hpp>
#include <ql/optional.hpp>
#include <ql/quotes/simplequote.hpp>
#include <ql/termstructures/volatility/optionlet/optionletvolatilitystructure.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <utility>

namespace QuantLib {

    class FloatingRateCoupon;
    class IborCoupon;

    //! generic pricer for floating-rate coupons
    class FloatingRateCouponPricer: public virtual Observer,
                                    public virtual Observable {
      public:
        ~FloatingRateCouponPricer() override = default;
        //! \name required interface
        //@{
        virtual Real swapletPrice() const = 0;
        virtual Rate swapletRate() const = 0;
        virtual Real capletPrice(Rate effectiveCap) const = 0;
        virtual Rate capletRate(Rate effectiveCap) const = 0;
        virtual Real floorletPrice(Rate effectiveFloor) const = 0;
        virtual Rate floorletRate(Rate effectiveFloor) const = 0;
        virtual void initialize(const FloatingRateCoupon& coupon) = 0;
        //@}
        //! \name Observer interface
        //@{
        void update() override { notifyObservers(); }
        //@}
    };

    //! base pricer for capped/floored Ibor coupons
    class IborCouponPricer : public FloatingRateCouponPricer {
      public:
        explicit IborCouponPricer(
            Handle<OptionletVolatilityStructure> v = Handle<OptionletVolatilityStructure>(),
            ext::optional<bool> useIndexedCoupon = ext::nullopt);

        bool useIndexedCoupon() const { return useIndexedCoupon_; }

        Handle<OptionletVolatilityStructure> capletVolatility() const {
            return capletVol_;
        }
        void setCapletVolatility(
                            const Handle<OptionletVolatilityStructure>& v =
                                    Handle<OptionletVolatilityStructure>()) {
            unregisterWith(capletVol_);
            capletVol_ = v;
            registerWith(capletVol_);
            update();
        }
        void initialize(const FloatingRateCoupon& coupon) override;

        void initializeCachedData(const IborCoupon& coupon) const;

      protected:

        const IborCoupon* coupon_;

        ext::shared_ptr<IborIndex> index_;
        Date fixingDate_;
        Real gearing_;
        Spread spread_;
        Time accrualPeriod_;

        Date fixingValueDate_, fixingEndDate_, fixingMaturityDate_;
        Time spanningTime_, spanningTimeIndexMaturity_;

        Handle<OptionletVolatilityStructure> capletVol_;
        bool useIndexedCoupon_;
    };

    /*! Black-formula pricer for capped/floored Ibor coupons
        References for timing adjustments
        Black76             Hull, Options, Futures and other
                            derivatives, 4th ed., page 550
        BivariateLognormal  http://ssrn.com/abstract=2170721 */
    class Bla