/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Roland Lichters

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

/*! \file syntheticcdo.hpp
    \brief Synthetic Collateralized Debt Obligation and pricing engines
*/

#ifndef quantlib_synthetic_cdo_hpp
#define quantlib_synthetic_cdo_hpp

#include <ql/qldefines.hpp>

#ifndef QL_PATCH_SOLARIS

#include <ql/instrument.hpp>
#include <ql/default.hpp>
#include <ql/optional.hpp>
#include <ql/time/schedule.hpp>

#include <ql/experimental/credit/basket.hpp>
#include <ql/cashflows/fixedratecoupon.hpp>

namespace QuantLib {

    class YieldTermStructure;

    //! Synthetic Collateralized Debt Obligation
    /*!
      The instrument prices a mezzanine CDO tranche with loss given default
      between attachment point \f$ D_1\f$ and detachment point
      \f$ D_2 > D_1 \f$.

      For purchased protection, the instrument value is given by the difference
      of the protection value \f$ V_1 \f$ and premium value \f$ V_2 \f$,

      \f[ V = V_1 - V_2. \f]

      The protection leg is priced as follows:

      - Build the probability distribution for volume of defaults \f$ L \f$
      (before recovery) or Loss Given Default \f$ LGD = (1-r)\,L \f$ at
      times/dates \f$ t_i, i=1, ..., N\f$ (premium schedule times with
      intermediate steps)

      - Determine the expected value
      \f$ E_i = E_{t_i}\,\left[Pay(LGD)\right] \f$
      of the protection payoff \f$ Pay(LGD) \f$  at each time \f$ t_i\f$ where
      \f[
      Pay(L) = min (D_1, LGD) - min (D_2, LGD) = \left\{
      \begin{array}{lcl}
      \displaystyle 0 &;& LGD < D_1 \\
      \displaystyle LGD - D_1 &;& D_1 \leq LGD \leq D_2 \\
      \displaystyle D_2 - D_1 &;& LGD > D_2
      \end{array}
      \right.
      \f]

      - The protection value is then calculated as
      \f[ V_1 \:=\: \sum_{i=1}^N (E_i - E_{i-1}) \cdot  d_i \f]
      where \f$ d_i\f$ is the discount factor at time/date \f$ t_i \f$

      The premium is paid on the protected notional amount, initially
      \f$ D_2 - D_1. \f$ This notional amount is reduced by the expected
      protection
      payments \f$ E_i \f$ at times \f$ t_i, \f$ so that the premium value is
      calculated as

      \f[
      V_2 =m \, \cdot \sum_{i=1}^N \,(D_2 - D_1 - E_i) \cdot \Delta_{i-1,i}\,d_i
      \f]

      where \f$ m \f$ is the premium rate, \f$ \Delta_{i-1, i}\f$ is the day
      count fraction between date/time \f$ t_{i-1}\f$ and \f$ t_i.\f$

      The construction of the portfolio loss distribution \f$ E_i \f$ is
      based on the probability bucketing algorithm described in

      <strong>
      John Hull and Alan White, "Valuation of a CDO and nth to default CDS
      without Monte Carlo simulation", Journal of Derivatives 12, 2, 2004
      </strong>

      The pricing algorithm allows for varying notional amounts and
      default termstructures of the underlyings.

      \todo Investigate and fix cases \f$ E_{i+1} < E_i. \f$
    */
    class SyntheticCDO : public Instrument {
    public:
        class arguments;
        class results;
        class engine;

        // Review: No accrual settlement flag. No separate upfront payment date.
        // Review: Forward start case.
        /*! If the notional exceeds the basket inception tranche
            notional, the cdo is leveraged by th