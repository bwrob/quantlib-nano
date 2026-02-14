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

#ifndef quantlib_spotlosslatentmodel_hpp
#define quantlib_spotlosslatentmodel_hpp

#include <ql/experimental/credit/defaultprobabilitylatentmodel.hpp>

namespace QuantLib {

    /*! \brief Random spot recovery rate latent variable portfolio model.\par
    See: \par
    <b>A Spot Stochastic Recovery Extension of the Gaussian Copula</b> N.Bennani
         and J.Maetz, MPRA July 2009 \par
    <b>Extension of Spot Recovery model for Gaussian Copula</b> H.Li, October
        2009,  MPRA \par
    The model is adpated here for a multifactor set up and a generic copula so 
    it can be used for pricing in single factor mode or for risk metrics in its
    multifactor version.\par
    \todo Rewrite this model: the distribution of the spot recovery given
    default could be given as a functional of rr_i with the market factors and
    the rest of methods depend on this. That would offer a family of models.
    \todo Implement eq. 45 to have the EL(t) and be able to integrate the model
    */
    template <class copulaPolicy>
    class SpotRecoveryLatentModel : public LatentModel<copulaPolicy> {
    public:
        // resolve LM interface:
        using LatentModel<copulaPolicy>::factorWeights;
        using LatentModel<copulaPolicy>::inverseCumulativeY;
        using LatentModel<copulaPolicy>::cumulativeY;
        using LatentModel<copulaPolicy>::latentVarValue;
        using LatentModel<copulaPolicy>::integratedExpectedValue;
    private:
        const std::vector<Real> recoveries_;
        const Real modelA_;
        // products of default and recoveries factors, see refs ('covariances')
        std::vector<Real> crossIdiosyncFctrs_;
        mutable Size numNames_;
        mutable ext::shared_ptr<Basket> basket_;
        ext::shared_ptr<LMIntegration> integration_;
    protected:
        //! access to integration:
      const ext::shared_ptr<LMIntegration>& integration() const override { return integration_; }

    private:
        typedef typename copulaPolicy::initTraits initTraits;
    public:
        SpotRecoveryLatentModel(
            const std::vector<std::vector<Real> >& factorWeights,
            const std::vector<Real>& recoveries,
            Real modelA,
            LatentModelIntegrationType::LatentModelIntegrationType integralType,
            const initTraits& ini = initTraits()
            );

        void resetBasket(const ext::shared_ptr<Basket>& basket) const;
        Probability conditionalDefaultProbability(const Date& date, Size iName,
            const std::vector<Real>& mktFactors) const;
        Probability conditionalDefaultProbability(Probability prob, Size iName,
            const std::vector<Real>& mktFactors) const;
        Probability conditionalDefaultProbabilityInvP(Real invCumYProb, 
            Size iName, 
            const std::vector<Real>& m) const;
        /*! Expected conditional spot recovery rate. Conditional on a set of 
        systemic factors and default returns the integrated attainable recovery 
        values. \par
        Corresponds to a multifactor generalization of the model in eq. 44 
        on p.15 of <b>Extension of Spot Recovery Model for Gaussian Copula</b> 
        Hui Li. 2009  Only 