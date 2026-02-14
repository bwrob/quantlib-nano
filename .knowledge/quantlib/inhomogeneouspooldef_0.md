/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Roland Lichters
 Copyright (C) 2009, 2014 Jose Aparicio

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

#ifndef quantlib_inhomogenous_pool_default_model_hpp
#define quantlib_inhomogenous_pool_default_model_hpp

#include <ql/experimental/credit/lossdistribution.hpp>
#include <ql/experimental/credit/basket.hpp>
#include <ql/experimental/credit/constantlosslatentmodel.hpp>
#include <ql/experimental/credit/defaultlossmodel.hpp>

// Intended to replace InhomogeneousPoolCDOEngine in syntheticcdoengines.hpp

namespace QuantLib {

    //-------------------------------------------------------------------------
    //! Default loss distribution convolution for finite non homogeneous pool
    /* A note on the number of buckets: As it is now the code goes splitting
    losses into buckets from loses equal to zero to losses up to the value of
    the underlying basket. This is in view of a stochastic loss given default
    but in a constant LGD situation this is a waste and it is more efficient to
    go up to the attainable losses.
    \todo Extend to the multifactor case for a generic LM
    \todo Many common code with the homogeneous version, both classes perform
    the same work on different loss distribution types, merge and send the
    distribution object?
    */
    template<class copulaPolicy>
    class InhomogeneousPoolLossModel : public DefaultLossModel {
    private:
      void resetModel() override;

    public:
        // allow base correlations:
        typedef copulaPolicy copulaType;

        InhomogeneousPoolLossModel(
        // restricted to non random recoveries, but it could be possible.
            const ext::shared_ptr<ConstantLossLatentmodel<copulaPolicy> >&
                copula,
            Size nBuckets,
            Real max = 5.,
            Real min = -5.,
            Size nSteps = 50)
        : copula_(copula),
          nBuckets_(nBuckets),
          max_(max), min_(min), nSteps_(nSteps), delta_((max - min)/nSteps)
        {
            QL_REQUIRE(copula->numFactors() == 1,
                "Inhomogeneous model not implemented for multifactor");
        }
    // Write another constructor sending the LM factors and recoveries.
    protected:
        Distribution lossDistrib(const Date& d) const;
    public:
      Real expectedTrancheLoss(const Date& d) const override {
          return lossDistrib(d).cumulativeExcessProbability(attachAmount_, detachAmount_);
          // This one if the distribution is over the whole loss structure:
          // but it becomes very expensive
          /*
          return lossDistrib(d).trancheExpectedValue(
              attachAmount_, detachAmount_);
          */
      }
      Real percentile(const Date& d, Real percentile) const override {
          Real portfLoss = lossDistrib(d).confidenceLevel(percentile);
          return std::min(std::max(portfLoss - attachAmount_, 0.), detachAmount_ - attachAmount_);
      }
      Real expectedShortfall(const Date& d, Probability percentile) const override {
          Distribution dist = lossDistrib(d);
          dist.tranche(attachAmount_, detachAmount_);
          return dist.expectedShortfall(percentile);
      }

    protected:
        const ext::shared_ptr<ConstantLossLatentmodel<copulaPolicy>
