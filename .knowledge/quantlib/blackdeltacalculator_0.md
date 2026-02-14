/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2010 Dimitri Reiswich

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

/*! \file blackdeltacalculator.hpp
    \brief Black-Scholes formula delta calculator class
*/

#ifndef quantlib_black_delta_calculator_hpp
#define quantlib_black_delta_calculator_hpp

#include <ql/pricingengines/blackcalculator.hpp>
#include <ql/math/distributions/normaldistribution.hpp>
#include <ql/math/solvers1d/brent.hpp>
#include <ql/quotes/deltavolquote.hpp>

namespace QuantLib {

    //! Black delta calculator class
    /*! Class includes many operations needed for different applications
        in FX markets, which has special quotation mechanisms, since
        every price can be expressed in both numeraires.
    */
    class BlackDeltaCalculator {
      public:
        //! \name Constructors
        //@{
        /*!
            \brief Constructs a BlackDeltaCalculator object 
            This class provides methods to calculate option delta and strike values
            using the Black-Scholes formula, supporting various FX delta conventions
            (spot, forward, premium-adjusted, etc.). It is designed for efficient
            repeated calculations across different strikes, which is useful in
            volatility smile construction and calibration routines.

            \param ot Option type (call or put)
            \param dt Delta type (spot, forward, premium-adjusted, etc.)
            \param spot Spot FX rate
            \param dDiscount Domestic discount factor
            \param fDiscount Foreign discount factor
            \param stdDev Standard deviation of the underlying
            
            \warning instead of volatility it uses standard deviation,
                 i.e. volatility*sqrt(timeToMaturity)
        */
        BlackDeltaCalculator(Option::Type ot,
                             DeltaVolQuote::DeltaType dt,
                             Real spot,
                             DiscountFactor dDiscount,   // domestic discount
                             DiscountFactor fDiscount,   // foreign discount
                             Real stdDev);
        //@}

        /*!
            \brief Computes the option delta for a given strike.

            Calculates the delta of an option using the Black-Scholes formula,
            according to the delta convention specified at construction (spot, forward, premium-adjusted, etc.).

            \param strike The option strike price.
            \return       The option delta under the chosen convention.
        */
        Real deltaFromStrike(Real strike) const;

        /*!
            \brief Computes the strike corresponding to a given delta.

            Inverts the Black-Scholes formula to find the strike that yields the specified delta,
            according to the delta convention set at construction. Used for constructing volatility smiles
            and for quoting FX options by delta.

            \param delta  The target option delta (under the chosen convention).
            \return       The strike price corresponding to the given delta.
        */
        Real strikeFromDelta(Real delta) const;

        /*!
            \brief Calculates the at-the-money (ATM) strike for the given ATM convention.
            
            Computes the strike pric