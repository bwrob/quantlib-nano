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

/*! \file fireflyalgorithm.hpp
\brief Implementation based on:
Yang, Xin-She (2009) Firefly Algorithm, Levy Flights and Global
Optimization. Research and Development in Intelligent Systems XXVI, pp 209-218.
http://arxiv.org/pdf/1003.1464.pdf
*/

#ifndef quantlib_optimization_fireflyalgorithm_hpp
#define quantlib_optimization_fireflyalgorithm_hpp

#include <ql/math/optimization/problem.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <ql/experimental/math/isotropicrandomwalk.hpp>
#include <ql/experimental/math/levyflightdistribution.hpp>
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <ql/math/randomnumbers/seedgenerator.hpp>

#include <cmath>
#include <random>

namespace QuantLib {

    /*! The main process is as follows:
    M individuals are used to explore the N-dimensional parameter space:
    \f$ X_{i}^k = (X_{i, 1}^k, X_{i, 2}^k, \ldots, X_{i, N}^k) \f$ is the kth-iteration 
    for the ith-individual. X is updated via the rule
    \f[
    X_{i, j}^{k+1} = X_{i, j}^k + I(X^k)_{i,j} + RandomWalk_{i,j}^k
    \f]

    The intensity function I(X) should be monotonic
    The optimization stops either because the number of iterations has been reached
    or because the stationary function value limit has been reached.

    The current implementation extends the normal Firefly Algorithm with a 
    differential evolution (DE) optimizer according to:
    Afnizanfaizal Abdullah, et al. "A New Hybrid Firefly Algorithm for Complex and 
    Nonlinear Problem". Volume 151 of the series Advances in Intelligent and Soft 
    Computing pp 673-680, 2012.
    http://link.springer.com/chapter/10.1007%2F978-3-642-28765-7_81
    
    In effect this implementation provides a fully fledged DE global optimizer 
    as well. The Firefly Algorithm was easy to combine with DE because it already 
    contained a step where the current solutions are sorted. The population is 
    then divided into two subpopulations based on their order. The subpopulation 
    with the best results are updated via the firefly algorithm. The worse 
    subpopulation is updated via the DE operator:
    \f[
    Y^{k+1} = X_{best}^k + F(X_{r1}^k - X_{r2}^k)
    \f]
    and 
    \f[
    X_{i,j}^{k+1} = Y_{i,j}^{k+1}\ \text{if} R_{i,j} <= C
    \f]
    \f[
    X_{i,j}^{k+1} = X_{i,j}^{k+1}\ \text{otherwise}
    \f]
    where C is the crossover constant, and R is a random uniformly distributed
    number.
    */
    class FireflyAlgorithm : public OptimizationMethod {
      public:
        class RandomWalk;
        class Intensity;
        FireflyAlgorithm(Size M,
                         ext::shared_ptr<Intensity> intensity,
                         ext::shared_ptr<RandomWalk> randomWalk,
                         Size Mde = 0,
                         Real mutationFactor = 1.0,
                         Real crossoverFactor = 0.5,
                         unsigned long seed = SeedGenerator::instance().get());
        void startState(Problem &P, const EndCriteria &endCriteria);
        EndCriteria::Type minimize(Problem& P, const EndCriteria& endCriteria) override;

      protected:
        std::vector<Array> x_, xI_, xRW_; 
        std::vector<std::pair<Real, Size