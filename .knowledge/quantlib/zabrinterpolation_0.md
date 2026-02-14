/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2014 Peter Caspers

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

/*! \file zabrinterpolation.hpp
    \brief ZABR interpolation interpolation between discrete points
*/

#ifndef quantlib_zabr_interpolation_hpp
#define quantlib_zabr_interpolation_hpp

#include <ql/experimental/volatility/zabrsmilesection.hpp>
#include <ql/math/interpolations/xabrinterpolation.hpp>
#include <utility>

namespace QuantLib {

namespace detail {

template <typename Evaluation> struct ZabrSpecs {
    Size dimension() { return 5; }
    Real eps() { return 0.000001; }
    void defaultValues(std::vector<Real> &params,
                       std::vector<bool> &paramIsFixed, const Real &forward,
                       const Real expiryTime, const std::vector<Real>& addParams) {
        if (params[1] == Null<Real>())
            params[1] = 0.5;
        if (params[0] == Null<Real>())
            // adapt alpha to beta level
            params[0] =
                0.2 *
                (params[1] < 0.9999 ? std::pow(forward, 1.0 - params[1]) : Real(1.0));
        if (params[2] == Null<Real>())
            params[2] = std::sqrt(0.4);
        if (params[3] == Null<Real>())
            params[3] = 0.0;
        if (params[4] == Null<Real>())
            params[4] = 1.0;
    }
    void guess(Array &values, const std::vector<bool> &paramIsFixed,
               const Real &forward, const Real expiryTime,
               const std::vector<Real> &r, const std::vector<Real>& addParams) {
        Size j = 0;
        if (!paramIsFixed[1])
            values[1] = (1.0 - 2E-6) * r[j++] + 1E-6;
        if (!paramIsFixed[0]) {
            values[0] = (1.0 - 2E-6) * r[j++] + 1E-6; // lognormal vol guess
            // adapt this to beta level
            if (values[1] < 0.999)
                values[0] *= std::pow(forward, 1.0 - values[1]);
        }
        if (!paramIsFixed[2])
            values[2] = 1.5 * r[j++] + 1E-6;
        if (!paramIsFixed[3])
            values[3] = (2.0 * r[j++] - 1.0) * (1.0 - 1E-6);
        if (!paramIsFixed[4])
            values[4] = r[j++] * 2.0;
    }
    Real eps1() { return .0000001; }
    Real eps2() { return .9999; }
    Real dilationFactor() { return 0.001; }
    Array inverse(const Array &y, const std::vector<bool> &,
                  const std::vector<Real> &, const Real) {
        Array x(5);
        x[0] = y[0] < 25.0 + eps1() ? std::sqrt(y[0] - eps1())
                                    : Real((y[0] - eps1() + 25.0) / 10.0);
        x[1] = std::sqrt(-std::log(y[1]));
        x[2] = std::tan(M_PI*(y[4]/5.0-0.5));
        x[3] = std::asin(y[3] / eps2());
        x[4] = std::tan(M_PI*(y[4]/1.9-0.5));
        return x;
    }
    Array direct(const Array &x, const std::vector<bool> &,
                 const std::vector<Real> &, const Real) {
        Array y(5);
        y[0] = std::fabs(x[0]) < 5.0 ? Real(x[0] * x[0] + eps1())
                                     : (10.0 * std::fabs(x[0]) - 25.0) + eps1();
        y[1] = std::fabs(x[1]) < std::sqrt(-std::log(eps1()))
                   ? std::exp(-(x[1] * x[1]))
                   : eps1();
        // limit nu to 5.00
        y[2] = (std::atan(x[2])/M_PI + 0.5) * 5.0;
        y[3] = std::fabs(x[3]) < 2.5 * M_PI
                   ? eps2() * std::sin(x[3])

