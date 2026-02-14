/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2014 Jose Aparicio

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

#ifndef quantlib_binomial_loss_model_hpp
#define quantlib_binomial_loss_model_hpp

#include <ql/experimental/credit/basket.hpp>
#include <ql/experimental/credit/constantlosslatentmodel.hpp>
#include <ql/experimental/credit/defaultlossmodel.hpp>
#include <ql/handle.hpp>
#include <algorithm>
#include <numeric>
#include <utility>

namespace QuantLib {

    /*! Binomial Defaultable Basket Loss Model\par
    Models the portfolio loss distribution by approximatting it to an adjusted 
    binomial. Fits the two moments of the loss distribution through an adapted 
    binomial approximation. This simple model allows for portfolio inhomogeneity
    with no excesive cost over the LHP.\par
    See:\par
    <b>Approximating Independent Loss Distributions with an Adjusted Binomial 
    Distribution</b> , Dominic O'Kane, 2007 EDHEC RISK AND ASSET MANAGEMENT 
    RESEARCH CENTRE \par
    <b>Modelling single name and multi-name credit derivatives</b> Chapter 
    18.5.2, Dominic O'Kane, Wiley Finance, 2008 \par
    The version presented here is adaptated to the multifactorial case
    by computing a conditional binomial approximation; notice that the Binomial
    is stable. This way the model can be used also in risk management models
    rather than only in pricing. The copula is also left 
    undefined/arbitrary. \par
    LLM: Loss Latent Model template parameter able to model default and 
    loss.\par
    The model is allowed and arbitrary copula, although initially designed for
    a Gaussian setup. If these exotic versions were not allowed the template 
    parameter can then be dropped but the use of random recoveries should be
    added in some other way.

    \todo untested/wip for the random recovery models.
    \todo integrate with the previously computed probability inversions of
    the cumulative functions.
    */
    template<class LLM>
    class BinomialLossModel : public DefaultLossModel {
    public:
        typedef typename LLM::copulaType copulaType;
        explicit BinomialLossModel(ext::shared_ptr<LLM> copula) : copula_(std::move(copula)) {}

      private:
        void resetModel() override {
            /* say there are defaults and these havent settled... and this is
            the engine to compute them.... is this the wrong place?:*/
            attachAmount_ = basket_->remainingAttachmentAmount();
            detachAmount_ = basket_->remainingDetachmentAmount();

            copula_->resetBasket(basket_.currentLink()); // forces interface
      }

    protected:
        /*! Returns the probability of the default loss values given by the 
            method lossPoints.
        */
        std::vector<Real> expectedDistribution(const Date& date) const {
            // precal date conditional magnitudes:
            std::vector<Real> notionals = basket_->remainingNotionals(date);
            std::vector<Probability> invProbs = 
                basket_->remainingProbabilities(date);
            for(Size iName=0; iName<invProbs.size(); iName++)
                invProbs[iName] = 
                    copula_->inverseCumulativeY(invProbs[iName], iName);

            return copula_->integratedExpectedValueV(
                [&](cons