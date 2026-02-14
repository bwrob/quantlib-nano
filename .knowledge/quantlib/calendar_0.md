/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006, 2007 StatPro Italia srl
 Copyright (C) 2006 Piter Dias
 Copyright (C) 2020 Leonardo Arcari
 Copyright (C) 2020 Kline s.r.l.

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

/*! \file calendar.hpp
    \brief %calendar class
*/

#ifndef quantlib_calendar_hpp
#define quantlib_calendar_hpp

#include <ql/errors.hpp>
#include <ql/time/date.hpp>
#include <ql/time/businessdayconvention.hpp>
#include <ql/shared_ptr.hpp>
#include <set>
#include <vector>
#include <string>

namespace QuantLib {

    class Period;

    //! %calendar class
    /*! This class provides methods for determining whether a date is a
        business day or a holiday for a given market, and for
        incrementing/decrementing a date of a given number of business days.

        The Bridge pattern is used to provide the base behavior of the
        calendar, namely, to determine whether a date is a business day.

        A calendar should be defined for specific exchange holiday schedule
        or for general country holiday schedule. Legacy city holiday schedule
        calendars will be moved to the exchange/country convention.

        \ingroup datetime

        \test the methods for adding and removing holidays are tested
              by inspecting the calendar before and after their
              invocation.
    */
    class Calendar {
      protected:
        //! abstract base class for calendar implementations
        class Impl {
          public:
            virtual ~Impl() = default;
            virtual std::string name() const = 0;
            virtual bool isBusinessDay(const Date&) const = 0;
            virtual bool isWeekend(Weekday) const = 0;
            std::set<Date> addedHolidays, removedHolidays;
        };
        ext::shared_ptr<Impl> impl_;
      public:
        /*! The default constructor returns a calendar with a null
            implementation, which is therefore unusable except as a
            placeholder.
        */
        Calendar() = default;
        //! \name Calendar interface
        //@{
        //!  Returns whether or not the calendar is initialized
        bool empty() const;
        //! Returns the name of the calendar.
        /*! \warning This method is used for output and comparison between
                calendars. It is <b>not</b> meant to be used for writing
                switch-on-type code.
        */
        std::string name() const;
        /*! Returns <tt>true</tt> iff the date is a business day for the
            given market.
        */

        /*! Returns the set of added holidays for the given calendar */
        const std::set<Date>& addedHolidays() const;

        /*! Returns the set of removed holidays for the given calendar */
        const std::set<Date>& removedHolidays() const;

        /*! Clear the set of added and removed holidays */
        void resetAddedAndRemovedHolidays();

        bool isBusinessDay(const Date& d) const;
        /*! Returns <tt>true</tt> iff the date is a holiday for the given
            market.
        */
        bool isHoliday(const Date& d) const;
        /*! Returns <tt>true</tt> iff the weekday is part of the
            weekend for the given market.
        */

