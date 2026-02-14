/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2002, 2003 Ferdinando Ametrano
 Copyright (C) 2002, 2003 Sadruddin Rejeb
 Copyright (C) 2003 Neil Firth
 Copyright (C) 2007 StatPro Italia srl

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

/*! \file mcdigitalengine.hpp
    \brief digital option Monte Carlo engine
*/

#ifndef quantlib_digital_mc_engine_hpp
#define quantlib_digital_mc_engine_hpp

#include <ql/exercise.hpp>
#include <ql/methods/montecarlo/mctraits.hpp>
#include <ql/pricingengines/vanilla/mcvanillaengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <utility>

namespace QuantLib {

    //! Pricing engine for digital options using Monte Carlo simulation
    /*! Uses the Brownian Bridge correction for the barrier found in
        <i>
        Going to Extremes: Correcting Simulation Bias in Exotic
        Option Valuation - D.R. Beaglehole, P.H. Dybvig and G. Zhou
        Financial Analysts Journal; Jan/Feb 1997; 53, 1. pg. 62-68
        </i>
        and
        <i>
        Simulating path-dependent options: A new approach -
        M. El Babsiri and G. Noel
        Journal of Derivatives; Winter 1998; 6, 2; pg. 65-83
        </i>

        \ingroup vanillaengines

        \test the correctness of the returned value in case of
              cash-or-nothing at-hit digital payoff is tested by
              reproducing known good results.
    */
    template<class RNG = PseudoRandom, class S = Statistics>
    class MCDigitalEngine : public MCVanillaEngine<SingleVariate,RNG,S> {
      public:
        typedef
        typename MCVanillaEngine<SingleVariate,RNG,S>::path_generator_type
            path_generator_type;
        typedef
        typename MCVanillaEngine<SingleVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename MCVanillaEngine<SingleVariate,RNG,S>::stats_type
            stats_type;
        // constructor
        MCDigitalEngine(
                    const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
                    Size timeSteps,
                    Size timeStepsPerYear,
                    bool brownianBridge,
                    bool antitheticVariate,
                    Size requiredSamples,
                    Real requiredTolerance,
                    Size maxSamples,
                    BigNatural seed);
      protected:
        // McSimulation implementation
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
    };

    //! Monte Carlo digital engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCDigitalEngine {
      public:
        MakeMCDigitalEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);
        // named parameters
        MakeMCDigitalEngine& withSteps(Size steps);
        MakeMCDigitalEngine& withStepsPerYear(Size steps);
        MakeMCDigitalEngine& withBrownianBridge(bool b = true);
        MakeMCDigitalEngine& withSamples(Size samples);
        MakeMCDigitalEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCDigitalEngine& withMaxSamples(Size samples);
        MakeMCDigitalEngine& withSeed(BigNatural seed);
        MakeMCDigitalEngine& withAntitheticVariate