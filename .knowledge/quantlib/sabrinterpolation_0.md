/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Ferdinando Ametrano
 Copyright (C) 2007 Marco Bianchetti
 Copyright (C) 2007 François du Vignaud
 Copyright (C) 2007 Giorgio Facchinetti
 Copyright (C) 2006 Mario Pucci
 Copyright (C) 2006 StatPro Italia srl
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

/*! \file sabrinterpolation.hpp
    \brief SABR interpolation interpolation between discrete points
*/

#ifndef quantlib_sabr_interpolation_hpp
#define quantlib_sabr_interpolation_hpp

#include <ql/math/interpolations/xabrinterpolation.hpp>
#include <ql/termstructures/volatility/sabr.hpp>
#include <utility>

namespace QuantLib {

namespace detail {

class SABRWrapper {
  public:
    SABRWrapper(const Time t,
                const Real& forward,
                const std::vector<Real>& params,
                const std::vector<Real>& addParams)
    : t_(t), forward_(forward), params_(params), shift_(addParams.empty() ? 0.0 : addParams[0]) {
        QL_REQUIRE(forward_ + shift_ > 0.0, "forward+shift must be positive: "
                                                 << forward_ << " with shift "
                                                 << shift_ << " not allowed");
        validateSabrParameters(params[0], params[1], params[2], params[3]);
    }
    Real volatility(const Real x, const VolatilityType volatilityType) {
        return shiftedSabrVolatility(x, forward_, t_, params_[0], params_[1],
                                     params_[2], params_[3], shift_, volatilityType);
    }

  private:
    const Real t_, &forward_;
    const std::vector<Real> &params_;
    const Real shift_;
};

struct SABRSpecs {
    Size dimension() { return 4; }
    void defaultValues(std::vector<Real> &params, std::vector<bool> &,
                       const Real &forward, const Real expiryTime,
                       const std::vector<Real> &addParams) {
        if (params[1] == Null<Real>())
            params[1] = 0.5;
        if (params[0] == Null<Real>())
            // adapt alpha to beta level
            params[0] = 0.2 * (params[1] < 0.9999 ?
                                   Real(std::pow(forward + (addParams.empty() ? 0.0 : addParams[0]),
                                            1.0 - params[1])) :
                                   1.0);
        if (params[2] == Null<Real>())
            params[2] = std::sqrt(0.4);
        if (params[3] == Null<Real>())
            params[3] = 0.0;
    }
    void guess(Array &values, const std::vector<bool> &paramIsFixed,
               const Real &forward, const Real expiryTime,
               const std::vector<Real> &r, const std::vector<Real> &addParams) {
        Size j = 0;
        if (!paramIsFixed[1])
            values[1] = (1.0 - 2E-6) * r[j++] + 1E-6;
        if (!paramIsFixed[0]) {
            values[0] = (1.0 - 2E-6) * r[j++] + 1E-6; // lognormal vol guess
            // adapt this to beta level
            if (values[1] < 0.999)
                values[0] *=
                    std::pow(forward + (addParams.empty() ? 0.0 : addParams[0]), 1.0 - values[1]);
        }
        if (!paramIsFixed[2])
            values[2] = 1.5 * r[j++] + 1E-6;
        if (!paramIsFixed[3])
            values[3] = (2.0 * r[j++] - 1.0) * (1.0 - 1E-6);
    }
    Real eps1() { return .00000
