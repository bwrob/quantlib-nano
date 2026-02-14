/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Piero Del Boca
 Copyright (C) 2009 Chris Kenyon
 Copyright (C) 2015 Bernd Lewerenz

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

#ifndef quantlib_seasonality_hpp
#define quantlib_seasonality_hpp

#include <ql/time/daycounter.hpp>
#include <ql/time/frequency.hpp>
#include <ql/shared_ptr.hpp>
#include <vector>

namespace QuantLib {

    class InflationTermStructure;

    //! A transformation of an existing inflation swap rate.
    /*! This is an abstract class and contains the functions
        correctXXXRate which returns rates with the seasonality
        correction.  Currently only the price multiplicative version
        is implemented, but this covers stationary (1-year) and
        non-stationary (multi-year) seasonality depending on how many
        years of factors are given.  Seasonality is piecewise
        constant, hence it will work with un-interpolated inflation
        indices.

        A seasonality assumption can be used to fill in inflation swap
        curves between maturities that are usually given in integer
        numbers of years, e.g. 8,9,10,15,20, etc.  Historical
        seasonality may be observed in reported CPI values,
        alternatively it may be affected by known future events, e.g.
        announced changes in VAT rates.  Thus seasonality may be
        stationary or non-stationary.

        If seasonality is additive then both swap rates will show
        affects.  Additive seasonality is not implemented.
    */
    class Seasonality {

        public:

        //! \name Seasonality interface
        //@{
          virtual Rate
          correctZeroRate(const Date& d, Rate r, const InflationTermStructure& iTS) const = 0;
          virtual Rate
          correctYoYRate(const Date& d, Rate r, const InflationTermStructure& iTS) const = 0;
          /*! It is possible for multi-year seasonalities to be
              inconsistent with the inflation term structure they are
              given to.  This method enables testing - but programmers
              are not required to implement it.  E.g. for price
              seasonality the corrections at whole years after the
              inflation curve base date should be the same or else there
              can be an inconsistency with quoted instruments.
              Alternatively, the seasonality can be set _before_ the
              inflation curve is bootstrapped.
          */
          virtual bool isConsistent(const InflationTermStructure& iTS) const;
          //@}

          virtual ~Seasonality() = default;
    };

    //! Multiplicative seasonality in the price index (CPI/RPI/HICP/etc).

    /*! Stationary multiplicative seasonality in CPI/RPI/HICP (i.e. in
        price) implies that zero inflation swap rates are affected,
        but that year-on-year inflation swap rates show no effect.  Of
        course, if the seasonality in CPI/RPI/HICP is non-stationary
        then both swap rates will be affected.

        Factors must be in multiples of the minimum required for one
        year, e.g. 12 for monthly, and these factors are reused for as
        long as is required, i.e. they wrap around.  So, for example,
        if 24 factors are given this repeats every two years.  True
        stationary season
