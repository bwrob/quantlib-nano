/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003 Ferdinando Ametrano
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

/*! \file mceuropeanengine.hpp
    \brief Monte Carlo European option engine
*/

#ifndef quantlib_montecarlo_european_engine_hpp
#define quantlib_montecarlo_european_engine_hpp

#include <ql/pricingengines/vanilla/mcvanillaengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/termstructures/volatility/equityfx/blackconstantvol.hpp>
#include <ql/termstructures/volatility/equityfx/blackvariancecurve.hpp>

namespace QuantLib {

    //! European option pricing engine using Monte Carlo simulation
    /*! \ingroup vanillaengines

        \test the correctness of the returned value is tested by
              checking it against analytic results.
    */
    template <class RNG = PseudoRandom, class S = Statistics>
    class MCEuropeanEngine : public MCVanillaEngine<SingleVariate,RNG,S> {
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
        MCEuropeanEngine(
             const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
             Size timeSteps,
             Size timeStepsPerYear,
             bool brownianBridge,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed);
      protected:
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
    };

    //! Monte Carlo European engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCEuropeanEngine {
      public:
        MakeMCEuropeanEngine(ext::shared_ptr<GeneralizedBlackScholesProcess>);
        // named parameters
        MakeMCEuropeanEngine& withSteps(Size steps);
        MakeMCEuropeanEngine& withStepsPerYear(Size steps);
        MakeMCEuropeanEngine& withBrownianBridge(bool b = true);
        MakeMCEuropeanEngine& withSamples(Size samples);
        MakeMCEuropeanEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCEuropeanEngine& withMaxSamples(Size samples);
        MakeMCEuropeanEngine& withSeed(BigNatural seed);
        MakeMCEuropeanEngine& withAntitheticVariate(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        bool brownianBridge_ = false;
        BigNatural seed_ = 0;
    };

    class EuropeanPathPricer : public PathPricer<Path> {
      public:
        EuropeanPathPricer(Option::Type type,
                           Real strike,
                           DiscountFactor discount);
        Real operator()(const Path& path) const override;

      private:
        PlainVanillaPayoff payoff_