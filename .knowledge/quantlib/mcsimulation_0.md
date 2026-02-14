/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003 Ferdinando Ametrano
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
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

/*! \file mcsimulation.hpp
    \brief framework for Monte Carlo engines
*/

#ifndef quantlib_montecarlo_engine_hpp
#define quantlib_montecarlo_engine_hpp

#include <ql/methods/montecarlo/montecarlomodel.hpp>

namespace QuantLib {

    //! base class for Monte Carlo engines
    /*! Eventually this class might offer greeks methods.  Deriving a
        class from McSimulation gives an easy way to write a Monte
        Carlo engine.

        See McVanillaEngine as an example.
    */

    template <template <class> class MC, class RNG, class S = Statistics>
    class McSimulation {
      public:
        typedef typename MonteCarloModel<MC,RNG,S>::path_generator_type
            path_generator_type;
        typedef typename MonteCarloModel<MC,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename MonteCarloModel<MC,RNG,S>::stats_type
            stats_type;
        typedef typename MonteCarloModel<MC,RNG,S>::result_type result_type;

        virtual ~McSimulation() = default;
        //! add samples until the required absolute tolerance is reached
        result_type value(Real tolerance,
                          Size maxSamples = QL_MAX_INTEGER,
                          Size minSamples = 1023) const;
        //! simulate a fixed number of samples
        result_type valueWithSamples(Size samples) const;
        //! error estimated using the samples simulated so far
        result_type errorEstimate() const;
        //! access to the sample accumulator for richer statistics
        const stats_type& sampleAccumulator() const;
        //! basic calculate method provided to inherited pricing engines
        void calculate(Real requiredTolerance,
                       Size requiredSamples,
                       Size maxSamples) const;
      protected:
        McSimulation(bool antitheticVariate,
                     bool controlVariate)
        : antitheticVariate_(antitheticVariate),
          controlVariate_(controlVariate) {}
        virtual ext::shared_ptr<path_pricer_type> pathPricer() const = 0;
        virtual ext::shared_ptr<path_generator_type> pathGenerator()
                                                                   const = 0;
        virtual TimeGrid timeGrid() const = 0;
        virtual ext::shared_ptr<path_pricer_type> controlPathPricer() const {
            return ext::shared_ptr<path_pricer_type>();
        }
        virtual ext::shared_ptr<path_generator_type> 
        controlPathGenerator() const {
            return ext::shared_ptr<path_generator_type>();
        }
        virtual ext::shared_ptr<PricingEngine> controlPricingEngine() const {
            return ext::shared_ptr<PricingEngine>();
        }
        virtual result_type controlVariateValue() const {
            return Null<result_type>();
        }
        template <class Sequence>
        static Real maxError(const Sequence& sequence) {
            return *std::max_element(sequence.begin(), sequence.end());
        }
        static Real maxError(Real error) {
            return error;
        }
        
        mutable ext::shared_ptr<M