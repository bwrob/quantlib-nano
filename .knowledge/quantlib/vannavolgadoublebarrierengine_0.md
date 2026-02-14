/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2013 Yue Tian

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

/*! \file vannavolgadoublebarrierengine.hpp
    \brief Vanna/Volga double-barrier option engine
*/

#ifndef quantlib_vanna_volga_double_barrier_engine_hpp
#define quantlib_vanna_volga_double_barrier_engine_hpp

#include <ql/instruments/doublebarrieroption.hpp>
#include <ql/experimental/barrieroption/vannavolgainterpolation.hpp>
#include <ql/quotes/deltavolquote.hpp>
#include <ql/math/matrix.hpp>
#include <ql/pricingengines/barrier/analyticbarrierengine.hpp>
#include <ql/pricingengines/blackdeltacalculator.hpp>
#include <ql/pricingengines/blackformula.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/quotes/simplequote.hpp>
#include <ql/termstructures/volatility/equityfx/blackconstantvol.hpp>
#include <ql/time/calendars/nullcalendar.hpp>
#include <utility>

namespace QuantLib {

    //! Vanna Volga double-barrier option engine

    /*!
        \ingroup barrierengines
    */
   template <class DoubleBarrierEngine>
      class VannaVolgaDoubleBarrierEngine
           : public GenericEngine<DoubleBarrierOption::arguments,
                                  DoubleBarrierOption::results> {
         public:
           // Constructor
           VannaVolgaDoubleBarrierEngine(Handle<DeltaVolQuote> atmVol,
                                         Handle<DeltaVolQuote> vol25Put,
                                         Handle<DeltaVolQuote> vol25Call,
                                         Handle<Quote> spotFX,
                                         Handle<YieldTermStructure> domesticTS,
                                         Handle<YieldTermStructure> foreignTS,
                                         const bool adaptVanDelta = false,
                                         const Real bsPriceWithSmile = 0.0,
                                         int series = 5)
           : GenericEngine<DoubleBarrierOption::arguments, DoubleBarrierOption::results>(),
             atmVol_(std::move(atmVol)), vol25Put_(std::move(vol25Put)),
             vol25Call_(std::move(vol25Call)), T_(atmVol_->maturity()), spotFX_(std::move(spotFX)),
             domesticTS_(std::move(domesticTS)), foreignTS_(std::move(foreignTS)),
             adaptVanDelta_(adaptVanDelta), bsPriceWithSmile_(bsPriceWithSmile), series_(series) {

               QL_REQUIRE(vol25Put_->delta() == -0.25,
                          "25 delta put is required by vanna volga method");
               QL_REQUIRE(vol25Call_->delta() == 0.25,
                          "25 delta call is required by vanna volga method");

               QL_REQUIRE(vol25Put_->maturity() == vol25Call_->maturity() &&
                              vol25Put_->maturity() == atmVol_->maturity(),
                          "Maturity of 3 vols are not the same");

               QL_REQUIRE(!domesticTS_.empty(), "domestic yield curve is not defined");
               QL_REQUIRE(!foreignTS_.empty(), "foreign yield curve is not defined");

               registerWith(atmVol_);
               registerWith(vol25Put_);
               registerWith(vol25Call_);
               registerWith(spotFX_);
               registerWith(domesticTS_);
               registerWith(foreignTS_);
           }

             void calculate()
