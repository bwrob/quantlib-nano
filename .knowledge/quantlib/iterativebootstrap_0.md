/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008, 2011, 2015 Ferdinando Ametrano
 Copyright (C) 2007 Chris Kenyon
 Copyright (C) 2007 StatPro Italia srl
 Copyright (C) 2015 Paolo Mazzocchi

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

/*! \file iterativebootstrap.hpp
    \brief universal piecewise-term-structure boostrapper.
*/

#ifndef quantlib_iterative_bootstrap_hpp
#define quantlib_iterative_bootstrap_hpp

#include <ql/termstructures/bootstraphelper.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/math/solvers1d/finitedifferencenewtonsafe.hpp>
#include <ql/math/solvers1d/brent.hpp>
#include <ql/utilities/dataformatters.hpp>

namespace QuantLib {

namespace detail {

    /*! If \c dontThrow is \c true in IterativeBootstrap and on a given pillar the bootstrap fails when
        searching for a helper root between \c xMin and \c xMax, we use this function to return the value that
        gives the minimum absolute helper error in the interval between \c xMin and \c xMax inclusive.
    */
    template <class Fn>
    Real dontThrowFallback(const Fn& error, Real xMin, Real xMax, Size steps) {

        QL_REQUIRE(xMin < xMax, "Expected xMin to be less than xMax");

        // Set the initial value of the result to xMin and store the absolute bootstrap error at xMin
        Real result = xMin;
        Real absError = std::abs(error(xMin));
        Real minError = absError;

        // Step out to xMax
        Real stepSize = (xMax - xMin) / steps;
        for (Size i = 0; i < steps; i++) {

            // Get absolute bootstrap error at updated x value
            xMin += stepSize;
            absError = std::abs(error(xMin));

            // If this absolute bootstrap error is less than the minimum, update result and minError
            if (absError < minError) {
                result = xMin;
                minError = absError;
            }
        }

        return result;
    }

}

    //! Universal piecewise-term-structure boostrapper.
    template <class Curve>
    class IterativeBootstrap {
        typedef typename Curve::traits_type Traits;
        typedef typename Curve::interpolator_type Interpolator;
      public:
        /*! Constructor
            \param accuracy       Accuracy for the bootstrap stopping criterion. If it is set to
                                  \c Null<Real>(), its value is taken from the termstructure's accuracy.
            \param minValue       Allow to override the initial minimum value coming from traits.
            \param maxValue       Allow to override the initial maximum value coming from traits.
            \param maxAttempts    Number of attempts on each iteration. A number greater than 1 implies retries.
            \param maxFactor      Factor for max value retry on each iteration if there is a failure.
            \param minFactor      Factor for min value retry on each iteration if there is a failure.
            \param dontThrow      If set to \c true, the bootstrap doesn't throw and returns a <em>fall back</em>
                                  result.
            \param dontThrowSteps If \p dontThrow is \c true, this gives the number of steps to use when searching
                                  for a fallback curve pillar value that gives the minimum bootstrap help