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

/*! \file noarbsabrinterpolation.hpp
    \brief noabr sabr interpolation between discrete points
*/

#ifndef quantlib_noarbsabr_interpolation_hpp
#define quantlib_noarbsabr_interpolation_hpp

#include <ql/experimental/volatility/noarbsabrsmilesection.hpp>
#include <ql/math/interpolations/sabrinterpolation.hpp>
#include <utility>

namespace QuantLib {

namespace detail {

// we can directly use the smile section as the wrapper
typedef NoArbSabrSmileSection NoArbSabrWrapper;

struct NoArbSabrSpecs {
    Size dimension() { return 4; }
    Real eps() { return 0.000001; }
    void defaultValues(std::vector<Real> &params,
                       std::vector<bool> &paramIsFixed, const Real &forward,
                       const Real expiryTime, const std::vector<Real> &addParams) {
        SABRSpecs().defaultValues(params, paramIsFixed, forward, expiryTime, addParams);
        // check if alpha / beta is admissable, otherwise adjust
        // if possible (i.e. not fixed, otherwise an exception will
        // be thrown from the model constructor anyway)
        Real sigmaI = params[0] * std::pow(forward, params[1] - 1.0);
        if (sigmaI < detail::NoArbSabrModel::sigmaI_min) {
            if (!paramIsFixed[0])
                params[0] = detail::NoArbSabrModel::sigmaI_min * (1.0 + eps()) /
                            std::pow(forward, params[1] - 1.0);
            else {
                if (!paramIsFixed[1])
                    params[1] = 1.0 +
                                std::log(detail::NoArbSabrModel::sigmaI_min *
                                         (1.0 + eps()) / params[0]) /
                                    std::log(forward);
            }
        }
        if (sigmaI > detail::NoArbSabrModel::sigmaI_max) {
            if (!paramIsFixed[0])
                params[0] = detail::NoArbSabrModel::sigmaI_max * (1.0 - eps()) /
                            std::pow(forward, params[1] - 1.0);
            else {
                if (!paramIsFixed[1])
                    params[1] = 1.0 +
                                std::log(detail::NoArbSabrModel::sigmaI_max *
                                         (1.0 - eps()) / params[0]) /
                                    std::log(forward);
            }
        }
    }
    void guess(Array &values, const std::vector<bool> &paramIsFixed,
               const Real &forward, const Real expiryTime,
               const std::vector<Real> &r, const std::vector<Real> &) {
        Size j = 0;
        if (!paramIsFixed[1])
            values[1] = detail::NoArbSabrModel::beta_min +
                        (detail::NoArbSabrModel::beta_max -
                         detail::NoArbSabrModel::beta_min) *
                            r[j++];
        if (!paramIsFixed[0]) {
            Real sigmaI = detail::NoArbSabrModel::sigmaI_min +
                          (detail::NoArbSabrModel::sigmaI_max -
                           detail::NoArbSabrModel::sigmaI_min) *
                              r[j++];
            sigmaI *= (1.0 - eps());
            sigmaI += eps() / 2.0;
            values[0] = sigmaI / std::pow(forward, values[1] - 1.0);
        }
        if (!paramIsFixed[2])
            values[2] = det