/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2001, 2002, 2003 Nicolas Di Césaré
 Copyright (C) 2004, 2008, 2009, 2011 Ferdinando Ametrano
 Copyright (C) 2009 Sylvain Bertrand
 Copyright (C) 2013 Peter Caspers
 Copyright (C) 2016 Nicholas Bertocchi

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

/*! \file cubicinterpolation.hpp
    \brief cubic interpolation between discrete points
*/

#ifndef quantlib_cubic_interpolation_hpp
#define quantlib_cubic_interpolation_hpp

#include <algorithm>
#include <ql/math/matrix.hpp>
#include <ql/math/interpolation.hpp>
#include <ql/methods/finitedifferences/tridiagonaloperator.hpp>
#include <vector>

namespace QuantLib {

    namespace detail {

        class CoefficientHolder {
          public:
            explicit CoefficientHolder(Size n)
            : n_(n), primitiveConst_(n-1), a_(n-1), b_(n-1), c_(n-1),
              monotonicityAdjustments_(n) {}
            virtual ~CoefficientHolder() = default;
            Size n_;
            // P[i](x) = y[i] +
            //           a[i]*(x-x[i]) +
            //           b[i]*(x-x[i])^2 +
            //           c[i]*(x-x[i])^3
            std::vector<Real> primitiveConst_, a_, b_, c_;
            std::vector<bool> monotonicityAdjustments_;
        };

        template <class I1, class I2> class CubicInterpolationImpl;

    }

    //! %Cubic interpolation between discrete points.
    /*! Cubic interpolation is fully defined when the ${f_i}$ function values
        at points ${x_i}$ are supplemented with ${f^'_i}$ function derivative
        values.

        Different type of first derivative approximations are implemented,
        both local and non-local. Local schemes (Fourth-order, Parabolic,
        Modified Parabolic, Fritsch-Butland, Akima, Kruger) use only $f$ values
        near $x_i$ to calculate each $f^'_i$. Non-local schemes (Spline with
        different boundary conditions) use all ${f_i}$ values and obtain
        ${f^'_i}$ by solving a linear system of equations. Local schemes
        produce $C^1$ interpolants, while the spline schemes generate $C^2$
        interpolants.

        Hyman's monotonicity constraint filter is also implemented: it can be
        applied to all schemes to ensure that in the regions of local
        monotoniticity of the input (three successive increasing or decreasing
        values) the interpolating cubic remains monotonic. If the interpolating
        cubic is already monotonic, the Hyman filter leaves it unchanged
        preserving all its original features.

        In the case of $C^2$ interpolants the Hyman filter ensures local
        monotonicity at the expense of the second derivative of the interpolant
        which will no longer be continuous in the points where the filter has
        been applied.

        While some non-linear schemes (Modified Parabolic, Fritsch-Butland,
        Kruger) are guaranteed to be locally monotonic in their original
        approximation, all other schemes must be filtered according to the
        Hyman criteria at the expense of their linearity.

        See R. L. Dougherty, A. Edelman, and J. M. Hyman,
        "Nonnegativity-, Monotonicity-, or Convexity-Preserving CubicSpline and
        Quintic Hermite Interpolation"
   