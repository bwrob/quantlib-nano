/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004 StatPro Italia srl
 Copyright (C) 2006, 2007 Cristina Duminuco
 Copyright (C) 2006, 2007 Giorgio Facchinetti
 Copyright (C) 2006 Mario Pucci
 Copyright (C) 2007 Ferdinando Ametrano
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

/*! \file cashflowvectors.hpp
    \brief Cash flow vector builders
*/

#ifndef quantlib_cash_flow_vectors_hpp
#define quantlib_cash_flow_vectors_hpp

#include <ql/cashflows/fixedratecoupon.hpp>
#include <ql/cashflows/replication.hpp>
#include <ql/time/schedule.hpp>
#include <ql/utilities/null.hpp>
#include <ql/utilities/vectors.hpp>
#include <ql/position.hpp>
#include <ql/indexes/swapindex.hpp>

namespace QuantLib {

    namespace detail {

        Rate effectiveFixedRate(const std::vector<Spread>& spreads,
                                const std::vector<Rate>& caps,
                                const std::vector<Rate>& floors,
                                Size i);

        bool noOption(const std::vector<Rate>& caps,
                      const std::vector<Rate>& floors,
                      Size i);

    }


    template <typename InterestRateIndexType,
              typename FloatingCouponType,
              typename CappedFlooredCouponType>
    Leg FloatingLeg(const Schedule& schedule,
                    const std::vector<Real>& nominals,
                    const ext::shared_ptr<InterestRateIndexType>& index,
                    const DayCounter& paymentDayCounter,
                    BusinessDayConvention paymentAdj,
                    const std::vector<Natural>& fixingDays,
                    const std::vector<Real>& gearings,
                    const std::vector<Spread>& spreads,
                    const std::vector<Rate>& caps,
                    const std::vector<Rate>& floors,
                    bool isInArrears,
                    bool isZero,
                    Integer paymentLag = 0,
                    Calendar paymentCalendar = Calendar(),
                    Period exCouponPeriod = Period(),
                    Calendar exCouponCalendar = Calendar(),
                    BusinessDayConvention exCouponAdjustment = Unadjusted,
                    bool exCouponEndOfMonth = false) {

        Size n = schedule.size()-1;
        QL_REQUIRE(!nominals.empty(), "no notional given");
        QL_REQUIRE(nominals.size() <= n,
                   "too many nominals (" << nominals.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(gearings.size()<=n,
                   "too many gearings (" << gearings.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(spreads.size()<=n,
                   "too many spreads (" << spreads.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(caps.size()<=n,
                   "too many caps (" << caps.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(floors.size()<=n,
                   "too many floors (" << floors.size() <<
                   "), only " << n << " required");
        QL_REQUIRE(!isZero || !isInArrears,
                   "in-arrears and zero features are not compat