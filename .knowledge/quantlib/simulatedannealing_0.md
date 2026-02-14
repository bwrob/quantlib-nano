/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2013 Peter Caspers

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

/*! \file simulatedannealing.hpp
    \brief Numerical Recipes in C (second edition), Chapter 10.9,
           with the original exit criterion in f(x) replaced by one
           in x (see simplex.cpp for a reference to GSL concerning this)
*/

#ifndef quantlib_optimization_simulatedannealing_hpp
#define quantlib_optimization_simulatedannealing_hpp

#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <ql/math/optimization/problem.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <cmath>

namespace QuantLib {

    /*! Class RNG must implement the following interface:
        \code
            RNG::sample_type RNG::next() const;
        \endcode

        \ingroup optimizers
    */

    //! Simulated Annealing
    template <class RNG = MersenneTwisterUniformRng>
    class SimulatedAnnealing : public OptimizationMethod {

      public:

        enum Scheme {
            ConstantFactor,
            ConstantBudget
        };

        /*! reduce temperature T by a factor of \f$ (1-\epsilon) \f$ after m moves */
        SimulatedAnnealing(const Real lambda, const Real T0,
                           const Real epsilon, const Size m,
                           const RNG &rng = RNG())
            : scheme_(ConstantFactor), lambda_(lambda), T0_(T0),
              epsilon_(epsilon), alpha_(0.0), K_(0), rng_(rng), m_(m) {}

        /*! budget a total of K moves, set temperature T to the initial
          temperature times \f$ ( 1 - k/K )^\alpha \f$ with k being the total number
          of moves so far. After K moves the temperature is guaranteed to be
          zero, after that the optimization runs like a deterministic simplex
          algorithm.
        */
        SimulatedAnnealing(const Real lambda, const Real T0, const Size K,
                           const Real alpha, const RNG &rng = RNG())
            : scheme_(ConstantBudget), lambda_(lambda), T0_(T0), epsilon_(0.0),
              alpha_(alpha), K_(K), rng_(rng) {}

        EndCriteria::Type minimize(Problem& P, const EndCriteria& ec) override;

      private:

        const Scheme scheme_;
        const Real lambda_, T0_, epsilon_, alpha_;
        const Size K_;
        const RNG rng_;

        Real simplexSize();
        void amotsa(Problem &, Real);

        Real T_;
        std::vector<Array> vertices_;
        Array values_, sum_;
        Integer i_, ihi_, ilo_, j_, m_, n_;
        Real fac1_, fac2_, yflu_;
        Real rtol_, swap_, yhi_, ylo_, ynhi_, ysave_, yt_, ytry_, yb_, tt_;
        Array pb_, ptry_;
        Size iteration_, iterationT_;
    };

    template <class RNG>
    Real SimulatedAnnealing<RNG>::simplexSize() { // this is taken from
                                                  // simplex.cpp
        Array center(vertices_.front().size(), 0);
        for (auto& vertice : vertices_)
            center += vertice;
        center *= 1 / Real(vertices_.size());
        Real result = 0;
        for (auto& vertice : vertices_) {
            Array temp = vertice - center;
            result += Norm2(temp);
        }
        return result / Real(vertices_.size());
    }

    template <class RNG>
    void SimulatedAnnealing<RNG>::amotsa(Problem &P, Re
