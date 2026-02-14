/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006 StatPro Italia srl
 Copyright (C) 2015 Peter Caspers
 Copyright (C) 2015 Michael von den Driesch

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

/*! \file optionletvolatilitystructure.hpp
    \brief optionlet (caplet/floorlet) volatility structure
*/

#ifndef quantlib_optionlet_volatility_structure_hpp
#define quantlib_optionlet_volatility_structure_hpp

#include <ql/termstructures/voltermstructure.hpp>
#include <ql/termstructures/volatility/optionlet/optionletstripper.hpp>
#include <ql/termstructures/volatility/volatilitytype.hpp>

namespace QuantLib {

    class SmileSection;

    //! Optionlet (caplet/floorlet) volatility structure
    /*! This class is purely abstract and defines the interface of
        concrete structures which will be derived from this one.
    */
    class OptionletVolatilityStructure : public VolatilityTermStructure {
      public:
        /*! \name Constructors
            See the TermStructure documentation for issues regarding
            constructors.
        */
        //@{
        //! default constructor
        /*! \warning term structures initialized by means of this
                     constructor must manage their own reference date
                     by overriding the referenceDate() method.
        */
        OptionletVolatilityStructure(BusinessDayConvention bdc = Following,
                                     const DayCounter& dc = DayCounter());
        //! initialize with a fixed reference date
        OptionletVolatilityStructure(const Date& referenceDate,
                                     const Calendar& cal,
                                     BusinessDayConvention bdc,
                                     const DayCounter& dc = DayCounter());
        //! calculate the reference date based on the global evaluation date
        OptionletVolatilityStructure(Natural settlementDays,
                                     const Calendar&,
                                     BusinessDayConvention bdc,
                                     const DayCounter& dc = DayCounter());
        //@}
        ~OptionletVolatilityStructure() override = default;
        //! \name Volatility and Variance
        //@{
        //! returns the volatility for a given option tenor and strike rate
        Volatility volatility(const Period& optionTenor,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the volatility for a given option date and strike rate
        Volatility volatility(const Date& optionDate,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the volatility for a given option time and strike rate
        Volatility volatility(Time optionTime,
                              Rate strike,
                              bool extrapolate = false) const;

        //! returns the Black variance for a given option tenor and strike rate
        Real blackVariance(const Period& optionTenor,
                           Rate strike,
                           bool extrapolate = false) const;
        //! returns the Black variance for a given option date and strike rate
 