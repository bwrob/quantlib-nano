/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2005, 2007 StatPro Italia srl
 Copyright (C) 2011 Ferdinando Ametrano
 Copyright (C) 2007 Chris Kenyon
 Copyright (C) 2019 SoftSolutions! S.r.l.

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

/*! \file bootstraptraits.hpp
    \brief bootstrap traits
*/

#ifndef ql_bootstrap_traits_hpp
#define ql_bootstrap_traits_hpp

#include <ql/termstructures/yield/discountcurve.hpp>
#include <ql/termstructures/yield/zerocurve.hpp>
#include <ql/termstructures/yield/interpolatedsimplezerocurve.hpp>
#include <ql/termstructures/yield/forwardcurve.hpp>
#include <ql/termstructures/bootstraphelper.hpp>

namespace QuantLib {

    namespace detail {
        const Real avgRate = 0.05;
        const Real maxRate = 1.0;
    }

    //! Discount-curve traits
    struct Discount {
        // interpolated curve type
        template <class Interpolator>
        struct curve {
            typedef InterpolatedDiscountCurve<Interpolator> type;
        };
        // helper class
        typedef BootstrapHelper<YieldTermStructure> helper;

        // start of curve data
        static Date initialDate(const YieldTermStructure* c) {
            return c->referenceDate();
        }
        // value at reference date
        static Real initialValue(const YieldTermStructure*) {
            return 1.0;
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
                return 1.0/(1.0+detail::avgRate*c->times()[1]);

            // flat rate extrapolation
            Real r = -std::log(c->data()[i-1])/c->times()[i-1];
            return std::exp(-r * c->times()[i]);
        }

        // possible constraints based on previous values
        template <class C>
        static Real minValueAfter(Size i,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            if (validData) {
                return *(std::min_element(c->data().begin(),
                                          c->data().end()))/2.0;
            }
            Time dt = c->times()[i] - c->times()[i-1];
            return c->data()[i-1] * std::exp(- detail::maxRate * dt);
        }
        template <class C>
        static Real maxValueAfter(Size i,
                                  const C* c,
                                  bool validData,
                                  Size) // firstAliveHelper
        {
            Time dt = c->times()[i] - c->times()[i-1];
            return c->data()[i-1] * std::exp(detail::maxRate * dt);
        }

        // transformation to add constraints to an unconstrained optimization
        template <class C>
        static Real transformDirect(Real x, Size i, const C* c)
        {
            return std::exp(x);
        }
        template <class C>
        static Real transformInverse(Real x, Size i, const C* c)
        {
            return std::log(x);
        }

        // root-finding update
        static void up