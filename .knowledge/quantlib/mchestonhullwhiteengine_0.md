/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007, 2008 Klaus Spanderen

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

/*! \file mchestonhullwhiteengine.hpp
    \brief Monte Carlo vanilla option engine for stochastic interest rates
*/

#ifndef quantlib_mc_heston_hull_white_engine_hpp
#define quantlib_mc_heston_hull_white_engine_hpp

#include <ql/pricingengines/vanilla/analytichestonhullwhiteengine.hpp>
#include <ql/pricingengines/vanilla/mcvanillaengine.hpp>
#include <ql/processes/hestonprocess.hpp>
#include <ql/processes/hullwhiteprocess.hpp>
#include <ql/processes/hybridhestonhullwhiteprocess.hpp>
#include <utility>

namespace QuantLib {

    template <class RNG = PseudoRandom, class S = Statistics>
    class MCHestonHullWhiteEngine
        : public MCVanillaEngine<MultiVariate, RNG, S> {
      public:
        typedef MCVanillaEngine<MultiVariate, RNG,S> base_type;
        typedef typename base_type::path_generator_type path_generator_type;
        typedef typename base_type::path_pricer_type path_pricer_type;
        typedef typename base_type::stats_type stats_type;
        typedef typename base_type::result_type result_type;

        MCHestonHullWhiteEngine(
               const ext::shared_ptr<HybridHestonHullWhiteProcess>& process,
               Size timeSteps,
               Size timeStepsPerYear,
               bool antitheticVariate,
               bool controlVariate,
               Size requiredSamples,
               Real requiredTolerance,
               Size maxSamples,
               BigNatural seed);

        void calculate() const override;

      protected:
        // just to avoid upcasting
        ext::shared_ptr<HybridHestonHullWhiteProcess> process_;

        ext::shared_ptr<path_pricer_type> pathPricer() const override;

        ext::shared_ptr<path_pricer_type> controlPathPricer() const override;
        ext::shared_ptr<PricingEngine> controlPricingEngine() const override;
        ext::shared_ptr<path_generator_type> controlPathGenerator() const override;
    };

    //! Monte Carlo Heston/Hull-White engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCHestonHullWhiteEngine {
      public:
        explicit MakeMCHestonHullWhiteEngine(ext::shared_ptr<HybridHestonHullWhiteProcess>);
        // named parameters
        MakeMCHestonHullWhiteEngine& withSteps(Size steps);
        MakeMCHestonHullWhiteEngine& withStepsPerYear(Size steps);
        MakeMCHestonHullWhiteEngine& withAntitheticVariate(bool b = true);
        MakeMCHestonHullWhiteEngine& withControlVariate(bool b = true);
        MakeMCHestonHullWhiteEngine& withSamples(Size samples);
        MakeMCHestonHullWhiteEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCHestonHullWhiteEngine& withMaxSamples(Size samples);
        MakeMCHestonHullWhiteEngine& withSeed(BigNatural seed);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<HybridHestonHullWhiteProcess> process_;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        bool antithetic_ = false, controlVariate_ = false;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class HestonHullWhitePathPricer : public PathPricer<MultiPath> {
      public:

