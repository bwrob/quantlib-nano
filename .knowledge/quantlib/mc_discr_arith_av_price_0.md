/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004 Ferdinando Ametrano

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

/*! \file mc_discr_arith_av_price.hpp
    \brief Monte Carlo engine for discrete arithmetic average price Asian
*/

#ifndef quantlib_mc_discrete_arithmetic_average_price_asian_engine_hpp
#define quantlib_mc_discrete_arithmetic_average_price_asian_engine_hpp

#include <ql/exercise.hpp>
#include <ql/pricingengines/asian/analytic_discr_geom_av_price.hpp>
#include <ql/pricingengines/asian/mc_discr_geom_av_price.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <utility>

namespace QuantLib {

    //!  Monte Carlo pricing engine for discrete arithmetic average price Asian
    /*!  Monte Carlo pricing engine for discrete arithmetic average price
         Asian options. It can use MCDiscreteGeometricAPEngine (Monte Carlo
         discrete arithmetic average price engine) and
         AnalyticDiscreteGeometricAveragePriceAsianEngine (analytic discrete
         arithmetic average price engine) for control variation.

         \ingroup asianengines

         \test the correctness of the returned value is tested by
               reproducing results available in literature.
    */
    template <class RNG = PseudoRandom, class S = Statistics>
    class MCDiscreteArithmeticAPEngine
        : public MCDiscreteAveragingAsianEngineBase<SingleVariate,RNG,S> {
      public:
        typedef
        typename MCDiscreteAveragingAsianEngineBase<SingleVariate,RNG,S>::path_generator_type
            path_generator_type;
        typedef
        typename MCDiscreteAveragingAsianEngineBase<SingleVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename MCDiscreteAveragingAsianEngineBase<SingleVariate,RNG,S>::stats_type
            stats_type;
        // constructor
        MCDiscreteArithmeticAPEngine(
             const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
             bool brownianBridge,
             bool antitheticVariate,
             bool controlVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed);
      protected:
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
        ext::shared_ptr<path_pricer_type> controlPathPricer() const override;
        ext::shared_ptr<PricingEngine> controlPricingEngine() const override {
            ext::shared_ptr<GeneralizedBlackScholesProcess> process =
                ext::dynamic_pointer_cast<GeneralizedBlackScholesProcess>(
                    this->process_);
            QL_REQUIRE(process, "Black-Scholes process required");
            return ext::shared_ptr<PricingEngine>(new
                AnalyticDiscreteGeometricAveragePriceAsianEngine(process));
        }
    };


    class ArithmeticAPOPathPricer : public PathPricer<Path> {
      public:
        ArithmeticAPOPathPricer(Option::Type type,
                                Real strike,
                                DiscountFactor discount,
                                Real runningSum = 0.0,
                                Size pastFixings = 0);
        Real operator()(const Path& path) const override;

      private:
        PlainVa