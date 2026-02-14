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

#ifndef quantlib_math_multidimquadrature_hpp
#define quantlib_math_multidimquadrature_hpp

#include <ql/qldefines.hpp>

/* Currently, this doesn't compile under Sun C++ (see
   https://github.com/lballabio/QuantLib/issues/223).  Until that's
   fixed, we disable it so that the rest of the library can be built.
*/

#ifndef QL_PATCH_SOLARIS

#include <ql/math/integrals/gaussianquadratures.hpp>
#include <functional>

namespace QuantLib {

    /*! \brief Integrates a vector or scalar function of vector domain. 
        
        A template recursion along dimensions avoids calling depth 
        test or virtual functions.

        \todo Add coherence test between the integrand function dimensions (the
        vector size) and the declared dimension in the constructor.

        \todo Split into integrator classes for functions returning scalar and 
            vector?
    */
    class GaussianQuadMultidimIntegrator {
    private:
        // Vector integration. Quadrature to functions returning a vector of 
        // real numbers, turns 1D quadratures into ND
        class VectorIntegrator : public GaussHermiteIntegration {
        public:
            explicit VectorIntegrator(Size n, Real mu = 0.0) 
            : GaussHermiteIntegration(n, mu) {}

            template <class F> // todo: fix copies.
            std::vector<Real> operator()(const F& f) const {
                //first one, we do not know the size of the vector returned by f
                Integer i = order()-1;
                std::vector<Real> term = f(x_[i]);// potential copy! @#$%^!!!
                std::for_each(term.begin(), term.end(),
                              [&](Real x) -> Real { return x * w_[i]; });
                std::vector<Real> sum = term;
           
                for (i--; i >= 0; --i) {
                    term = f(x_[i]);// potential copy! @#$%^!!!
                    // sum[j] += term[j] * w_[i];
                    std::transform(term.begin(), term.end(), sum.begin(), 
                                   sum.begin(),
                                   [&](Real x, Real y) -> Real { return w_[i]*x + y; });
                }
                return sum;
            }
        };

    public:
        /*!
            @param dimension The number of dimensions of the argument of the 
            function we want to integrate.
            @param quadOrder Quadrature order.
            @param mu Parameter in the Gauss Hermite weight (i.e. points load).
        */
        GaussianQuadMultidimIntegrator(Size dimension, Size quadOrder, 
            Real mu = 0.);
        //! Integration quadrature order.
        Size order() const {return integralV_.order();}

        //! Integrates function f over \f$ R^{dim} \f$
        /* This function is just syntax since the only thing it does is calling 
        to integrate<RetType> which has to exist for the type returned by the 
        function. So theres one redundant call but there should not be any extra 
        cost... up to the compiler. It can not be templated all the way since
        the integration entries functions can not be templates.
        Most times integrands will return a scalar or vector but could be 