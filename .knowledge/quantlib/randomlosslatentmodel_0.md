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
#ifndef quantlib_randomloss_latent_model_hpp
#define quantlib_randomloss_latent_model_hpp

#include <ql/experimental/credit/basket.hpp>
#include <ql/experimental/credit/randomdefaultlatentmodel.hpp>
#include <ql/experimental/credit/spotlosslatentmodel.hpp> 
#include <ql/experimental/math/gaussiancopulapolicy.hpp>
#include <ql/experimental/math/latentmodel.hpp>
#include <ql/experimental/math/tcopulapolicy.hpp>
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <ql/math/solvers1d/brent.hpp>
#include <cmath>

namespace QuantLib {


    template<class , class > class RandomLossLM;
    template<class copulaPolicy, class USNG>
        struct simEvent<RandomLossLM<copulaPolicy, USNG> > {
            simEvent(unsigned int n, unsigned int d, Real r) 
            : nameIdx(n), dayFromRef(d), 
                // truncates the value:
              compactRR(std::lround(r/rrGranular)) {}
            unsigned int nameIdx : 12; // can index up to 4095 names
            unsigned int dayFromRef : 12; // can index up to 4095 days = 11 yrs
        private:
            unsigned int compactRR : 8;
        public:
            // ..............still one bit left
            bool operator<(const simEvent& evt) const {
                return dayFromRef < evt.dayFromRef; 
            }
            Real recovery() const {
                /* we pay the price of this product (plus the division at 
                construction) for the memory we save. Precission is lost though,
                e.g. figures from 0.0 to 0.00390625/2. are stored as 0.0
                */
                return rrGranular * compactRR;
            }
            static const Real rrGranular;// = 1./256.;// 2^8
    };

#ifndef __DOXYGEN__

    template <class C, class G> const Real 
        simEvent<RandomLossLM<C, G> >::rrGranular = 1./256.;// 2^8

#endif

    /*! Random spot recovery rate loss model simulation for an arbitrary copula.
    */
    template<class copulaPolicy, class USNG = SobolRsg>
    class RandomLossLM : public RandomLM<RandomLossLM, copulaPolicy, USNG>
    {
    private:
        typedef simEvent<RandomLossLM> defaultSimEvent;

        const ext::shared_ptr<SpotRecoveryLatentModel<copulaPolicy> > copula_;
        // for time inversion:
        Real accuracy_;
    public:
        explicit RandomLossLM(
            const ext::shared_ptr<SpotRecoveryLatentModel<copulaPolicy> >& 
                copula,
            Size nSims = 0,
            Real accuracy = 1.e-6, 
            BigNatural seed = 2863311530UL)
        : RandomLM< ::QuantLib::RandomLossLM, copulaPolicy, USNG>
            (copula->numFactors(), copula->size(), copula->copula(), 
                nSims, seed),
          copula_(copula), accuracy_(accuracy)
    {
        // redundant through basket?
        this->registerWith(Settings::instance().evaluationDate());
    }

        // grant access to static polymorphism:
        /* While this works on g++, VC9 refuses to compile it.
        Not completely sure whos right; individually making friends of the 
        calling members or writing explicitly the derived class T parameters 
        throws the same errors.
        The access is then open to the m