/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2013, 2018 Peter Caspers

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

/*! \file markovfunctional.hpp
    \brief Markov Functional 1 Factor Model
*/

#ifndef quantlib_markovfunctional_hpp
#define quantlib_markovfunctional_hpp

#include <ql/math/interpolation.hpp>
#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <ql/processes/mfstateprocess.hpp>
#include <ql/termstructures/volatility/optionlet/optionletvolatilitystructure.hpp>
#include <ql/termstructures/volatility/smilesection.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <utility>

namespace QuantLib {

    /*! One factor Markov Functional model class. Some documentation is
        available here
        http://ssrn.com/abstract_id=2183721
        http://quantlib.org/slides/qlws13/caspers.pdf
    */

    /*! The model requires a suitable input smile which means it should be
      arbitrage free, smooth (at least implying a C^1 call price function) and
      with a call price function not decreasing too slow in strike  direction.

      A method for arbitrage free extra- and interpolation due to Kahale is
      provided and may be used to improve an input smile. Alternatively a
      SABR smile with arbitrage free wings can be fitted to the input smile
      to provide an appropriate input smile.

      If you use the Kahale or SABR method for smile pretreatment then this
      implies zero density for underlying rates below minus the displacement
      parameter. This means that in this case the market yield term structure
      must imply underlying atm forward rates greater than minus displacement.

      If you do not use a smile pretreatment you should ensure that the input
      smileSection is arbitrage free and  that the input smileSection covers the
      strikes from lowerRateBound to upperRateBound.

      During calibration a monocurve setup is assumed with the given yield term
      structure determining the rates throughout, no matter what curves are
      linked to the indices in the volatility term structures. The yield term
      structure should therefore be the main risk curve, i.e. the forwarding curve
      for the respective swaption or cap underlyings.

      The model uses a simplified formula for the npv of a swaps floating leg
      namely $P(t,T_0)-P(t,T_1)$ with  $T_0$ being the start date of the leg
      and $T_1$ being the last payment date, which is an approximation to the
      true npv.

      The model calibrates to slightly modified market options in the sense that
      the start date is set equal to the  fixing date, i.e. there is no delay.
      The model diagnostic outputs refer to this modified instrument. In general
      the actual market instrument including the delay is still matched very
      well though the calibration is done on a slightly different instrument.

      AdjustYts and AdjustDigitals are experimental options. Specifying
      AdjustYts may have a negative impact on the volatility smile match, so
      it should be used with special care. For long term calibration it seems
      an interesting option though.

      A bad fit to the initial yield term structure may be due to a non suitable
      input smile or accumulating n