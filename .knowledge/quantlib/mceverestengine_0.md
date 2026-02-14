/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Master IMAFA - Polytech'Nice Sophia - Université de Nice Sophia Antipolis

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

/*! \file mceverestengine.hpp
    \brief Monte Carlo engine for Everest options
*/

#ifndef quantlib_mc_everest_engine_hpp
#define quantlib_mc_everest_engine_hpp

#include <ql/exercise.hpp>
#include <ql/experimental/exoticoptions/everestoption.hpp>
#include <ql/pricingengines/mcsimulation.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/processes/stochasticprocessarray.hpp>
#include <utility>

namespace QuantLib {

    template <class RNG = PseudoRandom, class S = Statistics>
    class MCEverestEngine : public EverestOption::engine,
                            public McSimulation<MultiVariate,RNG,S> {
      public:
        typedef typename McSimulation<MultiVariate,RNG,S>::path_generator_type
            path_generator_type;
        typedef typename McSimulation<MultiVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename McSimulation<MultiVariate,RNG,S>::stats_type
            stats_type;
        MCEverestEngine(ext::shared_ptr<StochasticProcessArray>,
                        Size timeSteps,
                        Size timeStepsPerYear,
                        bool brownianBridge,
                        bool antitheticVariate,
                        Size requiredSamples,
                        Real requiredTolerance,
                        Size maxSamples,
                        BigNatural seed);
        void calculate() const override {

            McSimulation<MultiVariate,RNG,S>::calculate(requiredTolerance_,
                                                        requiredSamples_,
                                                        maxSamples_);
            results_.value = this->mcModel_->sampleAccumulator().mean();

            if constexpr (RNG::allowsErrorEstimate) {
                results_.errorEstimate =
                    this->mcModel_->sampleAccumulator().errorEstimate();
            }

            Real notional = arguments_.notional;
            DiscountFactor discount = endDiscount();
            results_.yield = results_.value/(notional * discount) - 1.0;
        }

      private:
        DiscountFactor endDiscount() const;
        // McEverest implementation
        TimeGrid timeGrid() const override;
        ext::shared_ptr<path_generator_type> pathGenerator() const override {

            Size numAssets = processes_->size();

            TimeGrid grid = timeGrid();
            typename RNG::rsg_type gen =
                RNG::make_sequence_generator(numAssets*(grid.size()-1),seed_);

            return ext::shared_ptr<path_generator_type>(
                         new path_generator_type(processes_,
                                                 grid, gen, brownianBridge_));
        }
        ext::shared_ptr<path_pricer_type> pathPricer() const override;

        // data members
        ext::shared_ptr<StochasticProcessArray> processes_;
        Size timeSteps_, timeStepsPerYear_;
        Size requiredSamples_;
        Size maxSamples_;
        Real requiredTolerance_;
        bool brownianBridge_;
        BigNatural seed_;
    };


    //! Monte Carlo Everest-option engine factory
    template <
