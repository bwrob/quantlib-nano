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

#ifndef quantlib_gaussian_lhp_lossmodel_hpp
#define quantlib_gaussian_lhp_lossmodel_hpp

#include <ql/qldefines.hpp>

#ifndef QL_PATCH_SOLARIS

#include <ql/math/distributions/bivariatenormaldistribution.hpp>
#include <ql/experimental/credit/recoveryratequote.hpp>
#include <ql/quotes/simplequote.hpp>
#include <ql/experimental/credit/defaultlossmodel.hpp>
#include <ql/experimental/credit/basket.hpp>
#include <ql/experimental/math/latentmodel.hpp>
#include <functional>
#include <numeric>

/* Intended to replace GaussianLHPCDOEngine in
    ql/experimental/credit/syntheticcdoengines.hpp
   Moved from an engine to a loss model, CDO engines might refer to it.
*/

namespace QuantLib {

    /*!
      Portfolio loss model with analytical expected tranche loss for a large
      homogeneous pool with Gaussian one-factor copula. See for example
      "The Normal Inverse Gaussian Distribution for Synthetic CDO pricing.",
      Anna Kalemanova, Bernd Schmid, Ralf Werner,
      Journal of Derivatives, Vol. 14, No. 3, (Spring 2007), pp. 80-93.
      http://www.defaultrisk.com/pp_crdrv_91.htm

      It can be used to price a credit derivative or to provide risk metrics of
      a portfolio.

      \todo It should be checking that basket exposures are deterministic (fixed
      or programmed amortizing) otherwise the model is not fit for the basket.

      \todo Bugging on tranched baskets with upper limit over maximum
        attainable loss?
     */
    class GaussianLHPLossModel : public DefaultLossModel,
        public LatentModel<GaussianCopulaPolicy> {
    public:
        typedef GaussianCopulaPolicy copulaType;

        GaussianLHPLossModel(
            const Handle<Quote>& correlQuote,
            const std::vector<Handle<RecoveryRateQuote> >& quotes);

        GaussianLHPLossModel(
            Real correlation,
            const std::vector<Real>& recoveries);

        GaussianLHPLossModel(
            const Handle<Quote>& correlQuote,
            const std::vector<Real>& recoveries);

        void update() override {
            sqrt1minuscorrel_ = std::sqrt(1.-correl_->value());
            beta_ = std::sqrt(correl_->value());
            biphi_ = BivariateCumulativeNormalDistribution(
                -beta_);
            // tell basket to notify instruments, etc, we are invalid
            if(!basket_.empty()) basket_->notifyObservers();
        }

    private:
      void resetModel() override {}
      /*! @param attachLimit as a fraction of the underlying live portfolio
      notional
      */
      Real expectedTrancheLossImpl(Real remainingNot, // << at the given date 'd'
                                   Real prob,         // << at the given date 'd'
                                   Real averageRR,    // << at the given date 'd'
                                   Real attachLimit,
                                   Real detachLimit) const;
    public:
      Real expectedTrancheLoss(const Date& d) const override {
          // can calls to Basket::remainingNotional(d) be cached?<<<<<<<<<<<<<
          const Real remainingfullNot = basket_->remainingNotional(d);
          Real averageRR = ave
