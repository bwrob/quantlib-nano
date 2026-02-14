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

/*! \file mcforwardeuropeanbsengine.hpp
    \brief Monte Carlo engine for forward-starting strike-reset European options using BS process
*/

#ifndef quantlib_mc_forward_european_bs_engine_hpp
#define quantlib_mc_forward_european_bs_engine_hpp

#include <ql/pricingengines/forward/mcforwardvanillaengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <utility>

namespace QuantLib {

    /*! \ingroup forwardengines
        \test
        - the correctness of the returned value is tested by
          comparing prices to the analytic pricer for a range
          of moneynesses
    */
    template <class RNG = PseudoRandom, class S = Statistics>
    class MCForwardEuropeanBSEngine
        : public MCForwardVanillaEngine<SingleVariate,RNG,S> {
      public:
        typedef
        typename MCForwardVanillaEngine<SingleVariate,RNG,S>::path_generator_type
            path_generator_type;
        typedef
        typename MCForwardVanillaEngine<SingleVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename MCForwardVanillaEngine<SingleVariate,RNG,S>::stats_type
            stats_type;
        // constructor
        MCForwardEuropeanBSEngine(
             const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
             Size timeSteps,
             Size timeStepsPerYear,
             bool brownianBridge,
             bool antitheticVariate,
             Size requiredSamples,
             Real requiredTolerance,
             Size maxSamples,
             BigNatural seed);
      protected:
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
    };


    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCForwardEuropeanBSEngine {
      public:
        explicit MakeMCForwardEuropeanBSEngine(
            ext::shared_ptr<GeneralizedBlackScholesProcess> process);
        // named parameters
        MakeMCForwardEuropeanBSEngine& withSteps(Size steps);
        MakeMCForwardEuropeanBSEngine& withStepsPerYear(Size steps);
        MakeMCForwardEuropeanBSEngine& withBrownianBridge(bool b = false);
        MakeMCForwardEuropeanBSEngine& withSamples(Size samples);
        MakeMCForwardEuropeanBSEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCForwardEuropeanBSEngine& withMaxSamples(Size samples);
        MakeMCForwardEuropeanBSEngine& withSeed(BigNatural seed);
        MakeMCForwardEuropeanBSEngine& withAntitheticVariate(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        bool antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        bool brownianBridge_ = false;
        BigNatural seed_ = 0;
    };


    class ForwardEuropeanBSPathPricer : public PathPricer<Path> {
      public:
        ForwardEuropeanBSPathPricer(Option::Type type,
                                   Real moneyness,
                                   Size resetIndex,
                                   DiscountFactor discount);
        Real operator()(const Path& path) const override;

      private:
        Option::Type ty