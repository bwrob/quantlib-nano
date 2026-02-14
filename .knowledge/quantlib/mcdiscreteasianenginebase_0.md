/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004 Ferdinando Ametrano
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

/*! \file mcdiscreteasianenginebase.hpp
    \brief Monte Carlo pricing engine for discrete average Asians
*/

#ifndef quantlib_mcdiscreteasian_engine_base_hpp
#define quantlib_mcdiscreteasian_engine_base_hpp

#include <ql/exercise.hpp>
#include <ql/instruments/asianoption.hpp>
#include <ql/pricingengines/mcsimulation.hpp>
#include <utility>

namespace QuantLib {


    namespace detail {

        class PastFixingsOnly : public Error {
          public:
            PastFixingsOnly()
            : Error("n/a", 0, "n/a",
                    "all fixings are in the past") {}
        };

    }

    //! Pricing engine for discrete average Asians using Monte Carlo simulation
    /*! \warning control-variate calculation is disabled under VC++6.
        \ingroup asianengines
    */

    template<template <class> class MC,
             class RNG = PseudoRandom, class S = Statistics>
    class MCDiscreteAveragingAsianEngineBase :
                                public DiscreteAveragingAsianOption::engine,
                                public McSimulation<MC,RNG,S> {
      public:
        typedef
        typename McSimulation<MC,RNG,S>::path_generator_type
            path_generator_type;
        typedef typename McSimulation<MC,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename McSimulation<MC,RNG,S>::stats_type
            stats_type;
        // constructor
        MCDiscreteAveragingAsianEngineBase(ext::shared_ptr<StochasticProcess> process,
                                           bool brownianBridge,
                                           bool antitheticVariate,
                                           bool controlVariate,
                                           Size requiredSamples,
                                           Real requiredTolerance,
                                           Size maxSamples,
                                           BigNatural seed,
                                           Size timeSteps = Null<Size>(),
                                           Size timeStepsPerYear = Null<Size>());
        void calculate() const override {
            try {
                McSimulation<MC,RNG,S>::calculate(requiredTolerance_,
                                                  requiredSamples_,
                                                  maxSamples_);
            } catch (detail::PastFixingsOnly&) {
                // Ideally, here we could calculate the payoff (which
                // is fully determine) and write it into the results.
                // This would probably need a new virtual method that
                // derived engines should implement.
                throw;
            }

            results_.value = this->mcModel_->sampleAccumulator().mean();

            if (this->controlVariate_) {
                // control variate might lead to small negative
                // option values for deep OTM options
                this->results_.value = std::max(0.0, this->results_.value);
            }

            if constexpr (RNG::allowsErrorEstimate)
          