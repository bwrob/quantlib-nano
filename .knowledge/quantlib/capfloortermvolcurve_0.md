/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Ferdinando Ametrano
 Copyright (C) 2007 Katiuscia Manzoni
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005 StatPro Italia srl

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

/*! \file capfloortermvolcurve.hpp
    \brief Cap/floor at-the-money term-volatility curve
*/

#ifndef quantlib_cap_volatility_vector_hpp
#define quantlib_cap_volatility_vector_hpp

#include <ql/termstructures/volatility/capfloor/capfloortermvolatilitystructure.hpp>
#include <ql/math/interpolation.hpp>
#include <ql/quote.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <vector>

namespace QuantLib {

    //! Cap/floor at-the-money term-volatility vector
    /*! This class provides the at-the-money volatility for a given cap/floor
        interpolating a volatility vector whose elements are the market
        volatilities of a set of caps/floors with given length.
    */
    class CapFloorTermVolCurve : public LazyObject,
                                 public CapFloorTermVolatilityStructure {
      public:
        //! floating reference date, floating market data
        CapFloorTermVolCurve(Natural settlementDays,
                             const Calendar& calendar,
                             BusinessDayConvention bdc,
                             const std::vector<Period>& optionTenors,
                             const std::vector<Handle<Quote> >& vols,
                             const DayCounter& dc = Actual365Fixed());
        //! fixed reference date, floating market data
        CapFloorTermVolCurve(const Date& settlementDate,
                             const Calendar& calendar,
                             BusinessDayConvention bdc,
                             const std::vector<Period>& optionTenors,
                             const std::vector<Handle<Quote> >& vols,
                             const DayCounter& dc = Actual365Fixed());
        //! fixed reference date, fixed market data
        CapFloorTermVolCurve(const Date& settlementDate,
                             const Calendar& calendar,
                             BusinessDayConvention bdc,
                             const std::vector<Period>& optionTenors,
                             const std::vector<Volatility>& vols,
                             const DayCounter& dc = Actual365Fixed());
        //! floating reference date, fixed market data
        CapFloorTermVolCurve(Natural settlementDays,
                             const Calendar& calendar,
                             BusinessDayConvention bdc,
                             const std::vector<Period>& optionTenors,
                             const std::vector<Volatility>& vols,
                             const DayCounter& dc = Actual365Fixed());

        // make class non-copyable and non-movable
        CapFloorTermVolCurve(CapFloorTermVolCurve&&) = delete;
        CapFloorTermVolCurve(const CapFloorTermVolCurve&) = delete;
        CapFloorTermVolCurve& operator=(CapFloorTermVolCurve&&) = delete;
        CapFloorTermVolCurve& operator=(const CapFloorTermVolCurve&) = delete;

        ~CapFloorTermVolCurve() override = default;

        //! \name TermStructure interface
        //@{
        Date
