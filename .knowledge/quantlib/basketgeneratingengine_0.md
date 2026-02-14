/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2013 Peter Caspers

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

/*! \file basketgeneratingengine.hpp
    \brief base class for pricing engines capable of
           generating a calibration basket
*/

#ifndef quantlib_basketgeneratingengine_hpp
#define quantlib_basketgeneratingengine_hpp

#include <ql/cashflows/fixedratecoupon.hpp>
#include <ql/cashflows/iborcoupon.hpp>
#include <ql/indexes/swapindex.hpp>
#include <ql/instruments/vanillaswap.hpp>
#include <ql/math/optimization/costfunction.hpp>
#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <ql/qldefines.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <utility>

namespace QuantLib {

    /* \warning the generated calibrating swaptions have a strike floored at
       0.1bp (minus lognormal shift, if applicable), this is not true for atm
       swaptions where the strike is generated in the swaption helper.

       \warning the standardSwapBase index should have associated forward and
       discount curves. These curves are used for setup of the swaption helper.
       This means that the market price of the calibration instrument is calculated
       using these curves. Therefore the model price must be calculated using the
       same curves, otherwise the calibration gets incosistent, i.e. the pricing
       engine used for model calibration has to be capable of using the same curves
       as associated to the index. Also the volatility structure passed to construct
       the calibration helper should use curves that are consistent with the model
       calibration curve setup. Finally the discountCurve given in the constructor
       should be the same curve as the discounting curve of the swapIndex used to
       determine the calibration basket. */

    class BasketGeneratingEngine {

      public:

        typedef enum CalibrationBasketType {
            Naive,
            MaturityStrikeByDeltaGamma
        } CalibrationBasketType;

        virtual ~BasketGeneratingEngine() = default;

        std::vector<ext::shared_ptr<BlackCalibrationHelper>>
        calibrationBasket(const ext::shared_ptr<Exercise>& exercise,
                          const ext::shared_ptr<SwapIndex>& standardSwapBase,
                          const ext::shared_ptr<SwaptionVolatilityStructure>& swaptionVolatility,
                          CalibrationBasketType basketType = MaturityStrikeByDeltaGamma) const;

      protected:
        BasketGeneratingEngine(const ext::shared_ptr<Gaussian1dModel>& model,
                               Handle<Quote> oas,
                               Handle<YieldTermStructure> discountCurve)
        : onefactormodel_(model), oas_(std::move(oas)), discountCurve_(std::move(discountCurve)) {}

        BasketGeneratingEngine(Handle<Gaussian1dModel> model,
                               Handle<Quote> oas,
                               Handle<YieldTermStructure> discountCurve)
        : onefactormodel_(std::move(model)), oas_(std::move(oas)),
          discountCurve_(std::move(discountCurve)) {}

        virtual Real underlyingNpv(const Date& expiry, Real y) const = 0;

        virtual Swap::Type underlyingType() const = 0;
