/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008, 2009 Jose Aparicio
 Copyright (C) 2008 Roland Lichters
 Copyright (C) 2008 StatPro Italia srl

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

/*! \file creditdefaultswap.hpp
    \brief Credit default swap
*/

#ifndef quantlib_credit_default_swap_hpp
#define quantlib_credit_default_swap_hpp

#include <ql/instrument.hpp>
#include <ql/cashflows/simplecashflow.hpp>
#include <ql/default.hpp>
#include <ql/termstructures/defaulttermstructure.hpp>
#include <ql/time/schedule.hpp>
#include <ql/optional.hpp>

namespace QuantLib {

    class YieldTermStructure;
    class Claim;

    //! Credit default swap
    /*! \note This instrument currently assumes that the issuer did
              not default until today's date.

        \warning if <tt>Settings::includeReferenceDateCashFlows()</tt>
                 is set to <tt>true</tt>, payments occurring at the
                 settlement date of the swap might be included in the
                 NPV and therefore affect the fair-spread
                 calculation. This might not be what you want.

        \warning conventionalSpread (and impliedHazardRate) by default
                 use the mid-point engine, which is not ISDA conform.

        \ingroup instruments
    */
    class CreditDefaultSwap : public Instrument {
      public:
        class arguments;
        class results;
        class engine;
        enum PricingModel {
            Midpoint,
            ISDA
        };
        //! \name Constructors
        //@{
        //! CDS quoted as running-spread only
        /*! @param side  Whether the protection is bought or sold.
            @param notional  Notional value
            @param spread  Running spread in fractional units.
            @param schedule  Coupon schedule.
            @param paymentConvention  Business-day convention for
                                      payment-date adjustment.
            @param dayCounter  Day-count convention for accrual.
            @param settlesAccrual  Whether or not the accrued coupon is
                                   due in the event of a default.
            @param paysAtDefaultTime  If set to true, any payments
                                      triggered by a default event are
                                      due at default time. If set to
                                      false, they are due at the end of
                                      the accrual period.
            @param protectionStart  The first date where a default event will trigger the contract.
                                    Before the CDS Big Bang 2009, this was typically trade date (T) + 1 calendar day.
                                    After the CDS Big Bang 2009, protection is typically effective immediately i.e. on
                                    trade date so this is what should be entered for protection start.
                                    Notice that there is no default lookback period and protection start here.
                                    In the way it determines the dirty amount it is more like the trade execution date.
            @param lastPeriodDayCounter Day-count convention for accrual in last period
            @param rebatesAccrual  The protection seller pays the accrued

