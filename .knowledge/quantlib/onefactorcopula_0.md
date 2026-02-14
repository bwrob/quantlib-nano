/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Roland Lichters

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

/*! \file onefactorcopula.hpp
    \brief One-factor copula base class
*/

#ifndef quantlib_one_factor_copula_hpp
#define quantlib_one_factor_copula_hpp

#include <ql/experimental/credit/distribution.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/quote.hpp>
#include <utility>

namespace QuantLib {

    //! Abstract base class for one-factor copula models
    /*! Reference: John Hull and Alan White, The Perfect Copula, June 2006

        Let \f$Q_i(t)\f$ be the cumulative probability of default of
        counterparty i before time t.

        In a one-factor model, consider random variables
        \f[ Y_i = a_i\,M+\sqrt{1-a_i^2}\:Z_i \f]
        where \f$M\f$ and \f$Z_i\f$ have independent zero-mean
        unit-variance distributions and \f$-1\leq a_i \leq 1\f$.  The
        correlation between \f$Y_i\f$ and \f$Y_j\f$ is then
        \f$a_i a_j\f$.

        Let \f$F_Y(y)\f$ be the cumulative distribution function of \f$Y_i\f$.
        \f$y\f$ is mapped to \f$t\f$ such that percentiles match, i.e.
        \f$F_Y(y)=Q_i(t)\f$ or \f$y=F_Y^{-1}(Q_i(t))\f$.

        Now let \f$F_Z(z)\f$ be the cumulated distribution function of
        \f$Z_i\f$.  For given realization of \f$M\f$, this determines
        the distribution of \f$y\f$:
        \f[
        Prob \,(Y_i < y|M) = F_Z \left( \frac{y-a_i\,M}{\sqrt{1-a_i^2}}\right)
        \qquad
        \mbox{or}
        \qquad
        Prob \,(t_i < t|M) = F_Z \left( \frac{F_Y^{-1}(Q_i(t))-a_i\,M}
        {\sqrt{1-a_i^2}}
        \right)
        \f]

        The distribution functions of \f$ M, Z_i \f$ are specified in
        derived classes. The distribution function of \f$ Y \f$ is
        then given by the convolution
        \f[
        F_Y(y) = Prob\,(Y<y) = \int_{-\infty}^\infty\,\int_{-\infty}^{\infty}\:
        D_Z(z)\,D_M(m) \quad
        \Theta \left(y - a\,m - \sqrt{1-a^2}\,z\right)\,dm\,dz,
        \qquad
        \Theta (x) = \left\{
        \begin{array}{ll}
        1 & x \geq 0 \\
        0 & x < 0
        \end{array}\right.
        \f]
        where \f$ D_Z(z) \f$ and \f$ D_M(m) \f$ are the probability
        densities of \f$ Z\f$ and \f$ M, \f$ respectively.

        This convolution can also be written
        \f[
        F(y) = Prob \,(Y < y) =
        \int_{-\infty}^\infty D_M(m)\,dm\:
        \int_{-\infty}^{g(y,a,m)} D_Z(z)\,dz, \qquad
        g(y,a,m) = \frac{y - a\cdot m}{\sqrt{1-a^2}}, \qquad a < 1
        \f]

        or

        \f[
        F(y) = Prob \,(Y < y) =
        \int_{-\infty}^\infty D_Z(z)\,dz\:
        \int_{-\infty}^{h(y,a,z)} D_M(m)\,dm, \qquad
        h(y,a,z) = \frac{y - \sqrt{1 - a^2}\cdot z}{a}, \qquad a > 0.
        \f]

        In general, \f$ F_Y(y) \f$ needs to be computed numerically.

        \todo Improve on simple Euler integration
    */
    class OneFactorCopula : public LazyObject {
      public:
        OneFactorCopula(Handle<Quote> correlation,
                        Real maximum = 5.0,
                        Size integrationSteps = 50,
                        Real minimum = -5.0)
        : correlation_(std::move(correlation)), max_(maximum), steps_(integrationSteps),
          min_(minimum) {
            QL_REQUIRE(correlation_-