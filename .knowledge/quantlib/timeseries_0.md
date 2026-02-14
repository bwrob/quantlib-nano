/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Joseph Wang
 Copyright (C) 2010 Liquidnet Holdings, Inc.

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

/*! \file timeseries.hpp
    \brief Container for historical data
*/

#ifndef quantlib_timeseries_hpp
#define quantlib_timeseries_hpp

#include <ql/time/date.hpp>
#include <ql/utilities/null.hpp>
#include <ql/errors.hpp>
#include <boost/iterator/transform_iterator.hpp>
#include <functional>
#include <iterator>
#include <algorithm>
#include <map>
#include <vector>
#include <type_traits>

namespace QuantLib {

    //! Container for historical data
    /*! This class acts as a generic repository for a set of
        historical data.  Any single datum can be accessed through its
        date, while sets of consecutive data can be accessed through
        iterators.

        \pre The <c>Container</c> type must satisfy the requirements
             set by the C++ standard for associative containers.
    */
    template <class T, class Container = std::map<Date, T> >
    class TimeSeries {
      public:
        typedef Date key_type;
        typedef T value_type;
      private:
        mutable Container values_;
      public:
        /*! Default constructor */
        TimeSeries() = default;
        /*! This constructor initializes the history with a set of
            values passed as two sequences, the first containing dates
            and the second containing corresponding values.
        */
        template <class DateIterator, class ValueIterator>
        TimeSeries(DateIterator dBegin, DateIterator dEnd,
                   ValueIterator vBegin) {
            while (dBegin != dEnd)
                values_[*(dBegin++)] = *(vBegin++);
        }
        /*! This constructor initializes the history with a set of
            values. Such values are assigned to a corresponding number
            of consecutive dates starting from <b><i>firstDate</i></b>
            included.
        */
        template <class ValueIterator>
        TimeSeries(const Date& firstDate,
                   ValueIterator begin, ValueIterator end) {
            Date d = firstDate;
            while (begin != end)
                values_[d++] = *(begin++);
        }
        //! \name Inspectors
        //@{
        //! returns the first date for which a historical datum exists
        Date firstDate() const;
        //! returns the last date for which a historical datum exists
        Date lastDate() const;
        //! returns the number of historical data including null ones
        Size size() const;
        //! returns whether the series contains any data
        bool empty() const;
        //@}
        //! \name Historical data access
        //@{
        //! returns the (possibly null) datum corresponding to the given date
        T operator[](const Date& d) const {
            auto found = values_.find(d);
            if (found == values_.cend())
                return Null<T>();
            return found->second;
        }
        T& operator[](const Date& d) {
            auto found = values_.insert(std::pair<Date, T>(d, Null<T>())).first;
            return found->second;
        }
        //@}

        //! \name Iterators
        //@{
        typedef typename Container::const_iterator const_iterator;
        typedef t