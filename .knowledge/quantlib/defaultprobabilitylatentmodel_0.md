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

#ifndef quantlib_default_latent_model_hpp
#define quantlib_default_latent_model_hpp

#include <ql/experimental/credit/basket.hpp>
#include <ql/experimental/math/latentmodel.hpp>
#include <ql/experimental/math/gaussiancopulapolicy.hpp>
#include <boost/dynamic_bitset.hpp>

namespace QuantLib {

    /*! \brief Default event Latent Model.

     This is a model for joint default events based on a generic Latent
      Model. It models solely the default events in a portfolio, not making any
      reference to severities, exposures, etc...
     An implicit correspondence is stablished between the variables modelled and
     the names in the basket given by the basket and model variable access
     indices.
     The class is parametric on the Latent Model copula.

     \todo Consider QL_REQUIRE(basket_, "No portfolio basket set.") test in
     debug model only for performance reasons.
    */
    template<class copulaPolicy>
    class DefaultLatentModel : public LatentModel<copulaPolicy> {
        // import template members
    protected:
        using LatentModel<copulaPolicy>::factorWeights_;
        using LatentModel<copulaPolicy>::idiosyncFctrs_;
        using LatentModel<copulaPolicy>::copula_;
    public:
        using LatentModel<copulaPolicy>::inverseCumulativeY;
        using LatentModel<copulaPolicy>::cumulativeZ;
        using LatentModel<copulaPolicy>::integratedExpectedValue;// which one?
    protected:
        // not a handle, the model doesnt keep any cached magnitudes, no need
        //  for notifications, still...
        mutable ext::shared_ptr<Basket> basket_;
        ext::shared_ptr<LMIntegration> integration_;
    private:
        typedef typename copulaPolicy::initTraits initTraits;
    public:
        /*!
        @param factorWeights Latent model independent factors weights for each
            variable.
        @param integralType Integration type.
        @param ini Copula initialization if any.

        \warning Baskets with realized defaults not tested/WIP.
        */
        DefaultLatentModel(
            const std::vector<std::vector<Real> >& factorWeights,
            LatentModelIntegrationType::LatentModelIntegrationType integralType,
            const initTraits& ini = initTraits()
            )
        : LatentModel<copulaPolicy>(factorWeights, ini),
          integration_(LatentModel<copulaPolicy>::IntegrationFactory::
            createLMIntegration(factorWeights[0].size(), integralType))
        { }
        DefaultLatentModel(
            const Handle<Quote>& mktCorrel,
            Size nVariables,
            LatentModelIntegrationType::LatentModelIntegrationType integralType,
            const initTraits& ini = initTraits()
            )
        : LatentModel<copulaPolicy>(mktCorrel, nVariables, ini),
          integration_(LatentModel<copulaPolicy>::IntegrationFactory::
            createLMIntegration(1, integralType))
        { }
        /* \todo
            Add other constructors as in LatentModel for ease of use. (less
            dimensions, factors, etcc...)
        */

        /* To interface with loss models. It is possible to change the basket
        since there are no cached magnitudes.
        *