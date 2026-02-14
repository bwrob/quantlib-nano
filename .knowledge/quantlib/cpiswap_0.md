/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007, 2009, 2011 Chris Kenyon
 Copyright (C) 2009 StatPro Italia srl

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

/*! \file cpiswap.hpp
 \brief zero-inflation-indexed-ratio-with-base swap
 */

#ifndef quantlib_zeroinflationswap_hpp
#define quantlib_zeroinflationswap_hpp

#include <ql/instruments/swap.hpp>
#include <ql/time/calendar.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/cashflows/cpicoupon.hpp>

namespace QuantLib {

    class ZeroInflationIndex;

    //! zero-inflation-indexed swap,
    /*! fixed x zero-inflation, i.e. fixed x CPI(i'th fixing)/CPI(base)
        versus floating + spread

        Note that this does ony the inflation-vs-floating-leg.
        Extension to inflation-vs-fixed-leg.  is simple - just replace
        the floating leg with a fixed leg.

        Typically there are notional exchanges at the end: either
        inflated-notional vs notional; or just (inflated-notional -
        notional) vs zero.  The latter is perhaphs more typical.
        \warning Setting subtractInflationNominal to true means that
        the original inflation nominal is subtracted from both
        nominals before they are exchanged, even if they are
        different.

        This swap can mimic a ZCIIS where [(1+q)^n - 1] is exchanged
        against (cpi ratio - 1), by using differnt nominals on each
        leg and setting subtractInflationNominal to true.  ALSO -
        there must be just one date in each schedule.

        The two legs can have different schedules, fixing (days vs
        lag), settlement, and roll conventions.  N.B. accrual
        adjustment periods are already in the schedules.  Trade date
        and swap settlement date are outside the scope of the
        instrument.
    */
    class CPISwap : public Swap {
      public:
        class arguments;
        class results;
        class engine;

        /*! In this swap, the type (Payer or Receiver) refers to the floating leg. */
        CPISwap(Type type,
                Real nominal,
                bool subtractInflationNominal,
                // float+spread leg
                Spread spread,
                DayCounter floatDayCount,
                Schedule floatSchedule,
                const BusinessDayConvention& floatRoll,
                Natural fixingDays,
                ext::shared_ptr<IborIndex> floatIndex,
                // fixed x inflation leg
                Rate fixedRate,
                Real baseCPI,
                DayCounter fixedDayCount,
                Schedule fixedSchedule,
                const BusinessDayConvention& fixedRoll,
                const Period& observationLag,
                ext::shared_ptr<ZeroInflationIndex> fixedIndex,
                CPI::InterpolationType observationInterpolation = CPI::AsIndex,
                Real inflationNominal = Null<Real>());

        // results
        // float+spread
        virtual Real floatLegNPV() const;
        virtual Spread fairSpread() const;
        // fixed rate x inflation
        virtual Real fixedLegNPV() const;
        virtual Rate fairRate() const;

        // inspectors
        virtual Type type() const;
        virtual Real nominal() const;
        virtual
