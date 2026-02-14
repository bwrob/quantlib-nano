/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Ferdinando Ametrano
 Copyright (C) 2001, 2002, 2003 Sadruddin Rejeb
 Copyright (C) 2006 StatPro Italia srl
 Copyright (C) 2015, 2016, 2017 Peter Caspers
 Copyright (C) 2017 Paul Giltinan
 Copyright (C) 2017 Werner Kuerzinger
 Copyright (C) 2020 Marcin Rybacki

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

/*! \file blackswaptionengine.hpp
    \brief Black-formula swaption engine
*/

#ifndef quantlib_pricers_black_swaption_hpp
#define quantlib_pricers_black_swaption_hpp

#include <ql/cashflows/cashflows.hpp>
#include <ql/cashflows/fixedratecoupon.hpp>
#include <ql/exercise.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/instruments/swaption.hpp>
#include <ql/pricingengines/blackformula.hpp>
#include <ql/pricingengines/swap/discountingswapengine.hpp>
#include <ql/termstructures/volatility/swaption/swaptionconstantvol.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/time/calendars/nullcalendar.hpp>
#include <utility>

namespace QuantLib {

    class Quote;

    namespace detail {

    /*! Generic Black-style-formula swaption engine
        This is the base class for the Black and Bachelier swaption engines */
    template<class Spec>
    class BlackStyleSwaptionEngine : public Swaption::engine {
      public:
        enum CashAnnuityModel { SwapRate, DiscountCurve };
        BlackStyleSwaptionEngine(Handle<YieldTermStructure> discountCurve,
                                 Volatility vol,
                                 const DayCounter& dc = Actual365Fixed(),
                                 Real displacement = 0.0,
                                 CashAnnuityModel model = DiscountCurve);
        BlackStyleSwaptionEngine(Handle<YieldTermStructure> discountCurve,
                                 const Handle<Quote>& vol,
                                 const DayCounter& dc = Actual365Fixed(),
                                 Real displacement = 0.0,
                                 CashAnnuityModel model = DiscountCurve);
        BlackStyleSwaptionEngine(Handle<YieldTermStructure> discountCurve,
                                 Handle<SwaptionVolatilityStructure> vol,
                                 CashAnnuityModel model = DiscountCurve);
        void calculate() const override;
        Handle<YieldTermStructure> termStructure() { return discountCurve_; }
        Handle<SwaptionVolatilityStructure> volatility() { return vol_; }

      private:
        Handle<YieldTermStructure> discountCurve_;
        Handle<SwaptionVolatilityStructure> vol_;
        CashAnnuityModel model_;
    };

    // shifted lognormal type engine
    struct Black76Spec {
        static constexpr VolatilityType type = ShiftedLognormal;
        Real value(const Option::Type type, const Real strike,
                   const Real atmForward, const Real stdDev, const Real annuity,
                   const Real displacement) {
            return blackFormula(type, strike, atmForward, stdDev, annuity,
                                displacement);
        }
        Real vega(const Real strike, const Real atmForward, const Real stdDev,
                  const Real exerciseTime, const Real annuity,
                  const Real displacement) {
            return std::sqrt(exerciseTime)