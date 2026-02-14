/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2020 Lew Wei Hao

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

/*! \file mcdoublebarrierengine.hpp
    \brief Monte Carlo barrier option engines
*/

#ifndef quantlib_mc_double_barrier_engines_hpp
#define quantlib_mc_double_barrier_engines_hpp

#include <ql/exercise.hpp>
#include <ql/instruments/doublebarrieroption.hpp>
#include <ql/pricingengines/mcsimulation.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <utility>

namespace QuantLib {

    template <class RNG = PseudoRandom, class S = Statistics>
    class MCDoubleBarrierEngine : public DoubleBarrierOption::engine,
                                  public McSimulation<SingleVariate,RNG,S> {
      public:
        typedef typename McSimulation<SingleVariate,RNG,S>::path_generator_type
            path_generator_type;
        typedef typename McSimulation<SingleVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        // constructor
        MCDoubleBarrierEngine(ext::shared_ptr<GeneralizedBlackScholesProcess> process,
                              Size timeSteps,
                              Size timeStepsPerYear,
                              bool brownianBridge,
                              bool antithetic,
                              Size requiredSamples,
                              Real requiredTolerance,
                              Size maxSamples,
                              BigNatural seed);
        void calculate() const override {
            Real spot = process_->x0();
            QL_REQUIRE(spot > 0.0, "negative or null underlying given");
            QL_REQUIRE(!triggered(spot), "barrier touched");
            McSimulation<SingleVariate,RNG,S>::calculate(requiredTolerance_,
                                                         requiredSamples_,
                                                         maxSamples_);
            results_.value = this->mcModel_->sampleAccumulator().mean();
            if constexpr (RNG::allowsErrorEstimate)
                results_.errorEstimate =
                    this->mcModel_->sampleAccumulator().errorEstimate();
        }

      protected:
        // McSimulation implementation
        TimeGrid timeGrid() const override;
        ext::shared_ptr<path_generator_type> pathGenerator() const override {
            TimeGrid grid = timeGrid();
            typename RNG::rsg_type gen =
                RNG::make_sequence_generator(grid.size()-1,seed_);
            return ext::shared_ptr<path_generator_type>(
                         new path_generator_type(process_,
                                                 grid, gen, brownianBridge_));
        }
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
        // data members
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        Size timeSteps_, timeStepsPerYear_;
        Size requiredSamples_, maxSamples_;
        Real requiredTolerance_;
        bool antithetic_;
        bool brownianBridge_;
        BigNatural seed_;
    };

    //! Monte Carlo double-barrier-option engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCDoubleBarrierEngine {
      public:
        explicit MakeMCDoubleBarrierEngine(ext::shared_ptr<GeneralizedBlackScholesProcess
