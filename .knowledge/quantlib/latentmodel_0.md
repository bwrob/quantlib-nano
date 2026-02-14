/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Roland Lichters
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

#ifndef quantlib_latent_model_hpp
#define quantlib_latent_model_hpp

#include <ql/experimental/math/multidimquadrature.hpp>
#include <ql/experimental/math/multidimintegrator.hpp>
#include <ql/math/integrals/trapezoidintegral.hpp>
#include <ql/math/randomnumbers/randomsequencegenerator.hpp>
#include <ql/experimental/math/gaussiancopulapolicy.hpp>
#include <ql/experimental/math/tcopulapolicy.hpp>
#include <ql/math/randomnumbers/boxmullergaussianrng.hpp>
#include <ql/experimental/math/polarstudenttrng.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <vector>

/*! \file latentmodel.hpp
    \brief Generic multifactor latent variable model.
*/

namespace QuantLib {

    namespace detail {
        // havent figured out how to do this in-place
        struct multiplyV {
            std::vector<Real> operator()(Real d, std::vector<Real> v) 
            {
                std::transform(v.begin(), v.end(), v.begin(), 
                               [=](Real x) -> Real { return x * d; });
                return v;
            }
        };
    }

    //! \name Latent model direct integration facility.
    //@{
    /* Things trying to achieve here:
    1.- Unify the two branches of integrators in the library, they do not 
      hang from a common base class and here a common ptr for the 
      factory is needed.
    2.- Have a common signature for the integration call.
    3.- Factory construction so integrable latent models can choose the 
      integration algorithm separately.
    */
    class LMIntegration {
    public:
        // Interface with actual integrators:
        // integral of a scalar function
        virtual Real integrate(const std::function<Real (
            const std::vector<Real>& arg)>& f) const = 0;
        // integral of a vector function
        /* I had to use a different name, since the compiler does not
        recognise the overload; MSVC sees the argument as 
        std::function<Signature> in both cases....   
        I could do the as with the quadratures and have this as a template 
        function and spez for the vector case but I prefer to understand
        why the overload fails....
                    FIX ME
        */
        virtual std::vector<Real> integrateV(
            const std::function<std::vector<Real>  (
            const std::vector<Real>& arg)>& f) const {
            QL_FAIL("No vector integration provided");
        }
        virtual ~LMIntegration() = default;
    };

    //CRTP-ish for joining the integrations, class above to have the factory
    template <class I_T>
    class IntegrationBase : 
        public I_T, public LMIntegration {// diamond on 'integrate'
     // this class template always to be fully specialized:
     private:
       IntegrationBase() = default;
    };
    //@}
    
    // gcc reports value collision with heston engine (?!) thats why the name
    namespace LatentModelIntegrationType {
        typedef 
        enum LatentModelIntegrationType {
            #ifndef QL_PATCH_SOLARIS
            GaussianQuadrature,
            #endif
            Trapezoid
            // etc....
        } LatentModelIntegrationType;
    }

 