/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006 StatPro Italia srl
 Copyright (C) 2006, 2008 Ferdinando Ametrano
 Copyright (C) 2015 Peter Caspers

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

/*! \file swaptionvolstructure.hpp
    \brief Swaption volatility structure
*/

#ifndef quantlib_swaption_volatility_structure_hpp
#define quantlib_swaption_volatility_structure_hpp

#include <ql/termstructures/voltermstructure.hpp>
#include <ql/termstructures/volatility/volatilitytype.hpp>

namespace QuantLib {

    class SmileSection;

    //! %Swaption-volatility structure
    /*! This abstract class defines the interface of concrete swaption
        volatility structures which will be derived from this one.
    */
    class SwaptionVolatilityStructure : public VolatilityTermStructure {
      public:
        /*! \name Constructors
            See the TermStructure documentation for issues regarding
            constructors.
        */
        //@{
        /*! \warning term structures initialized by means of this
                     constructor must manage their own reference date
                     by overriding the referenceDate() method.
        */
        SwaptionVolatilityStructure(BusinessDayConvention bdc,
                                    const DayCounter& dc = DayCounter());
        //! initialize with a fixed reference date
        SwaptionVolatilityStructure(const Date& referenceDate,
                                    const Calendar& calendar,
                                    BusinessDayConvention bdc,
                                    const DayCounter& dc = DayCounter());
        //! calculate the reference date based on the global evaluation date
        SwaptionVolatilityStructure(Natural settlementDays,
                                    const Calendar&,
                                    BusinessDayConvention bdc,
                                    const DayCounter& dc = DayCounter());
        //@}
        ~SwaptionVolatilityStructure() override = default;
        //! \name Volatility, variance and smile
        //@{
        //! returns the volatility for a given option tenor and swap tenor
        Volatility volatility(const Period& optionTenor,
                              const Period& swapTenor,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the volatility for a given option date and swap tenor
        Volatility volatility(const Date& optionDate,
                              const Period& swapTenor,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the volatility for a given option time and swap tenor
        Volatility volatility(Time optionTime,
                              const Period& swapTenor,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the volatility for a given option tenor and swap length
        Volatility volatility(const Period& optionTenor,
                              Time swapLength,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns th
