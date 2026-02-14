/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Allen Kuo

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

/*! \file callablebondvolstructure.hpp
    \brief Callable-bond volatility structure
*/

#ifndef quantlib_callable_bond_volatility_structure_hpp
#define quantlib_callable_bond_volatility_structure_hpp

#include <ql/termstructure.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/termstructures/volatility/smilesection.hpp>

namespace QuantLib {

    //! Callable-bond volatility structure
    /*! This class is purely abstract and defines the interface of
        concrete callable-bond volatility structures which will be
        derived from this one.
    */
    class CallableBondVolatilityStructure : public TermStructure {
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
        CallableBondVolatilityStructure(const DayCounter& dc = DayCounter(),
                                        BusinessDayConvention bdc = Following);
        //! initialize with a fixed reference date
        CallableBondVolatilityStructure(const Date& referenceDate,
                                        const Calendar& calendar = Calendar(),
                                        const DayCounter& dc = DayCounter(),
                                        BusinessDayConvention bdc = Following);
        //! calculate the reference date based on the global evaluation date
        CallableBondVolatilityStructure(Natural settlementDays,
                                        const Calendar&,
                                        const DayCounter& dc = DayCounter(),
                                        BusinessDayConvention bdc = Following);
        //@}
        ~CallableBondVolatilityStructure() override = default;
        //! \name Volatility, variance and smile
        //@{
        //! returns the volatility for a given option time and bondLength
        Volatility volatility(Time optionTime,
                              Time bondLength,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the Black variance for a given option time and bondLength
        Real blackVariance(Time optionTime,
                           Time bondLength,
                           Rate strike,
                           bool extrapolate = false) const;

        //! returns the volatility for a given option date and bond tenor
        Volatility volatility(const Date& optionDate,
                              const Period& bondTenor,
                              Rate strike,
                              bool extrapolate = false) const;
        //! returns the Black variance for a given option date and bond tenor
        Real blackVariance(const Date& optionDate,
                           const Period& bondTenor,
                           Rate strike,
                           bool extrapolate = false) const;
        virtual ext::sha