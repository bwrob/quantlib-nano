/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2005 Klaus Spanderen
 Copyright (C) 2005 Gary Kennedy

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

/*! \file gaussianquadratures.hpp
    \brief Integral of a 1-dimensional function using the Gauss quadratures
*/

#ifndef quantlib_gaussian_quadratures_hpp
#define quantlib_gaussian_quadratures_hpp

#include <ql/math/array.hpp>
#include <ql/math/integrals/integral.hpp>
#include <ql/math/integrals/gaussianorthogonalpolynomial.hpp>

namespace QuantLib {
    class GaussianOrthogonalPolynomial;

    //! Integral of a 1-dimensional function using the Gauss quadratures method
    /*! References:
        Gauss quadratures and orthogonal polynomials

        G.H. Gloub and J.H. Welsch: Calculation of Gauss quadrature rule.
        Math. Comput. 23 (1986), 221-230

        "Numerical Recipes in C", 2nd edition,
        Press, Teukolsky, Vetterling, Flannery,

        \test the correctness of the result is tested by checking it
              against known good values.
    */
    class GaussianQuadrature {
      public:
        GaussianQuadrature(Size n,
                           const GaussianOrthogonalPolynomial& p);

#if defined(__GNUC__) && (__GNUC__ >= 7)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wnoexcept-type"
#endif

        template <class F>
        Real operator()(const F& f) const {
            Real sum = 0.0;
            for (Integer i = Integer(order())-1; i >= 0; --i) {
                sum += w_[i] * f(x_[i]);
            }
            return sum;
        }

#if defined(__GNUC__) && (__GNUC__ >= 7)
#pragma GCC diagnostic pop
#endif

        Size order() const { return x_.size(); }
        const Array& weights() { return w_; }
        const Array& x()       { return x_; }

      protected:
        Array x_, w_;
    };

    class MultiDimGaussianIntegration {
      public:
        MultiDimGaussianIntegration(
            const std::vector<Size>& ns,
            const std::function<ext::shared_ptr<GaussianQuadrature>(Size)>& genQuad);

        Real operator()(const std::function<Real(Array)>& f) const;

        const Array& weights() const { return weights_; }
        const std::vector<Array>& x() const { return x_; }

      private:
        Array weights_;
        std::vector<Array> x_;
    };


    //! generalized Gauss-Laguerre integration
    /*! This class performs a 1-dimensional Gauss-Laguerre integration.
        \f[
        \int_{0}^{\inf} f(x) \mathrm{d}x
        \f]
        The weighting function is
        \f[
            w(x;s)=x^s \exp{-x}
        \f]
        and \f[ s > -1 \f]
    */
    class GaussLaguerreIntegration : public GaussianQuadrature {
      public:
        explicit GaussLaguerreIntegration(Size n, Real s = 0.0)
        : GaussianQuadrature(n, GaussLaguerrePolynomial(s)) {}
    };

    //! generalized Gauss-Hermite integration
    /*! This class performs a 1-dimensional Gauss-Hermite integration.
        \f[
        \int_{-\inf}^{\inf} f(x) \mathrm{d}x
        \f]
        The weighting function is
        \f[
            w(x;\mu)=|x|^{2\mu} \exp{-x*x}
        \f]
        and \f[ \mu > -0.5 \f]
    */
    class GaussHermiteIntegration : public GaussianQuadrature {
      public:
        explicit GaussHermiteIntegration(Size n, Real mu = 0.0)

