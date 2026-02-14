/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006 StatPro Italia srl
 Copyright (C) 2004, 2005, 2006 Ferdinando Ametrano
 Copyright (C) 2006 Katiuscia Manzoni
 Copyright (C) 2006 Toyin Akin
 Copyright (C) 2015 Klaus Spanderen
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

/*! \file date.hpp
    \brief date- and time-related classes, typedefs and enumerations
*/

#ifndef quantlib_date_hpp
#define quantlib_date_hpp

#include <ql/time/period.hpp>
#include <ql/time/weekday.hpp>
#include <ql/utilities/null.hpp>

#ifdef QL_HIGH_RESOLUTION_DATE
#include <boost/date_time/posix_time/ptime.hpp>
#include <boost/date_time/posix_time/posix_time_duration.hpp>
#endif

#include <cstdint>
#include <utility>
#include <functional>
#include <string>


namespace QuantLib {

    //! Day number
    /*! \ingroup datetime */
    typedef Integer Day;

    //! Month names
    /*! \ingroup datetime */
    enum Month { January   = 1,
                 February  = 2,
                 March     = 3,
                 April     = 4,
                 May       = 5,
                 June      = 6,
                 July      = 7,
                 August    = 8,
                 September = 9,
                 October   = 10,
                 November  = 11,
                 December  = 12,
                 Jan = 1,
                 Feb = 2,
                 Mar = 3,
                 Apr = 4,
                 Jun = 6,
                 Jul = 7,
                 Aug = 8,
                 Sep = 9,
                 Oct = 10,
                 Nov = 11,
                 Dec = 12
    };

    /*! \relates Month */
    std::ostream& operator<<(std::ostream&, Month);

    //! Year number
    /*! \ingroup datetime */
    typedef Integer Year;

#ifdef QL_HIGH_RESOLUTION_DATE
    //! Hour number
    /*! \ingroup datetime */
    typedef boost::posix_time::hours::hour_type Hour;

    //! Minute number
    /*! \ingroup datetime */
    typedef boost::posix_time::minutes::min_type Minute;

    //! Second number
    /*! \ingroup datetime */
    typedef boost::posix_time::minutes::sec_type Second;

    //! Millisecond number
    /*! \ingroup datetime */
    typedef boost::posix_time::time_duration::fractional_seconds_type
        Millisecond;

    //! Microsecond number
    /*! \ingroup datetime */
    typedef boost::posix_time::time_duration::fractional_seconds_type
        Microsecond;
#endif

    //! Concrete date class
    /*! This class provides methods to inspect dates as well as methods and
        operators which implement a limited date algebra (increasing and
        decreasing dates, and calculating their difference).

        \ingroup datetime

        \test self-consistency of dates, serial numbers, days of
              month, months, and weekdays is checked over the whole
              date range.
    */

    class Date {
      public:
        //! serial number type
        typedef std::int_fast32_t serial_type;
        //! \name constructors
        //@{
        //! Default constructor returning a null date.
        Date();
        //! Constructor taking a serial number as given by Applix or Excel.
        explicit Date(Date::serial_type serialNumber);
