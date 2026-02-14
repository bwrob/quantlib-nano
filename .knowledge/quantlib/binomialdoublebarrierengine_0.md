/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2015 Thema Consulting SA

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

/*! \file binomialdoublebarrierengine.hpp
    \brief Binomial Double Barrier option engine
*/

#ifndef quantlib_binomial_double_barrier_engine_hpp
#define quantlib_binomial_double_barrier_engine_hpp

#include <ql/experimental/barrieroption/discretizeddoublebarrieroption.hpp>
#include <ql/math/distributions/normaldistribution.hpp>
#include <ql/methods/lattices/binomialtree.hpp>
#include <ql/methods/lattices/bsmlattice.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/termstructures/volatility/equityfx/blackconstantvol.hpp>
#include <ql/termstructures/yield/flatforward.hpp>
#include <utility>

namespace QuantLib {

    //! Pricing engine for double barrier options using binomial trees
    /*! \ingroup barrierengines

        \note This engine requires a the discretized option classes.
        By default uses a standard binomial implementation, but it can
        also work with DiscretizedDermanKaniDoubleBarrierOption to
        implement a Derman-Kani optimization.

        \test the correctness of the returned values is tested by
              checking it against analytic results.
    */
    template <class T, class D = DiscretizedDoubleBarrierOption>
    class BinomialDoubleBarrierEngine : public DoubleBarrierOption::engine {
      public:
        BinomialDoubleBarrierEngine(ext::shared_ptr<GeneralizedBlackScholesProcess> process,
                                    Size timeSteps)
        : process_(std::move(process)), timeSteps_(timeSteps) {
            QL_REQUIRE(timeSteps>0,
                       "timeSteps must be positive, " << timeSteps <<
                       " not allowed");
            registerWith(process_);
        }
        void calculate() const override;

      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        Size timeSteps_;
    };


    // template definitions

    template <class T, class D>
    void BinomialDoubleBarrierEngine<T,D>::calculate() const {

        DayCounter rfdc  = process_->riskFreeRate()->dayCounter();
        DayCounter divdc = process_->dividendYield()->dayCounter();
        DayCounter voldc = process_->blackVolatility()->dayCounter();
        Calendar volcal = process_->blackVolatility()->calendar();

        Real s0 = process_->stateVariable()->value();
        QL_REQUIRE(s0 > 0.0, "negative or null underlying given");
        Volatility v = process_->blackVolatility()->blackVol(
            arguments_.exercise->lastDate(), s0);
        Date maturityDate = arguments_.exercise->lastDate();
        Rate r = process_->riskFreeRate()->zeroRate(maturityDate,
            rfdc, Continuous, NoFrequency);
        Rate q = process_->dividendYield()->zeroRate(maturityDate,
            divdc, Continuous, NoFrequency);
        Date referenceDate = process_->riskFreeRate()->referenceDate();

        // binomial trees with constant coefficient
        Handle<YieldTermStructure> flatRiskFree(
            ext::shared_ptr<YieldTermStructure>(
                new FlatForward(referenceDate, r, rfdc)));
        Handle<YieldTermStructure> flatDividends(
            ext::shared_ptr<YieldTermStructure>(
                new FlatForward(referenceDate, q, divdc)));
