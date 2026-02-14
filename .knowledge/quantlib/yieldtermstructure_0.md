/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2004, 2009 Ferdinando Ametrano
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006 StatPro Italia srl

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

/*! \file yieldtermstructure.hpp
    \brief Interest-rate term structure
*/

#ifndef quantlib_yield_term_structure_hpp
#define quantlib_yield_term_structure_hpp

#include <ql/termstructure.hpp>
#include <ql/interestrate.hpp>
#include <ql/quote.hpp>
#include <vector>

namespace QuantLib {

    class MultiCurveBootstrapContributor;

    //! Interest-rate term structure
    /*! This abstract class defines the interface of concrete
        interest rate structures which will be derived from this one.

        \ingroup yieldtermstructures

        \test observability against evaluation date changes is checked.
    */
    class YieldTermStructure : public TermStructure {
      public:
        /*! \name Constructors
            See the TermStructure documentation for issues regarding
            constructors.
        */
        //@{
        explicit YieldTermStructure(const DayCounter& dc = DayCounter());
        YieldTermStructure(const Date& referenceDate,
                           const Calendar& cal = Calendar(),
                           const DayCounter& dc = DayCounter(),
                           std::vector<Handle<Quote> > jumps = {},
                           const std::vector<Date>& jumpDates = {});
        YieldTermStructure(Natural settlementDays,
                           const Calendar& cal,
                           const DayCounter& dc = DayCounter(),
                           std::vector<Handle<Quote> > jumps = {},
                           const std::vector<Date>& jumpDates = {});
        //@}

        /*! \name Discount factors

            These methods return the discount factor from a given date or time
            to the reference date.  In the latter case, the time is calculated
            as a fraction of year from the reference date.
        */
        //@{
        DiscountFactor discount(const Date& d,
                                bool extrapolate = false) const;
        /*! The same day-counting rule used by the term structure
            should be used for calculating the passed time t.
        */
        DiscountFactor discount(Time t,
                                bool extrapolate = false) const;
        //@}

        /*! \name Zero-yield rates

            These methods return the implied zero-yield rate for a
            given date or time.  In the former case, the time is
            calculated as a fraction of year from the reference date.
        */
        //@{
        /*! The resulting interest rate has the required daycounting
            rule.
        */
        InterestRate zeroRate(const Date& d,
                              const DayCounter& resultDayCounter,
                              Compounding comp,
                              Frequency freq = Annual,
                              bool extrapolate = false) const;

        /*! The resulting interest rate has the same day-counting rule
            used by the term structure. The same rule should be used
            for calculating the passed time t.
        */
        InterestRate zeroRate(Time t,

