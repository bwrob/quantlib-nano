/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2013 Peter Caspers

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

/*! \file floatfloatswap.hpp
    \brief swap exchanging capped floored Libor or CMS coupons with quite
           general specification. If no payment convention is given, the
           respective leg schedule convention is used. The interest rate
           indices should be linked to valid forwarding and in case of
           swap indices discounting curves
*/

#ifndef quantlib_floatfloat_swap_hpp
#define quantlib_floatfloat_swap_hpp

#include <ql/instruments/swap.hpp>
#include <ql/instruments/vanillaswap.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>
#include <ql/optional.hpp>

namespace QuantLib {

    class InterestRateIndex;

    //! float float swap

    class FloatFloatSwap : public Swap {
      public:
        class arguments;
        class results;
        class engine;
        FloatFloatSwap(
            Swap::Type type,
            Real nominal1,
            Real nominal2,
            Schedule schedule1,
            ext::shared_ptr<InterestRateIndex> index1,
            DayCounter dayCount1,
            Schedule schedule2,
            ext::shared_ptr<InterestRateIndex> index2,
            DayCounter dayCount2,
            bool intermediateCapitalExchange = false,
            bool finalCapitalExchange = false,
            Real gearing1 = 1.0,
            Real spread1 = 0.0,
            Real cappedRate1 = Null<Real>(),
            Real flooredRate1 = Null<Real>(),
            Real gearing2 = 1.0,
            Real spread2 = 0.0,
            Real cappedRate2 = Null<Real>(),
            Real flooredRate2 = Null<Real>(),
            const ext::optional<BusinessDayConvention>& paymentConvention1 = ext::nullopt,
            const ext::optional<BusinessDayConvention>& paymentConvention2 = ext::nullopt);

        FloatFloatSwap(
            Swap::Type type,
            std::vector<Real> nominal1,
            std::vector<Real> nominal2,
            Schedule schedule1,
            ext::shared_ptr<InterestRateIndex> index1,
            DayCounter dayCount1,
            Schedule schedule2,
            ext::shared_ptr<InterestRateIndex> index2,
            DayCounter dayCount2,
            bool intermediateCapitalExchange = false,
            bool finalCapitalExchange = false,
            std::vector<Real> gearing1 = std::vector<Real>(),
            std::vector<Real> spread1 = std::vector<Real>(),
            std::vector<Real> cappedRate1 = std::vector<Real>(),
            std::vector<Real> flooredRate1 = std::vector<Real>(),
            std::vector<Real> gearing2 = std::vector<Real>(),
            std::vector<Real> spread2 = std::vector<Real>(),
            std::vector<Real> cappedRate2 = std::vector<Real>(),
            std::vector<Real> flooredRate2 = std::vector<Real>(),
            const ext::optional<BusinessDayConvention>& paymentConvention1 = ext::nullopt,
            const ext::optional<BusinessDayConvention>& paymentConvention2 = ext::nullopt);

        //! \name Inspectors
        //@{
        Swap::Type type() const;
        const std::vector<Real> &nominal1() const;
        const std::vector<Real> &nominal2() const;

        const Schedule &schedule1() const;
        const Schedule &schedule2() const;

