/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Andrea Odetti

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

#ifndef quantlib_mc_longstaff_schwartz_path_engine_hpp
#define quantlib_mc_longstaff_schwartz_path_engine_hpp

#include <ql/experimental/mcbasket/longstaffschwartzmultipathpricer.hpp>
#include <ql/pricingengines/mcsimulation.hpp>
#include <utility>

namespace QuantLib {

    //! Longstaff-Schwarz Monte Carlo engine for early exercise options
    /*! References:

        Francis Longstaff, Eduardo Schwartz, 2001. Valuing American Options
        by Simulation: A Simple Least-Squares Approach, The Review of
        Financial Studies, Volume 14, No. 1, 113-147

        \test the correctness of the returned value is tested by
              reproducing results available in web/literature
    */
    template <class GenericEngine, template <class> class MC,
              class RNG, class S = Statistics>
    class MCLongstaffSchwartzPathEngine : public GenericEngine,
                                      public McSimulation<MC,RNG,S> {
      public:
        typedef typename MC<RNG>::path_type path_type;
        typedef typename McSimulation<MC,RNG,S>::stats_type
            stats_type;
        typedef typename McSimulation<MC,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename McSimulation<MC,RNG,S>::path_generator_type
            path_generator_type;

        MCLongstaffSchwartzPathEngine(ext::shared_ptr<StochasticProcess> process,
                                      Size timeSteps,
                                      Size timeStepsPerYear,
                                      bool brownianBridge,
                                      bool antitheticVariate,
                                      bool controlVariate,
                                      Size requiredSamples,
                                      Real requiredTolerance,
                                      Size maxSamples,
                                      BigNatural seed,
                                      Size nCalibrationSamples = Null<Size>());

        void calculate() const;

      protected:
        virtual ext::shared_ptr<LongstaffSchwartzMultiPathPricer>
                                                    lsmPathPricer() const = 0;

        TimeGrid timeGrid() const;
        ext::shared_ptr<path_pricer_type> pathPricer() const;
        ext::shared_ptr<path_generator_type> pathGenerator() const;

        ext::shared_ptr<StochasticProcess> process_;
        const Size timeSteps_;
        const Size timeStepsPerYear_;
        const bool brownianBridge_;
        const Size requiredSamples_;
        const Real requiredTolerance_;
        const Size maxSamples_;
        const Size seed_;
        const Size nCalibrationSamples_;

        mutable ext::shared_ptr<LongstaffSchwartzMultiPathPricer> pathPricer_;
    };

    template <class GenericEngine, template <class> class MC, class RNG, class S>
    inline MCLongstaffSchwartzPathEngine<GenericEngine, MC, RNG, S>::MCLongstaffSchwartzPathEngine(
        ext::shared_ptr<StochasticProcess> process,
        Size timeSteps,
        Size timeStepsPerYear,
        bool brownianBridge,
        bool antitheticVariate,
        bool controlVariate,
        Size requiredSamples,
        Real requir