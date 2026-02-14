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

/*! \file mcforwardeuropeanhestonengine.hpp
    \brief Monte Carlo engine for forward-starting strike-reset European options using Heston-like process
*/

#ifndef quantlib_mc_forward_european_heston_engine_hpp
#define quantlib_mc_forward_european_heston_engine_hpp

#include <ql/models/equity/hestonmodel.hpp>
#include <ql/pricingengines/forward/mcforwardvanillaengine.hpp>
#include <ql/pricingengines/vanilla/analytichestonengine.hpp>
#include <ql/processes/hestonprocess.hpp>
#include <utility>

namespace QuantLib {

    /*! References:

        Control Variate trade-off considerations discussed in pull request:
        https://github.com/lballabio/QuantLib/pull/948

        \ingroup forwardengines

        \test
        - Heston MC prices for a flat Heston process are
          compared to analytical BS prices with the same
          volatility for a range of moneynesses
        - Heston MC prices for a forward-starting option
          resetting at  t=0 are compared to semi-analytical
          Heston prices for a range of moneynesses
    */
    template <class RNG = PseudoRandom,
              class S = Statistics, class P = HestonProcess>
    class MCForwardEuropeanHestonEngine
        : public MCForwardVanillaEngine<MultiVariate,RNG,S> {
      public:
        typedef
        typename MCForwardVanillaEngine<MultiVariate,RNG,S>::path_generator_type
            path_generator_type;
        typedef
        typename MCForwardVanillaEngine<MultiVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename MCForwardVanillaEngine<MultiVariate,RNG,S>::stats_type
            stats_type;
        // constructor
        MCForwardEuropeanHestonEngine(
             const ext::shared_ptr<P>& process,
             Size timeSteps,
             Size timeStepsPerYear,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed,
             bool controlVariate = false);
      protected:
        ext::shared_ptr<path_pricer_type> pathPricer() const override;

        // Use the vanilla option running from t=0 to t=expiryTime with an analytic Heston pricer
        // as a control variate. Works well if resetTime small.
        ext::shared_ptr<path_pricer_type> controlPathPricer() const override;
        ext::shared_ptr<PricingEngine> controlPricingEngine() const override {
            ext::shared_ptr<P> process = ext::dynamic_pointer_cast<P>(this->process_);
            QL_REQUIRE(process, "Heston-like process required");

            ext::shared_ptr<HestonModel> hestonModel(new HestonModel(process));
            return ext::shared_ptr<PricingEngine>(new
                AnalyticHestonEngine(hestonModel));
        }
    };


    template <class RNG = PseudoRandom,
              class S = Statistics, class P = HestonProcess>
    class MakeMCForwardEuropeanHestonEngine {
      public:
        explicit MakeMCForwardEuropeanHestonEngine(ext::shared_ptr<P> process);
        // named parameters
        MakeMCForwardEuropeanHestonEngine& withSteps(Size steps);
        MakeMCForwardEuropeanHestonEngine& withStepsPerYear(Size steps);
        MakeMCForwardEuropeanHestonEngi
