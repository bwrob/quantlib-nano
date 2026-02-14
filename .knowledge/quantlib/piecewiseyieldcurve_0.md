/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2005, 2006, 2007, 2008 StatPro Italia srl
 Copyright (C) 2007, 2008, 2009 Ferdinando Ametrano
 Copyright (C) 2007 Chris Kenyon

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

/*! \file piecewiseyieldcurve.hpp
    \brief piecewise-interpolated term structure
*/

#ifndef quantlib_piecewise_yield_curve_hpp
#define quantlib_piecewise_yield_curve_hpp

#include <ql/patterns/lazyobject.hpp>
#include <ql/termstructures/iterativebootstrap.hpp>
#include <ql/termstructures/globalbootstrap.hpp>
#include <ql/termstructures/multicurve.hpp>
#include <ql/termstructures/yield/bootstraptraits.hpp>
#include <utility>

namespace QuantLib {

    //! Piecewise yield term structure
    /*! This term structure is bootstrapped on a number of interest
        rate instruments which are passed as a vector of pointers to
        RateHelper instances. Their maturities mark the boundaries of
        the interpolated segments.

        Each segment is determined sequentially starting from the
        earliest period to the latest and is chosen so that the
        instrument whose maturity marks the end of such segment is
        correctly repriced on the curve.

        \warning The bootstrapping algorithm will raise an exception if
                 any two instruments have the same maturity date.

        \ingroup yieldtermstructures

        \test
        - the correctness of the returned values is tested by
          checking them against the original inputs.
        - the observability of the term structure is tested.
    */
    template <class Traits, class Interpolator,
              template <class> class Bootstrap = IterativeBootstrap>
    class PiecewiseYieldCurve
        : public Traits::template curve<Interpolator>::type,
          public LazyObject,
          public MultiCurveBootstrapProvider {
      private:
        typedef typename Traits::template curve<Interpolator>::type base_curve;
        typedef PiecewiseYieldCurve<Traits,Interpolator,Bootstrap> this_curve;
      public:
        typedef Traits traits_type;
        typedef Interpolator interpolator_type;
        typedef Bootstrap<this_curve> bootstrap_type;

        //! \name Constructors
        //@{
        PiecewiseYieldCurve(
            const Date& referenceDate,
            std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
            const DayCounter& dayCounter,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& i = {},
            bootstrap_type bootstrap = {})
        : PiecewiseYieldCurve(std::move(instruments), std::move(bootstrap),
                              referenceDate, dayCounter, jumps, jumpDates, i) {}

        PiecewiseYieldCurve(const Date& referenceDate,
                            std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
                            const DayCounter& dayCounter,
                            const Interpolator& i,
                            bootstrap_type bootstrap = {})
        : PiecewiseYieldCurve(std::move(instruments), std::move(bootstrap),
                              referenceDate, dayCounter,
                              std::vector<Handle<Quote>>(), std::vector<Date>(), i) {}
