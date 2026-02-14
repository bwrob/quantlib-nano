/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Warren Chou
 Copyright (C) 2007, 2008 StatPro Italia srl

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

/*! \file replicatingvarianceswapengine.hpp
    \brief Replicating engine for variance swaps
*/

#ifndef quantlib_replicating_varianceswap_engine_hpp
#define quantlib_replicating_varianceswap_engine_hpp

#include <ql/exercise.hpp>
#include <ql/instruments/europeanoption.hpp>
#include <ql/instruments/varianceswap.hpp>
#include <ql/pricingengines/vanilla/analyticeuropeanengine.hpp>
#include <utility>

namespace QuantLib {

    //! Variance-swap pricing engine using replicating cost,
    /*! as described in Demeterfi, Derman, Kamal & Zou,
        "A Guide to Volatility and Variance Swaps", 1999

        \ingroup forwardengines

        \test returned variances verified against results from literature
    */
    class ReplicatingVarianceSwapEngine : public VarianceSwap::engine {
      public:
        typedef std::vector<std::pair<
                   ext::shared_ptr<StrikedTypePayoff>, Real> > weights_type;
        // constructor
        ReplicatingVarianceSwapEngine(ext::shared_ptr<GeneralizedBlackScholesProcess> process,
                                      Real dk = 5.0,
                                      const std::vector<Real>& callStrikes = std::vector<Real>(),
                                      const std::vector<Real>& putStrikes = std::vector<Real>());
        void calculate() const override;

      protected:
        // helper methods
        void computeOptionWeights(const std::vector<Real>&,
                                  Option::Type,
                                  weights_type& optionWeights) const;
        Real computeLogPayoff(Real, Real) const;
        Real computeReplicatingPortfolio(
                                     const weights_type& optionWeights) const;
        Rate riskFreeRate() const;
        DiscountFactor riskFreeDiscount() const;
        Real underlying() const;
        Time residualTime() const;
      private:
        ext::shared_ptr<GeneralizedBlackScholesProcess> process_;
        Real dk_;
        std::vector<Real> callStrikes_, putStrikes_;
    };


    // inline definitions

    inline ReplicatingVarianceSwapEngine::ReplicatingVarianceSwapEngine(
        ext::shared_ptr<GeneralizedBlackScholesProcess> process,
        Real dk,
        const std::vector<Real>& callStrikes,
        const std::vector<Real>& putStrikes)
    : process_(std::move(process)), dk_(dk), callStrikes_(callStrikes), putStrikes_(putStrikes) {

        QL_REQUIRE(process_, "no process given");
        QL_REQUIRE(!callStrikes.empty() && !putStrikes.empty(),
                   "no strike(s) given");
        QL_REQUIRE(*std::min_element(putStrikes.begin(),putStrikes.end())>0.0,
                   "min put strike must be positive");
        QL_REQUIRE(*std::min_element(callStrikes.begin(), callStrikes.end())==
                   *std::max_element(putStrikes.begin(), putStrikes.end()),
                   "min call and max put strikes differ");
    }


    inline void ReplicatingVarianceSwapEngine::computeOptionWeights(
                                    const std::vector<Real>& availStrikes,
                                    const Option::Type type,

