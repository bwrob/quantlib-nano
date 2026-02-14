/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2026 Chirag Desai

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

/*! \file fxforward.hpp
    \brief FX Forward instrument
*/

#ifndef quantlib_fx_forward_hpp
#define quantlib_fx_forward_hpp

#include <ql/currency.hpp>
#include <ql/instrument.hpp>
#include <ql/time/calendar.hpp>
#include <ql/time/date.hpp>

namespace QuantLib {

    //! %FX Forward instrument
    /*! This class represents a foreign exchange forward contract,
        which is an agreement to exchange a specified amount of one
        currency for another currency at a future date at a
        predetermined exchange rate.

        The instrument supports various settlement conventions:
        - Overnight (O/N): settlementDays = 0
        - TomNext (T/N): settlementDays = 1
        - SpotNext (S/N): settlementDays = 2 (standard spot)

        The payment date is computed as the evaluation date plus
        settlementDays business days according to the specified calendar.

        The instrument can be valued using DiscountingFxForwardEngine,
        which computes the NPV by discounting the source and target
        legs using their respective yield curves.

        \ingroup instruments
    */
    class FxForward : public Instrument {
      public:
        class arguments;
        class results;
        class engine;
        //! \name Constructors
        //@{
        /*! Constructor for FX Forward using nominal amounts.
            \param sourceNominal     Notional amount in source(domestic) currency
            \param sourceCurrency    Currency of sourceNominal (source currency)
            \param targetNominal     Notional amount in target(foreign) currency
            \param targetCurrency    Currency of targetNominal (target currency)
            \param maturityDate      Settlement date of the forward contract
            \param paySourceCurrency If true, pay source currency and receive target currency;
                                     if false, receive source currency and pay target currency
            \param settlementDays    Number of business days for payment settlement
                                     (0=O/N, 1=T/N, 2=Spot, default=2)
            \param paymentCalendar   Calendar for computing payment date
                                     (defaults to NullCalendar)
        */
        FxForward(Real sourceNominal,
                  const Currency& sourceCurrency,
                  Real targetNominal,
                  const Currency& targetCurrency,
                  const Date& maturityDate,
                  bool paySourceCurrency,
                  Natural settlementDays = 2,
                  const Calendar& paymentCalendar = Calendar());

        /*! Constructor for FX Forward using exchange rate.
            \param sourceNominal     Notional amount in source currency
            \param sourceCurrency    Currency of nominal amount
            \param targetCurrency    Currency to exchange into
            \param forwardRate       The forward exchange rate (target/source)
            \param maturityDate      Settlement date of the forward contract
            \param paySourceCurrency If true, pay source currency and receive target currency;
                                     if false, receive source currency and
