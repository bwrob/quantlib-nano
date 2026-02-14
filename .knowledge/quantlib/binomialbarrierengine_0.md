/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2014 Thema Consulting SA

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

/*! \file binomialbarrierengine.hpp
    \brief Binomial Barrier option engine
*/

#ifndef quantlib_binomial_barrier_engine_hpp
#define quantlib_binomial_barrier_engine_hpp

#include <ql/math/distributions/normaldistribution.hpp>
#include <ql/methods/lattices/binomialtree.hpp>
#include <ql/methods/lattices/bsmlattice.hpp>
#include <ql/pricingengines/barrier/discretizedbarrieroption.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/termstructures/volatility/equityfx/blackconstantvol.hpp>
#include <ql/termstructures/yield/flatforward.hpp>
#include <type_traits>
#include <utility>

namespace QuantLib {

    //! Pricing engine for barrier options using binomial trees
    /*! \ingroup barrierengines

        \note Timesteps for Cox-Ross-Rubinstein trees are adjusted using Boyle and Lau algorithm.
              See Journal of Derivatives, 1/1994,
              "Bumping up against the barrier with the binomial method"

        \test the correctness of the returned values is tested by
              checking it against analytic european results.
    */
    template <class T, class D>
    class BinomialBarrierEngine : public BarrierOption::engine {
      public:
        /*! The maxTimeSteps parameter is used to limit timeSteps when
            using Boyle-Lau optimization. If zero (the default) the
            maximum number of steps is calculated by an heuristic:
            anything when < 1000, otherwise no more than 5*timeSteps.
            If maxTimeSteps is equal to timeSteps, Boyle-Lau is
            disabled.  Likewise if the lattice is not
            CoxRossRubinstein Boyle-Lau is disabled and maxTimeSteps
            ignored.
        */
        BinomialBarrierEngine(ext::shared_ptr<GeneralizedBlackScholesProcess> process,
                              Size timeSteps,
                              Size maxTimeSteps = 0)
        : process_(std::move(process)), timeSteps_(timeSteps), maxTimeSteps_(maxTimeSteps) {
            QL_REQUIRE(timeSteps>0,
                       "timeSteps must be positive, " << timeSteps <<
                       " not allowed");
            QL_REQUIRE(maxTimeSteps==0 || maxTimeSteps>=timeSteps,
                       "maxTimeSteps must be zero or "
                       "greater than or equal to timeSteps, "
                       << maxTimeSteps << " not allowed");
            if (maxTimeSteps_==0)
               maxTimeSteps_ = std::max( (Size)1000, timeSteps_*5);
            registerWith(process_);
        }
        void calculate() const override;

      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        Size timeSteps_;
        Size maxTimeSteps_;
    };


    // template definitions

    template <class T, class D>
    void BinomialBarrierEngine<T,D>::calculate() const {

        ext::shared_ptr<StrikedTypePayoff> payoff =
            ext::dynamic_pointer_cast<StrikedTypePayoff>(arguments_.payoff);
        QL_REQUIRE(payoff, "non-striked payoff given");
        QL_REQUIRE(payoff->strike() > 0.0, "strike must be positive");

        Real s0 = process_->stateVariable()->value();
        QL_REQUIRE(s0 > 0.0, "negative or null underlying given");
        QL