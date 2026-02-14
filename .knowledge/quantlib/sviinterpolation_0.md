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

/*! \file sviinterpolation.hpp
    \brief Svi interpolation interpolation between discrete points
*/

#ifndef quantlib_svi_interpolation_hpp
#define quantlib_svi_interpolation_hpp

#include <ql/experimental/volatility/svismilesection.hpp>
#include <ql/math/interpolations/xabrinterpolation.hpp>
#include <utility>

namespace QuantLib {

namespace detail {

inline void checkSviParameters(const Real a, const Real b, const Real sigma,
                               const Real rho, const Real m, const Time tte) {
    QL_REQUIRE(b >= 0.0, "b (" << b << ") must be non negative");
    QL_REQUIRE(std::fabs(rho) < 1.0, "rho (" << rho << ") must be in (-1,1)");
    QL_REQUIRE(sigma > 0.0, "sigma (" << sigma << ") must be positive");
    QL_REQUIRE(a + b * sigma * std::sqrt(1.0 - rho * rho) >= 0.0,
               "a + b sigma sqrt(1-rho^2) (a=" << a << ", b=" << b << ", sigma="
                                               << sigma << ", rho=" << rho
                                               << ") must be non negative");
    QL_REQUIRE(b * (1.0 + std::fabs(rho)) <= 4.0,
               "b(1+|rho|) must be less than or equal to 4, (b=" << b << ", rho=" << rho << ")");

}

inline Real sviTotalVariance(const Real a, const Real b, const Real sigma,
                             const Real rho, const Real m, const Real k) {
    return a +
           b * (rho * (k - m) + std::sqrt((k - m) * (k - m) + sigma * sigma));
}

typedef SviSmileSection SviWrapper;

struct SviSpecs {
    Size dimension() { return 5; }
    void defaultValues(std::vector<Real> &params,
                       std::vector<bool> &paramIsFixed, const Real &forward,
                       const Real expiryTime,
                       const std::vector<Real> &addParams) {
        if (params[2] == Null<Real>())
            params[2] = 0.1;
        if (params[3] == Null<Real>())
            params[3] = -0.4;
        if (params[4] == Null<Real>())
            params[4] = 0.0;
        if (params[1] == Null<Real>())
            params[1] = 2.0 / (1.0 + std::fabs(params[3]));
        if (params[0] == Null<Real>()) {
            params[0] = std::max(
                0.20 * 0.20 * expiryTime -
                    params[1] * (params[3] * (-params[4]) +
                                 std::sqrt((-params[4]) * (-params[4]) +
                                           params[2] * params[2])),
                -params[1] * params[2] *
                std::sqrt(1.0 - params[3] * params[3]) + eps1());
        }
    }
    void guess(Array &values, const std::vector<bool> &paramIsFixed,
               const Real &forward, const Real expiryTime,
               const std::vector<Real> &r, const std::vector<Real> &addParams) {
        Size j = 0;
        if (!paramIsFixed[2])
            values[2] = r[j++] + eps1();
        if (!paramIsFixed[3])
            values[3] = (2.0 * r[j++] - 1.0) * eps2();
        if (!paramIsFixed[4])
            values[4] = (2.0 * r[j++] - 1.0);
        if (!paramIsFixed[1])
            values[1] = r[j++] * 4.0 / (1.0 + std::fabs(values[3])) * eps2();
        if (!paramIsFixed[0])
            values[0] = r[j++] * expiryTime -
                        eps2() * (values[1] * value
