/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2005 Klaus Spanderen
 Copyright (C) 2007 StatPro Italia srl

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

/*! \file mceuropeanhestonengine.hpp
    \brief Monte Carlo Heston-model engine for European options
*/

#ifndef quantlib_mc_european_heston_engine_hpp
#define quantlib_mc_european_heston_engine_hpp

#include <ql/pricingengines/vanilla/mcvanillaengine.hpp>
#include <ql/processes/hestonprocess.hpp>
#include <utility>

namespace QuantLib {

    //! Monte Carlo Heston-model engine for European options
    /*! \ingroup vanillaengines

        \test the correctness of the returned value is tested by
              reproducing results available in web/literature
    */
    template <class RNG = PseudoRandom,
              class S = Statistics, class P = HestonProcess>
    class MCEuropeanHestonEngine
        : public MCVanillaEngine<MultiVariate,RNG,S> {
      public:
        typedef typename MCVanillaEngine<MultiVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        MCEuropeanHestonEngine(const ext::shared_ptr<P>&,
                               Size timeSteps,
                               Size timeStepsPerYear,
                               bool antitheticVariate,
                               Size requiredSamples,
                               Real requiredTolerance,
                               Size maxSamples,
                               BigNatural seed);
      protected:
        ext::shared_ptr<path_pricer_type> pathPricer() const override;
    };

    //! Monte Carlo Heston European engine factory
    template <class RNG = PseudoRandom,
              class S = Statistics, class P = HestonProcess>
    class MakeMCEuropeanHestonEngine {
      public:
        explicit MakeMCEuropeanHestonEngine(ext::shared_ptr<P>);
        // named parameters
        MakeMCEuropeanHestonEngine& withSteps(Size steps);
        MakeMCEuropeanHestonEngine& withStepsPerYear(Size steps);
        MakeMCEuropeanHestonEngine& withSamples(Size samples);
        MakeMCEuropeanHestonEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCEuropeanHestonEngine& withMaxSamples(Size samples);
        MakeMCEuropeanHestonEngine& withSeed(BigNatural seed);
        MakeMCEuropeanHestonEngine& withAntitheticVariate(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<P> process_;
        bool antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class EuropeanHestonPathPricer : public PathPricer<MultiPath> {
      public:
        EuropeanHestonPathPricer(Option::Type type,
                                 Real strike,
                                 DiscountFactor discount);
        Real operator()(const MultiPath& Multipath) const override;

      private:
        PlainVanillaPayoff payoff_;
        DiscountFactor discount_;
    };


    // template definitions

    template <class RNG, class S, class P>
    MCEuropeanHestonEngine<RNG, S, P>::MCEuropeanHestonEngine(
                const ext::shared_ptr<P>& process,
                Size timeSteps, Size timeStepsPerYear, bool antitheticVariate,
                Size
