/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl

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

/*! \file solver1d.hpp
    \brief Abstract 1-D solver class
*/

#ifndef quantlib_solver1d_hpp
#define quantlib_solver1d_hpp

#include <ql/math/comparison.hpp>
#include <ql/utilities/null.hpp>
#include <ql/patterns/curiouslyrecurring.hpp>
#include <ql/errors.hpp>
#include <algorithm>
#include <iomanip>

namespace QuantLib {

    #define MAX_FUNCTION_EVALUATIONS 100

    //! Base class for 1-D solvers
    /*! The implementation of this class uses the so-called
        "Barton-Nackman trick", also known as "the curiously recurring
        template pattern". Concrete solvers will be declared as:
        \code
        class Foo : public Solver1D<Foo> {
          public:
            ...
            template <class F>
            Real solveImpl(const F& f, Real accuracy) const {
                ...
            }
        };
        \endcode
        Before calling <tt>solveImpl</tt>, the base class will set its
        protected data members so that:
        - <tt>xMin_</tt> and  <tt>xMax_</tt> form a valid bracket;
        - <tt>fxMin_</tt> and <tt>fxMax_</tt> contain the values of
          the function in <tt>xMin_</tt> and <tt>xMax_</tt>;
        - <tt>root_</tt> is a valid initial guess.
        The implementation of <tt>solveImpl</tt> can safely assume all
        of the above.

        \todo
        - clean up the interface so that it is clear whether the
          accuracy is specified for \f$ x \f$ or \f$ f(x) \f$.
        - add target value (now the target value is 0.0)
    */
    template <class Impl>
    class Solver1D : public CuriouslyRecurringTemplate<Impl> {
      public:
        Solver1D() = default;
        //! \name Modifiers
        //@{
        /*! This method returns the zero of the function \f$ f \f$,
            determined with the given accuracy \f$ \epsilon \f$;
            depending on the particular solver, this might mean that
            the returned \f$ x \f$ is such that \f$ |f(x)| < \epsilon
            \f$, or that \f$ |x-\xi| < \epsilon \f$ where \f$ \xi \f$
            is the real zero.

            This method contains a bracketing routine to which an
            initial guess must be supplied as well as a step used to
            scan the range of the possible bracketing values.
        */
        template <class F>
        Real solve(const F& f,
                   Real accuracy,
                   Real guess,
                   Real step) const {

            QL_REQUIRE(accuracy>0.0,
                       "accuracy (" << accuracy << ") must be positive");
            // check whether we really want to use epsilon
            accuracy = std::max(accuracy, QL_EPSILON);

            const Real growthFactor = 1.6;
            Integer flipflop = -1;

            root_ = guess;
            fxMax_ = f(root_);

            // monotonically crescent bias, as in optionValue(volatility)
            if (close(fxMax_,0.0))
                return root_;
            else if (fxMax_ > 0.0) {
                xMin_ = enforceBounds_(root_ - step);
                fxMin_ = f(xMin_);
                xMax_ = root_;
            } else {
                xMin_ = root_;
                fxMin_ = fxMax_;
              