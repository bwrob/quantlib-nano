/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Allen Kuo
 Copyright (C) 2010 Alessandro Roveda

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

/*! \file nonlinearfittingmethods.hpp
    \brief nonlinear methods to fit a bond discount function
*/

#ifndef quantlib_nonlinear_fitting_methods_hpp
#define quantlib_nonlinear_fitting_methods_hpp

#include <ql/termstructures/yield/fittedbonddiscountcurve.hpp>
#include <ql/math/interpolations/cubicinterpolation.hpp>
#include <ql/math/bspline.hpp>
#include <ql/shared_ptr.hpp>

namespace QuantLib {

    //! Exponential-splines fitting method
    /*! Fits a discount function to the exponential form
        \f[
        d(t) = \sum_{i=1}^9 c_i e^{-\kappa_i t}
        \f]
        where the constants \f$ c_i \f$ and \f$ \kappa \f$ are to be
        determined.  See:Li, B., E. DeWetering, G. Lucas, R. Brenner
        and A. Shapiro (2001): "Merrill Lynch Exponential Spline
        Model." Merrill Lynch Working Paper

        \f$ \kappa \f$ can be passed a fixed value, in which case it
        is excluded from optimization.

        \warning convergence may be slow
    */
    class ExponentialSplinesFitting
        : public FittedBondDiscountCurve::FittingMethod {
      public:
        ExponentialSplinesFitting(bool constrainAtZero = true,
                                  const Array& weights = Array(),
                                  const ext::shared_ptr<OptimizationMethod>& optimizationMethod = {},
                                  const Array& l2 = Array(),
                                  Real minCutoffTime = 0.0,
                                  Real maxCutoffTime = QL_MAX_REAL,
                                  Size numCoeffs = 9,
                                  Real fixedKappa = Null<Real>(),
                                  Constraint constraint = NoConstraint());
        ExponentialSplinesFitting(bool constrainAtZero,
                                  const Array& weights,
                                  const Array& l2,
                                  Real minCutoffTime = 0.0,
                                  Real maxCutoffTime = QL_MAX_REAL,
                                  Size numCoeffs = 9,
                                  Real fixedKappa = Null<Real>(),
                                  Constraint constraint = NoConstraint());
        ExponentialSplinesFitting(bool constrainAtZero, 
                                  Size numCoeffs, 
                                  Real fixedKappa, 
                                  const Array& weights = Array(),
                                  Constraint constraint = NoConstraint());


        std::unique_ptr<FittedBondDiscountCurve::FittingMethod> clone() const override;
      private:
        Natural numCoeffs_;
        Real fixedKappa_;
        Size size() const override;
        DiscountFactor discountFunction(const Array& x, Time t) const override;
    };


    //! Nelson-Siegel fitting method
    /*! Fits a discount function to the form
        \f$ d(t) = e^{-r t}, \f$ where the zero rate \f$r\f$ is defined as
        \f[
        r \equiv c_0 + (c_1 + c_2) \left( \frac{1 - e^{-\kappa t}}{\kappa t} \right) -
        c_2 e^{ - \kappa t}.
        \f]
        See: Nelson, C. and A. Siegel (1985): "Parsimonious modeling of yield
        curves