/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
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

/*! \file mcforwardvanillaengine.hpp
    \brief Monte Carlo engine for forward-starting strike-reset vanilla options
*/

#ifndef quantlib_mcforwardvanilla_engine_hpp
#define quantlib_mcforwardvanilla_engine_hpp

#include <ql/instruments/forwardvanillaoption.hpp>
#include <ql/instruments/vanillaoption.hpp>
#include <ql/pricingengines/mcsimulation.hpp>
#include <utility>

namespace QuantLib {

    //! Monte Carlo engine for forward-starting vanilla options
    /*! \ingroup forwardengines
    */
    template<template <class> class MC,
             class RNG = PseudoRandom, class S = Statistics>
    class MCForwardVanillaEngine : public GenericEngine<ForwardOptionArguments<VanillaOption::arguments>,
                                                        VanillaOption::results>,
                                   public McSimulation<MC,RNG,S>
    {
      public:
        typedef typename McSimulation<MC,RNG,S>::path_generator_type
            path_generator_type;
        typedef typename McSimulation<MC,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename McSimulation<MC,RNG,S>::stats_type
            stats_type;
        // constructor
        MCForwardVanillaEngine(ext::shared_ptr<StochasticProcess> process,
                               Size timeSteps,
                               Size timeStepsPerYear,
                               bool brownianBridge,
                               bool antitheticVariate,
                               Size requiredSamples,
                               Real requiredTolerance,
                               Size maxSamples,
                               BigNatural seed,
                               bool controlVariate = false);
        void calculate() const override {
            McSimulation<MC,RNG,S>::calculate(requiredTolerance_,
                                              requiredSamples_,
                                              maxSamples_);
            this->results_.value = this->mcModel_->sampleAccumulator().mean();
            if constexpr (RNG::allowsErrorEstimate)
                this->results_.errorEstimate =
                    this->mcModel_->sampleAccumulator().errorEstimate();
        }

      protected:
        // McSimulation implementation
        TimeGrid timeGrid() const override;
        Real controlVariateValue() const override;
        ext::shared_ptr<path_generator_type> pathGenerator() const override {

            Size dimensions = process_->factors();
            TimeGrid grid = this->timeGrid();
            typename RNG::rsg_type gen =
                RNG::make_sequence_generator(dimensions*(grid.size()-1),seed_);
            return ext::shared_ptr<path_generator_type>(
                         new path_generator_type(process_, grid,
                                                 gen, brownianBridge_));
        }
        // data members
        ext::shared_ptr<StochasticProcess> process_;
        Size timeSteps_, timeStepsPerYear_, requiredSamples_, maxSamples_;
        Real requiredTolerance_;
        bool brownianBridge_;
        BigNatural seed_;
    };

    template <template <class> class MC, class RNG, class S>
    inline MCForwardVanillaEngine<MC, RNG, S>::MCFo
