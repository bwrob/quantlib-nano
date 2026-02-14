/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2004 Neil Firth
 Copyright (C) 2006 Klaus Spanderen
 Copyright (C) 2007, 2008 StatPro Italia srl

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

/*! \file mcamericanbasketengine.hpp
    \brief Least-square Monte Carlo engines
*/

#ifndef quantlib_american_basket_montecarlo_engine_hpp
#define quantlib_american_basket_montecarlo_engine_hpp

#include <ql/exercise.hpp>
#include <ql/instruments/basketoption.hpp>
#include <ql/methods/montecarlo/lsmbasissystem.hpp>
#include <ql/pricingengines/mclongstaffschwartzengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/processes/stochasticprocessarray.hpp>
#include <functional>
#include <utility>

namespace QuantLib {

    //! least-square Monte Carlo engine
    /*! \warning This method is intrinsically weak for out-of-the-money
                 options.

        \ingroup basketengines
    */
    template <class RNG = PseudoRandom>
    class MCAmericanBasketEngine
        : public MCLongstaffSchwartzEngine<BasketOption::engine,
                                           MultiVariate,RNG> {
      public:
        MCAmericanBasketEngine(const ext::shared_ptr<StochasticProcessArray>&,
                               Size timeSteps,
                               Size timeStepsPerYear,
                               bool brownianBridge,
                               bool antitheticVariate,
                               Size requiredSamples,
                               Real requiredTolerance,
                               Size maxSamples,
                               BigNatural seed,
                               Size nCalibrationSamples = Null<Size>(),
                               Size polynomialOrder = 2,
                               LsmBasisSystem::PolynomialType polynomialType = LsmBasisSystem::Monomial);
      protected:
        ext::shared_ptr<LongstaffSchwartzPathPricer<MultiPath> > lsmPathPricer() const override;

      private:
        const Size polynomialOrder_;
        const LsmBasisSystem::PolynomialType polynomialType_;
    };


    //! Monte Carlo American basket-option engine factory
    template <class RNG = PseudoRandom>
    class MakeMCAmericanBasketEngine {
      public:
        MakeMCAmericanBasketEngine(ext::shared_ptr<StochasticProcessArray>);
        // named parameters
        MakeMCAmericanBasketEngine& withSteps(Size steps);
        MakeMCAmericanBasketEngine& withStepsPerYear(Size steps);
        MakeMCAmericanBasketEngine& withBrownianBridge(bool b = true);
        MakeMCAmericanBasketEngine& withAntitheticVariate(bool b = true);
        MakeMCAmericanBasketEngine& withSamples(Size samples);
        MakeMCAmericanBasketEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCAmericanBasketEngine& withMaxSamples(Size samples);
        MakeMCAmericanBasketEngine& withSeed(BigNatural seed);
        MakeMCAmericanBasketEngine& withCalibrationSamples(Size samples);
        MakeMCAmericanBasketEngine& withPolynomialOrder(Size polynmOrder);
        MakeMCAmericanBasketEngine& withBasisSystem(LsmBasisSystem::PolynomialType polynomialType);

        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<StochasticProcessArray> process_;

