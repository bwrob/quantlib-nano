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

/*! \file hybridsimulatedannealing.hpp
\brief Implementation based on:
Very Fast Simulated Re-Annealing, Lester Ingber,
Mathl. Comput. Modelling, 967-973, 1989
*/

#ifndef quantlib_optimization_hybridsimulatedannealing_hpp
#define quantlib_optimization_hybridsimulatedannealing_hpp

#include <ql/experimental/math/hybridsimulatedannealingfunctors.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <ql/math/optimization/levenbergmarquardt.hpp>
#include <ql/math/optimization/problem.hpp>
#include <ql/shared_ptr.hpp>
#include <utility>

namespace QuantLib {

    /*! Method is fairly straightforward:
    1) Sampler provides a probability density (based on current value) for the parameters. Each
    iteration a new draw is made from it to find a new point
    2) Probability determines whether the new point, obtained from Sampler, is accepted or not
    3) Temperature is a schedule T(k) for the iteration k, which affects the Sampler and Probability
    4) Reannealing is a departure from the traditional Boltzmann Annealing method: it rescales
    the iteration k independently for each dimension so as to improve convergence

    The hybrid in the name is because one can provide it a local optimizer for use whenever any new
    best point is found or at every accepted point, in which case is used is chose by the user.

    Class Sampler must implement the following interface:
    \code
    void operator()(Array &newPoint, const Array &currentPoint, const Array &temp) const;
    \endcode
    Class Probability must implement the following interface:
    \code
    bool operator()(Real currentValue, Real newValue, const Array &temp) const;
    \endcode
    Class Temperature must implement the following interface:
    \code
    void operator()(Array &newTemp, const Array &currTemp, const Array &steps) const;
    \endcode
    Class Reannealing must implement the following interface:
    \code
    void operator()(Array & steps, const Array &currentPoint,
    Real aCurrentValue, const Array & currTemp) const;
    \endcode
    */
    template <class Sampler, class Probability, class Temperature, class Reannealing = ReannealingTrivial>
    class HybridSimulatedAnnealing : public OptimizationMethod {
      public:
        enum LocalOptimizeScheme {
            NoLocalOptimize,
            EveryNewPoint,
            EveryBestPoint
        };
        enum ResetScheme {
            NoResetScheme,
            ResetToBestPoint,
            ResetToOrigin
        };

        HybridSimulatedAnnealing(const Sampler& sampler,
                                 const Probability& probability,
                                 Temperature temperature,
                                 const Reannealing& reannealing = ReannealingTrivial(),
                                 Real startTemperature = 200.0,
                                 Real endTemperature = 0.01,
                                 Size reAnnealSteps = 50,
                                 ResetScheme resetScheme = ResetToBestPoint,
                                 Size resetSteps = 150,
                                 const ext::shared_ptr<OptimizationMethod>& localOptimizer =

