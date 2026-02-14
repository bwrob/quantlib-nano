/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Yee Man Chan

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

/*! \file mceuropeangjrgarchengine.hpp
    \brief Monte Carlo GJR-GARCH-model engine for European options
*/

#ifndef quantlib_mc_european_gjrgarch_engine_hpp
#define quantlib_mc_european_gjrgarch_engine_hpp

#include <ql/pricingengines/vanilla/mcvanillaengine.hpp>
#include <ql/processes/gjrgarchprocess.hpp>
#include <utility>

namespace QuantLib {

    //! Monte Carlo GJR-GARCH-model engine for European options
    /*! \ingroup vanillaengines

        \test the correctness of the returned value is tested by
              reproducing results available in web/literature
    */
    template <class RNG = PseudoRandom, class S = Statistics>
    class MCEuropeanGJRGARCHEngine
        : public MCVanillaEngine<MultiVariate,RNG,S> {
      public:
        typedef typename MCVanillaEngine<MultiVariate,RNG,S>::path_pricer_type
            path_pricer_type;
        MCEuropeanGJRGARCHEngine(const ext::shared_ptr<GJRGARCHProcess>&,
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

    //! Monte Carlo GJR-GARCH European engine factory
    template <class RNG = PseudoRandom, class S = Statistics>
    class MakeMCEuropeanGJRGARCHEngine {
      public:
        MakeMCEuropeanGJRGARCHEngine(ext::shared_ptr<GJRGARCHProcess>);
        // named parameters
        MakeMCEuropeanGJRGARCHEngine& withSteps(Size steps);
        MakeMCEuropeanGJRGARCHEngine& withStepsPerYear(Size steps);
        MakeMCEuropeanGJRGARCHEngine& withSamples(Size samples);
        MakeMCEuropeanGJRGARCHEngine& withAbsoluteTolerance(Real tolerance);
        MakeMCEuropeanGJRGARCHEngine& withMaxSamples(Size samples);
        MakeMCEuropeanGJRGARCHEngine& withSeed(BigNatural seed);
        MakeMCEuropeanGJRGARCHEngine& withAntitheticVariate(bool b = true);
        // conversion to pricing engine
        operator ext::shared_ptr<PricingEngine>() const;
      private:
        ext::shared_ptr<GJRGARCHProcess> process_;
        bool antithetic_ = false;
        Size steps_, stepsPerYear_, samples_, maxSamples_;
        Real tolerance_;
        BigNatural seed_ = 0;
    };


    class EuropeanGJRGARCHPathPricer : public PathPricer<MultiPath> {
      public:
        EuropeanGJRGARCHPathPricer(Option::Type type,
                                 Real strike,
                                 DiscountFactor discount);
        Real operator()(const MultiPath& Multipath) const override;

      private:
        PlainVanillaPayoff payoff_;
        DiscountFactor discount_;
    };


    // template definitions

    template <class RNG, class S>
    MCEuropeanGJRGARCHEngine<RNG, S>::MCEuropeanGJRGARCHEngine(
                const ext::shared_ptr<GJRGARCHProcess>& process,
                Size timeSteps, Size timeStepsPerYear, bool antitheticVariate,
                Size requiredSamples, Real requiredToleranc