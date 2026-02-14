/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Warren Chou

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

/*! \file mcvarianceswapengine.hpp
    \brief Monte Carlo variance-swap engine
*/

#ifndef quantlib_mc_varianceswap_engine_hpp
#define quantlib_mc_varianceswap_engine_hpp

#include <ql/instruments/varianceswap.hpp>
#include <ql/math/integrals/segmentintegral.hpp>
#include <ql/pricingengines/mcsimulation.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <utility>

namespace QuantLib {

    //! Variance-swap pricing engine using Monte Carlo simulation,
    /*! as described in Demeterfi, Derman, Kamal & Zou,
        "A Guide to Volatility and Variance Swaps", 1999

        \ingroup forwardengines

        \todo define tolerance of numerical integral and incorporate it
              in errorEstimate

        \test returned fair variances checked for consistency with
              implied volatility curve.
    */
    template <class RNG = PseudoRandom, class S = Statistics>
    class MCVarianceSwapEngine : public VarianceSwap::engine,
                                 public McSimulation<SingleVariate,RNG,S> {
      public:
        typedef
        typename McSimulation<SingleVariate,RNG,S>::path_generator_type
            path_generator_type;
        typedef
        typename McSimulation<SingleVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename McSimulation<SingleVariate,RNG,S>::stats_type
            stats_type;
        // constructor
        MCVarianceSwapEngine(ext::shared_ptr<GeneralizedBlackScholesProcess> process,
                             Size timeSteps,
                             Size timeStepsPerYear,
                             bool brownianBridge,
                             bool antitheticVariate,
                             Size requiredSamples,
                             Real requiredTolerance,
                             Size maxSamples,
                             BigNatural seed);
        // calculate variance via Monte Carlo
        void calculate() const override {
            McSimulation<SingleVariate,RNG,S>::calculate(requiredTolerance_,
                                                         requiredSamples_,
                                                         maxSamples_);
            results_.variance =
                     this->mcModel_->sampleAccumulator().mean();

            DiscountFactor riskFreeDiscount =
                process_->riskFreeRate()->discount(arguments_.maturityDate);
            Real multiplier;
            switch (arguments_.position) {
              case Position::Long:
                multiplier = 1.0;
                break;
              case Position::Short:
                multiplier = -1.0;
                break;
              default:
                QL_FAIL("Unknown position");
            }
            multiplier *= riskFreeDiscount * arguments_.notional;

            results_.value =
                multiplier * (results_.variance - arguments_.strike);

            if constexpr (RNG::allowsErrorEstimate) {
                Real varianceError =
                    this->mcModel_->sampleAccumulator().errorEstimate();
                results_.errorEstimate = multiplier * varianceError;
            }
        }

      protected:
