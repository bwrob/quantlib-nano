/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008, 2016 Jose Aparicio
 Copyright (C) 2008 Chris Kenyon
 Copyright (C) 2008 Roland Lichters
 Copyright (C) 2008 StatPro Italia srl

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

/*! \file piecewisedefaultcurve.hpp
    \brief piecewise-interpolated default-probability structure
*/

#ifndef quantlib_piecewise_default_curve_hpp
#define quantlib_piecewise_default_curve_hpp

#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/credit/probabilitytraits.hpp>
#include <ql/termstructures/iterativebootstrap.hpp>
#include <utility>

namespace QuantLib {

    //! Piecewise default-probability term structure
    /*! This term structure is bootstrapped on a number of credit
        instruments which are passed as a vector of handles to
        DefaultProbabilityHelper instances. Their maturities mark the
        boundaries of the interpolated segments.

        Each segment is determined sequentially starting from the
        earliest period to the latest and is chosen so that the
        instrument whose maturity marks the end of such segment is
        correctly repriced on the curve.

        \warning The bootstrapping algorithm will raise an exception if
                 any two instruments have the same maturity date.
    */
    template <class Traits, class Interpolator,
              template <class> class Bootstrap = IterativeBootstrap>
    class PiecewiseDefaultCurve
        : public Traits::template curve<Interpolator>::type,
          public LazyObject {
      private:
        typedef typename Traits::template curve<Interpolator>::type base_curve;
        typedef PiecewiseDefaultCurve<Traits,Interpolator,Bootstrap> this_curve;
      public:
        typedef Traits traits_type;
        typedef Interpolator interpolator_type;
        typedef Bootstrap<this_curve> bootstrap_type;

        //! \name Constructors
        //@{
        PiecewiseDefaultCurve(
            const Date& referenceDate,
            std::vector<ext::shared_ptr<typename Traits::helper> > instruments,
            const DayCounter& dayCounter,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& i = {},
            bootstrap_type bootstrap = {})
        : base_curve(referenceDate, dayCounter, jumps, jumpDates, i),
          instruments_(std::move(instruments)), accuracy_(1.0e-12),
          bootstrap_(std::move(bootstrap)) {
            bootstrap_.setup(this);
        }

        PiecewiseDefaultCurve(
               const Date& referenceDate,
               const std::vector<ext::shared_ptr<typename Traits::helper> >&
                                                                  instruments,
               const DayCounter& dayCounter,
               const Interpolator& i,
               const bootstrap_type& bootstrap = bootstrap_type())
        : base_curve(referenceDate, dayCounter,
                     {}, {}, i),
          instruments_(instruments), accuracy_(1.0e-12), bootstrap_(bootstrap) {
            bootstrap_.setup(this);
        }

        PiecewiseDefaultCurve(const Date& referenceDate,
                              std::vector<ext::shared_ptr<typ