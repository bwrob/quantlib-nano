/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006, 2007, 2008 StatPro Italia srl
 Copyright (C) 2007, 2008, 2009, 2015 Ferdinando Ametrano
 Copyright (C) 2007, 2009 Roland Lichters
 Copyright (C) 2015 Maddalena Zanzi
 Copyright (C) 2015 Paolo Mazzocchi
 Copyright (C) 2018 Matthias Lungwitz

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

/*! \file ratehelpers.hpp
    \brief deposit, FRA, futures, and various swap rate helpers
*/

#ifndef quantlib_ratehelpers_hpp
#define quantlib_ratehelpers_hpp

#include <ql/termstructures/bootstraphelper.hpp>
#include <ql/instruments/vanillaswap.hpp>
#include <ql/instruments/bmaswap.hpp>
#include <ql/instruments/futures.hpp>
#include <ql/time/calendar.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/optional.hpp>

namespace QuantLib {

    class SwapIndex;
    class Quote;

    typedef BootstrapHelper<YieldTermStructure> RateHelper;
    typedef RelativeDateBootstrapHelper<YieldTermStructure>
                                                        RelativeDateRateHelper;

    //! Rate helper for bootstrapping over IborIndex futures prices
    class FuturesRateHelper : public RateHelper {
      public:
        FuturesRateHelper(const std::variant<Real, Handle<Quote>>& price,
                          const Date& iborStartDate,
                          Natural lengthInMonths,
                          const Calendar& calendar,
                          BusinessDayConvention convention,
                          bool endOfMonth,
                          const DayCounter& dayCounter,
                          const std::variant<Real, Handle<Quote>>& convexityAdjustment = 0.0,
                          Futures::Type type = Futures::IMM);
        FuturesRateHelper(const std::variant<Real, Handle<Quote>>& price,
                          const Date& iborStartDate,
                          const Date& iborEndDate,
                          const DayCounter& dayCounter,
                          const std::variant<Real, Handle<Quote>>& convexityAdjustment = 0.0,
                          Futures::Type type = Futures::IMM);
        FuturesRateHelper(const std::variant<Real, Handle<Quote>>& price,
                          const Date& iborStartDate,
                          const ext::shared_ptr<IborIndex>& iborIndex,
                          const std::variant<Real, Handle<Quote>>& convexityAdjustment = 0.0,
                          Futures::Type type = Futures::IMM);
        //! \name RateHelper interface
        //@{
        Real impliedQuote() const override;
        //@}
        //! \name FuturesRateHelper inspectors
        //@{
        Real convexityAdjustment() const;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      private:
        Time yearFraction_;
        Handle<Quote> convAdj_;
    };


    //! Rate helper for bootstrapping over deposit rates
    class DepositRateHelper : public RelativeDateRateHelper {
      public:
        DepositRateHelper(const std::variant<Rate, Handle<Quote>>& rate,
                          const Period& tenor,
                          Natural fixingDays,
                          const Calendar& calendar,
                          Busines