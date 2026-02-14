/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2001, 2002, 2003 Sadruddin Rejeb
 Copyright (C) 2003, 2004, 2005, 2006, 2008 Ferdinando Ametrano
 Copyright (C) 2006 Mark Joshi
 Copyright (C) 2006 StatPro Italia srl
 Copyright (C) 2007 Cristina Duminuco
 Copyright (C) 2007 Chiara Fornarola
 Copyright (C) 2013 Gary Kennedy
 Copyright (C) 2015, 2024 Peter Caspers
 Copyright (C) 2017 Klaus Spanderen
 Copyright (C) 2019 Wojciech Ślusarski
 Copyright (C) 2020 Marcin Rybacki

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

/*! \file blackformula.hpp
    \brief Black formula
*/

#ifndef quantlib_blackformula_hpp
#define quantlib_blackformula_hpp

#include <ql/instruments/payoffs.hpp>
#include <ql/option.hpp>

namespace QuantLib {

    /*! Black 1976 formula
        \warning instead of volatility it uses standard deviation,
                 i.e. volatility*sqrt(timeToMaturity)
    */
    Real blackFormula(Option::Type optionType,
                      Real strike,
                      Real forward,
                      Real stdDev,
                      Real discount = 1.0,
                      Real displacement = 0.0);

    /*! Black 1976 formula
        \warning instead of volatility it uses standard deviation,
                 i.e. volatility*sqrt(timeToMaturity)
    */
    Real blackFormula(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                      Real forward,
                      Real stdDev,
                      Real discount = 1.0,
                      Real displacement = 0.0);

    /*! Black 1976 model forward derivative
        \warning instead of volatility it uses standard deviation,
                 i.e. volatility*sqrt(timeToMaturity)
    */
    Real blackFormulaForwardDerivative(Option::Type optionType,
                                       Real strike,
                                       Real forward,
                                       Real stdDev,
                                       Real discount = 1.0,
                                       Real displacement = 0.0);

    /*! Black 1976 model forward derivative
        \warning instead of volatility it uses standard deviation,
                 i.e. volatility*sqrt(timeToMaturity)
    */
    Real blackFormulaForwardDerivative(const ext::shared_ptr<PlainVanillaPayoff>& payoff,
                                       Real forward,
                                       Real stdDev,
                                       Real discount = 1.0,
                                       Real displacement = 0.0);

    /*! Approximated Black 1976 implied standard deviation,
        i.e. volatility*sqrt(timeToMaturity).

        It is calculated using Brenner and Subrahmanyan (1988) and Feinstein
        (1988) approximation for at-the-money forward option, with the
        extended moneyness approximation by Corrado and Miller (1996)
    */
    Real blackFormulaImpliedStdDevApproximation(Option::Type optionType,
                                                Real strike,
                                                Real forward,
                                                Real blackPrice,
                                                Real discount = 1.0,
                                                Real displacement = 0.0);

    /*! Approximated Black 1976 implie
