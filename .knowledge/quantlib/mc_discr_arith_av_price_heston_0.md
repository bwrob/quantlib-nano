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

/*! \file mc_discr_arith_av_price_heston.hpp
    \brief Heston MC engine for discrete arithmetic average price Asian
*/

#ifndef quantlib_mc_discrete_arithmetic_average_price_asian_heston_engine_hpp
#define quantlib_mc_discrete_arithmetic_average_price_asian_heston_engine_hpp

#include <ql/exercise.hpp>
#include <ql/experimental/asian/analytic_discr_geom_av_price_heston.hpp>
#include <ql/pricingengines/asian/mc_discr_geom_av_price_heston.hpp>
#include <ql/pricingengines/asian/mcdiscreteasianenginebase.hpp>
#include <ql/processes/hestonprocess.hpp>
#include <utility>

namespace QuantLib {

    //!  Heston MC pricing engine for discrete arithmetic average price Asian
    /*!
         By default, the MC discretization will use 1 time step per fixing date, but
         this can be controlled via timeSteps or timeStepsPerYear parameter, which
         will provide additional timesteps. The grid tries to space as evenly as it
         can and does not guarantee to match an exact number of steps, the precise
         grid used can be found in results_.additionalResults["TimeGrid"]

         Some performance metrics/graphs for the Control Variate are shown in the
         pull request: https://github.com/lballabio/QuantLib/pull/966

         \ingroup asianengines
         \test the correctness of the returned value is tested by
               reproducing results available in literature.
    */
    template <class RNG = PseudoRandom,
              class S = Statistics, class P = HestonProcess>
    class MCDiscreteArithmeticAPHestonEngine
        : public MCDiscreteAveragingAsianEngineBase<MultiVariate,RNG,S> {
      public:
        typedef typename MCDiscreteAveragingAsianEngineBase<MultiVariate,RNG,S>::path_generator_type path_generator_type;
        typedef typename MCDiscreteAveragingAsianEngineBase<MultiVariate,RNG,S>::path_pricer_type path_pricer_type;
        typedef typename MCDiscreteAveragingAsianEngineBase<MultiVariate,RNG,S>::stats_type stats_type;
        // constructor
        MCDiscreteArithmeticAPHestonEngine(
             const ext::shared_ptr<P>& process,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed,
             Size timeSteps = Null<Size>(),
             Size timeStepsPerYear = Null<Size>(),
             bool controlVariate = false);
      protected:
        ext::shared_ptr<path_pricer_type> pathPricer() const override;

        // Use the experimental analytic geometric asian option as a control variate.
        ext::shared_ptr<path_pricer_type> controlPathPricer() const override;
        ext::shared_ptr<PricingEngine> controlPricingEngine() const override {
            ext::shared_ptr<P> process = ext::dynamic_pointer_cast<P>(this->process_);
            QL_REQUIRE(process, "Heston-like process required");

            return ext::shared_ptr<PricingEngine>(new
                AnalyticDiscreteGeometricAveragePriceAsianHestonEngine(process));
        }
    };


    template <class RNG = PseudoRandom,
              class S = Statistics, class P = HestonProcess>
    class MakeMCDiscreteArithmeticAPHestonEngine {
      public:
        explicit 