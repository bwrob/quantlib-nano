/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Allen Kuo
 Copyright (C) 2009 Ferdinando Ametrano
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

/*! \file fittedbonddiscountcurve.hpp
    \brief discount curve fitted to a set of bonds
*/

#ifndef quantlib_fitted_bond_discount_curve_hpp
#define quantlib_fitted_bond_discount_curve_hpp

#include <ql/termstructures/yield/bondhelpers.hpp>
#include <ql/math/optimization/method.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/math/array.hpp>
#include <ql/utilities/clone.hpp>
#include <ql/math/optimization/constraint.hpp>

namespace QuantLib {

    //! Discount curve fitted to a set of fixed-coupon bonds
    /*! This class fits a discount function \f$ d(t) \f$ over a set of
        bonds, using a user defined fitting method. The discount
        function is fit in such a way so that all cashflows of all
        input bonds, when discounted using \f$ d(t) \f$, will
        reproduce the set of input bond prices in an optimized
        sense. Minimized price errors are weighted by the inverse of
        their respective bond duration.

        The FittedBondDiscountCurve class acts as a generic wrapper,
        while its inner class FittingMethod provides the
        implementation details. Developers thus need only derive new
        fitting methods from the latter.

        \warning The method can be slow if there are many bonds to
                 fit. Speed also depends on the particular choice of
                 fitting method chosen and its convergence properties
                 under optimization.  See also todo list for
                 BondDiscountCurveFittingMethod.

        \todo refactor the bond helper class so that it is pure
              virtual and returns a generic bond or its cash
              flows. Derived classes would include helpers for
              fixed-rate and zero-coupon bonds. In this way, both
              bonds and bills can be used to fit a discount curve
              using the exact same machinery. At present, only
              fixed-coupon bonds are supported. An even better way to
              move forward might be to get rate helpers to return
              cashflows, in which case this class could be used to fit
              any set of cash flows, not just bonds.

        \todo add more fitting diagnostics: smoothness, standard
              deviation, student-t test, etc. Generic smoothness
              method may be useful for smoothing splines fitting. See
              Fisher, M., D. Nychka and D. Zervos: "Fitting the term
              structure of interest rates with smoothing splines."
              Board of Governors of the Federal Reserve System,
              Federal Resere Board Working Paper, 95-1.

        \todo add extrapolation routines

        \ingroup yieldtermstructures
    */
    class FittedBondDiscountCurve : public YieldTermStructure,
                                    public LazyObject {
      public:
        class FittingMethod;

        //! \name Constructors
        //@{
        //! reference date based on current evaluation date
        FittedBondDiscountCurve(Natural settlementDays,
                                const Calendar& calendar,
                                std::vector<ex
