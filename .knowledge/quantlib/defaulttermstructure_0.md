/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Chris Kenyon
 Copyright (C) 2008 Roland Lichters
 Copyright (C) 2008 StatPro Italia srl
 Copyright (C) 2009 Ferdinando Ametrano

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

/*! \file defaulttermstructure.hpp
    \brief default-probability term structure
*/

#ifndef quantlib_default_term_structure_hpp
#define quantlib_default_term_structure_hpp

#include <ql/termstructure.hpp>
#include <ql/quote.hpp>

namespace QuantLib {

    //! Default probability term structure
    /*! This abstract class defines the interface of concrete
        credit structures which will be derived from this one.

        \ingroup defaultprobabilitytermstructures
    */
    class DefaultProbabilityTermStructure : public TermStructure {
      public:
        /*! \name Constructors
            See the TermStructure documentation for issues regarding
            constructors.
        */
        //@{
        DefaultProbabilityTermStructure(
            const DayCounter& dc = DayCounter(),
            std::vector<Handle<Quote> > jumps = {},
            const std::vector<Date>& jumpDates = {});
        DefaultProbabilityTermStructure(
            const Date& referenceDate,
            const Calendar& cal = Calendar(),
            const DayCounter& dc = DayCounter(),
            std::vector<Handle<Quote> > jumps = {},
            const std::vector<Date>& jumpDates = {});
        DefaultProbabilityTermStructure(
            Natural settlementDays,
            const Calendar& cal,
            const DayCounter& dc = DayCounter(),
            std::vector<Handle<Quote> > jumps = {},
            const std::vector<Date>& jumpDates = {});
        //@}

        /*! \name Survival probabilities

            These methods return the survival probability from the reference
            date until a given date or time.  In the latter case, the time
            is calculated as a fraction of year from the reference date.
        */
        //@{
        Probability survivalProbability(const Date& d,
                                        bool extrapolate = false) const;
        /*! The same day-counting rule used by the term structure
            should be used for calculating the passed time t.
        */
        Probability survivalProbability(Time t,
                                        bool extrapolate = false) const;
        //@}

        /*! \name Default probabilities

            These methods return the default probability from the reference
            date until a given date or time.  In the latter case, the time
            is calculated as a fraction of year from the reference date.
        */
        //@{
        Probability defaultProbability(const Date& d,
                                       bool extrapolate = false) const;
        /*! The same day-counting rule used by the term structure
            should be used for calculating the passed time t.
        */
        Probability defaultProbability(Time t,
                                       bool extrapolate = false) const;
        //! probability of default between two given dates
        Probability defaultProbability(const Date&,
                                       const Date&,
                                       bool extrapolate = false) const;
        //! pr
