/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Chris Kenyon
 Copyright (C) 2011 Ferdinando Ametrano

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

/*! \file piecewiseyoyoptionletvolatility.hpp
    \brief piecewise yoy inflation volatility term structure
*/

#ifndef quantlib_piecewise_yoy_optionlet_volatility_hpp
#define quantlib_piecewise_yoy_optionlet_volatility_hpp

#include <ql/experimental/inflation/yoyinflationoptionletvolatilitystructure2.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/termstructures/iterativebootstrap.hpp>
#include <utility>

namespace QuantLib {

    //! traits for inflation-volatility bootstrap
    class YoYInflationVolatilityTraits {
      public:
        typedef BootstrapHelper<YoYOptionletVolatilitySurface> helper;

        // start of curve data
        static Date initialDate(const YoYOptionletVolatilitySurface *s) {
            return s->baseDate();
        }
        // value at reference date
        static Real initialValue(const YoYOptionletVolatilitySurface *s) {
            return s->baseLevel();  // REALLLYYYY important because
                                    // generally don't have a clue
                                    // what this should be - embodies
                                    // assumptions on early options
                                    // that are _not_ quoted
        }

        // guesses
        template <class C>
        static Real guess(Size i,
                          const C* c,
                          bool validData,
                          Size) // firstAliveHelper
        {
            if (validData) // previous iteration value
                return c->data()[i];

            if (i==1) // first pillar
                return 0.005;

            // could/should extrapolate
            return 0.002;
        }

        // constraints
        template <class C>
        static Real minValueAfter(Size i,
                                  const C* c,
                                  bool,
                                  Size) // firstAliveHelper
        {
            return std::max(0.0, c->data()[i-1] - 0.02); // vol cannot be negative
        }
        template <class C>
        static Real maxValueAfter(Size i,
                                  const C* c,
                                  bool,
                                  Size) // firstAliveHelper
        {
            return c->data()[i-1] + 0.02;
        }

        // root-finding update
        static void updateGuess(std::vector<Real> &vols,
                                Real level,
                                Size i) {
            vols[i] = level;
        }
        // upper bound for convergence loop
        static Size maxIterations() {return 25;}
    };


    //! Piecewise year-on-year inflation volatility term structure
    /*! We use a flat smile for bootstrapping at constant K.  Happily
        most of the work has already been done in the bootstrapping
        classes.  We only need to add special attention for the start
        where there is usually no data, only assumptions.
    */
    template <class Interpolator,
              template <class> class Bootstrap = IterativeBootstrap,
              class Traits = YoYInflationVolatilityTraits>
    class PiecewiseYoYOptionletVolatili
