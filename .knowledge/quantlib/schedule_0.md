/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006, 2007, 2011 Ferdinando Ametrano
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006, 2009 StatPro Italia srl

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

/*! \file schedule.hpp
    \brief date schedule
*/

#ifndef quantlib_schedule_hpp
#define quantlib_schedule_hpp

#include <ql/time/calendars/nullcalendar.hpp>
#include <ql/utilities/null.hpp>
#include <ql/time/period.hpp>
#include <ql/time/dategenerationrule.hpp>
#include <ql/errors.hpp>
#include <ql/optional.hpp>

namespace QuantLib {

    //! Payment schedule
    /*! \ingroup datetime */
    class Schedule {
      public:
        /*! constructor that takes any list of dates, and optionally
            meta information that can be used by client classes. Note
            that neither the list of dates nor the meta information is
            checked for plausibility in any sense. */
        Schedule(
            const std::vector<Date>&,
            Calendar calendar = NullCalendar(),
            BusinessDayConvention convention = Unadjusted,
            const ext::optional<BusinessDayConvention>& terminationDateConvention = ext::nullopt,
            const ext::optional<Period>& tenor = ext::nullopt,
            const ext::optional<DateGeneration::Rule>& rule = ext::nullopt,
            const ext::optional<bool>& endOfMonth = ext::nullopt,
            std::vector<bool> isRegular = std::vector<bool>(0));
        /*! rule based constructor */
        Schedule(Date effectiveDate,
                 const Date& terminationDate,
                 const Period& tenor,
                 Calendar calendar,
                 BusinessDayConvention convention,
                 BusinessDayConvention terminationDateConvention,
                 DateGeneration::Rule rule,
                 bool endOfMonth,
                 const Date& firstDate = Date(),
                 const Date& nextToLastDate = Date());
        Schedule() = default;
        //! \name Element access
        //@{
        Size size() const { return dates_.size(); }
        const Date& operator[](Size i) const;
        const Date& at(Size i) const;
        const Date& date(Size i) const;
        const std::vector<Date>& dates() const { return dates_; }
        bool empty() const { return dates_.empty(); }
        const Date& front() const;
        const Date& back() const;
        //@}
        //! \name Other inspectors
        //@{
        Date previousDate(const Date& refDate) const;
        Date nextDate(const Date& refDate) const;
        bool hasIsRegular() const;
        bool isRegular(Size i) const;
        const std::vector<bool>& isRegular() const;
        const Calendar& calendar() const;
        const Date& startDate() const;
        const Date& endDate() const;
        bool hasTenor() const;
        const Period& tenor() const;
        BusinessDayConvention businessDayConvention() const;
        bool hasTerminationDateBusinessDayConvention() const;
        BusinessDayConvention terminationDateBusinessDayConvention() const;
        bool hasRule() const;
        DateGeneration::Rule rule() const;
        bool hasEndOfMonth() const;
        bool endOfMonth() const;
        //@}
        //! \name Iterators
        //@{
        typedef std::vector<Date>::
