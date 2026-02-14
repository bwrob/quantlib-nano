/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Andrea Odetti

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

/*! \file mcpathbasketengine.hpp
    \brief Path-dependent European basket MC engine
*/

#ifndef quantlib_mc_path_basket_engine_hpp
#define quantlib_mc_path_basket_engine_hpp

#include <ql/experimental/mcbasket/pathmultiassetoption.hpp>
#include <ql/experimental/mcbasket/pathpayoff.hpp>
#include <ql/pricingengines/mcsimulation.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/processes/stochasticprocessarray.hpp>
#include <ql/termstructures/yield/impliedtermstructure.hpp>
#include <ql/timegrid.hpp>
#include <utility>

namespace QuantLib {

    //! Pricing engine for path dependent basket options using
    //  Monte Carlo simulation
    template <class RNG = PseudoRandom, class S = Statistics>
    class MCPathBasketEngine  : public PathMultiAssetOption::engine,
                                public McSimulation<MultiVariate,RNG,S> {
      public:
        typedef typename McSimulation<MultiVariate,RNG,S>::path_generator_type
                                                          path_generator_type;
        typedef typename McSimulation<MultiVariate,RNG,S>::path_pricer_type
                                                             path_pricer_type;
        typedef typename McSimulation<MultiVariate,RNG,S>::stats_type
                                                                   stats_type;
        // constructor
        MCPathBasketEngine(ext::shared_ptr<StochasticProcessArray>,
                           Size timeSteps,
                           Size timeStepsPerYear,
                           bool brownianBridge,
                           bool antitheticVariate,
                           bool controlVariate,
                           Size requiredSamples,
                           Real requiredTolerance,
                           Size maxSamples,
                           BigNatural seed);

        void calculate() const override {
            McSimulation<MultiVariate,RNG,S>::calculate(requiredTolerance_,
                                                        requiredSamples_,
                                                        maxSamples_);
            results_.value = this->mcModel_->sampleAccumulator().mean();
            if constexpr (RNG::allowsErrorEstimate)
                results_.errorEstimate =
                    this->mcModel_->sampleAccumulator().errorEstimate();
        }

      protected:

        // McSimulation implementation
        TimeGrid timeGrid() const;
        ext::shared_ptr<path_generator_type> pathGenerator() const;
        ext::shared_ptr<path_pricer_type> pathPricer() const;

        // data members
        ext::shared_ptr<StochasticProcessArray> process_;
        Size timeSteps_;
        Size timeStepsPerYear_;
        Size requiredSamples_;
        Size maxSamples_;
        Real requiredTolerance_;
        bool brownianBridge_;
        BigNatural seed_;
    };


    class EuropeanPathMultiPathPricer : public PathPricer<MultiPath> {
      public:
        EuropeanPathMultiPathPricer(ext::shared_ptr<PathPayoff>& payoff,
                                    std::vector<Size> timePositions,
                                    std::vector<Handle<YieldTermStructure> > forw
