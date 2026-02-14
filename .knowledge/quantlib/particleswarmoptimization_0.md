/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
Copyright (C) 2015 Andres Hernandez

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

/*! \file particleswarmoptimization.hpp
\brief Implementation based on:
Clerc, M., Kennedy, J. (2002) The particle swarm-explosion, stability and
convergence in a multidimensional complex space. IEEE Transactions on Evolutionary
Computation, 6(2): 58–73.
*/

#ifndef quantlib_optimization_particleswarmoptimization_hpp
#define quantlib_optimization_particleswarmoptimization_hpp

#include <ql/math/optimization/problem.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <ql/experimental/math/isotropicrandomwalk.hpp>
#include <ql/experimental/math/levyflightdistribution.hpp>
#include <ql/math/randomnumbers/seedgenerator.hpp>

#include <random>

namespace QuantLib {

    /*! The process is as follows:
    M individuals are used to explore the N-dimensional parameter space:
    \f$ X_{i}^k = (X_{i, 1}^k, X_{i, 2}^k, \ldots, X_{i, N}^k) \f$ is the kth-iteration for the ith-individual.

    X is updated via the rule
    \f[
    X_{i, j}^{k+1} = X_{i, j}^k + V_{i, j}^{k+1}
    \f]
    with V being the "velocity" that updates the position:
    \f[
    V_{i, j}^{k+1} = \chi\left(V_{i, j}^k + c_1 r_{i, j}^k (P_{i, j}^k - X_{i, j}^k)
    + c_2 R_{i, j}^k (G_{i, j}^k - X_{i, j}^k)\right)
    \f]
    where c are constants, r and R are uniformly distributed random numbers in the range [0, 1], and
    \f$ P_{i, j} \f$ is the personal best parameter set for individual i up to iteration k
    \f$ G_{i, j} \f$ is the global best parameter set for the swarm up to iteration k.
    \f$ c_1 \f$ is the self recognition coefficient
    \f$ c_2 \f$ is the social recognition coefficient

    This version is known as the PSO with constriction factor (PSO-Co).
    PSO with inertia factor (PSO-In) updates the velocity according to:
    \f[
    V_{i, j}^{k+1} = \omega V_{i, j}^k + \hat{c}_1 r_{i, j}^k (P_{i, j}^k - X_{i, j}^k)
    + \hat{c}_2 R_{i, j}^k (G_{i, j}^k - X_{i, j}^k)
    \f]
    and is accessible from PSO-Co by setting \f$ \omega = \chi \f$,
    and \f$ \hat{c}_{1,2} = \chi c_{1,2} \f$.

    These two versions of PSO are normally referred to as canonical PSO.

    Convergence of PSO-Co is improved if \f$ \chi \f$ is chosen as
    \f$ \chi = \frac{2}{\vert 2-\phi-\sqrt{\phi^2 - 4\phi}\vert} \f$,
    with \f$ \phi = c_1 + c_2 \f$.
    Stable convergence is achieved if \f$ \phi >= 4 \f$. Clerc and Kennedy recommend
    \f$ c_1 = c_2 = 2.05 \f$ and \f$ \phi = 4.1 \f$.

    Different topologies can be chosen for G, e.g. instead of it being the best
    of the swarm, it is the best of the nearest neighbours, or some other form.

    In the canonical PSO, the inertia function is trivial. It is simply a
    constant (the inertia) multiplying the previous iteration's velocity. The
    value of the inertia constant determines the weight of a global search over
    local search. Like in the case of the topology, other possibilities for the
    inertia function are also possible, e.g. a function that interpolates between a
    high inertia at the beginning of the optimization (hence prioritizing a global
    search) and a low inertia towards the end of the optimization (hence prioritizing
    a local search).

    