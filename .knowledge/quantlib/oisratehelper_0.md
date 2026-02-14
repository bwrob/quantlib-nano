/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009, 2012 Roland Lichters
 Copyright (C) 2009, 2012 Ferdinando Ametrano

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

/*! \file oisratehelper.hpp
    \brief Overnight Indexed Swap (aka OIS) rate helpers
*/

#ifndef quantlib_oisratehelper_hpp
#define quantlib_oisratehelper_hpp

#include <ql/termstructures/yield/ratehelpers.hpp>
#include <ql/instruments/overnightindexedswap.hpp>
#include <ql/optional.hpp>
#include <variant>

namespace QuantLib {

    class FloatingRateCouponPricer;

    //! Rate helper for bootstrapping over Overnight Indexed Swap rates
    class OISRateHelper : public RelativeDateRateHelper {
      public:
        OISRateHelper(
          Natural settlementDays,
          const Period& tenor, // swap maturity
          const std::variant<Rate, Handle<Quote>>& fixedRate,
          const ext::shared_ptr<OvernightIndex>& overnightIndex,
          // exogenous discounting curve
          Handle<YieldTermStructure> discountingCurve = {},
          bool telescopicValueDates = false,
          Integer paymentLag = 0,
          BusinessDayConvention paymentConvention = Following,
          Frequency paymentFrequency = Annual,
          Calendar paymentCalendar = Calendar(),
          const Period& forwardStart = 0 * Days,
          const std::variant<Spread, Handle<Quote>>& overnightSpread = Spread(0.0),
          Pillar::Choice pillar = Pillar::LastRelevantDate,
          Date customPillarDate = Date(),
          RateAveraging::Type averagingMethod = RateAveraging::Compound,
          ext::optional<bool> endOfMonth = ext::nullopt,
          ext::optional<Frequency> fixedPaymentFrequency = ext::nullopt,
          Calendar fixedCalendar = Calendar(),
          Natural lookbackDays = Null<Natural>(),
          Natural lockoutDays = 0,
          bool applyObservationShift = false,
          ext::shared_ptr<FloatingRateCouponPricer> pricer = {},
          DateGeneration::Rule rule = DateGeneration::Backward,
          Calendar overnightCalendar = Calendar(),
          BusinessDayConvention convention = ModifiedFollowing);

        OISRateHelper(
          const Date& startDate,
          const Date& endDate,
          const std::variant<Rate, Handle<Quote>>& fixedRate,
          const ext::shared_ptr<OvernightIndex>& overnightIndex,
          // exogenous discounting curve
          Handle<YieldTermStructure> discountingCurve = {},
          bool telescopicValueDates = false,
          Integer paymentLag = 0,
          BusinessDayConvention paymentConvention = Following,
          Frequency paymentFrequency = Annual,
          Calendar paymentCalendar = Calendar(),
          const std::variant<Spread, Handle<Quote>>& overnightSpread = Spread(0.0),
          Pillar::Choice pillar = Pillar::LastRelevantDate,
          Date customPillarDate = Date(),
          RateAveraging::Type averagingMethod = RateAveraging::Compound,
          ext::optional<bool> endOfMonth = ext::nullopt,
          ext::optional<Frequency> fixedPaymentFrequency = ext::nullopt,
          Calendar fixedCalendar = Calendar(),
          Natural lookbackDays = Null<Natural>(),
          Natural lockoutDays = 0,
          bool applyObservationShift = false,
          ext::shared_ptr<FloatingRateCouponPricer> pricer = {},
          D