/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2013, 2015 Peter Caspers

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

/*! \file gsr.hpp
    \brief GSR 1 factor model
*/

#ifndef quantlib_gsr_hpp
#define quantlib_gsr_hpp

#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <ql/processes/gsrprocess.hpp>

namespace QuantLib {

//! One factor gsr model, formulation is in forward measure

class Gsr : public Gaussian1dModel, public CalibratedModel {

  public:
    // constant mean reversion
    Gsr(const Handle<YieldTermStructure>& termStructure,
        std::vector<Date> volstepdates,
        const std::vector<Real>& volatilities,
        Real reversion,
        Real T = 60.0);
    // piecewise mean reversion (with same step dates as volatilities)
    Gsr(const Handle<YieldTermStructure>& termStructure,
        std::vector<Date> volstepdates,
        const std::vector<Real>& volatilities,
        const std::vector<Real>& reversions,
        Real T = 60.0);
    // constant mean reversion with floating model data
    Gsr(const Handle<YieldTermStructure>& termStructure,
        std::vector<Date> volstepdates,
        std::vector<Handle<Quote> > volatilities,
        const Handle<Quote>& reversion,
        Real T = 60.0);
    // piecewise mean reversion with floating model data
    Gsr(const Handle<YieldTermStructure>& termStructure,
        std::vector<Date> volstepdates,
        std::vector<Handle<Quote> > volatilities,
        std::vector<Handle<Quote> > reversions,
        Real T = 60.0);

    Real numeraireTime() const;
    void numeraireTime(Real T);

    const Array &reversion() const { return reversion_.params(); }
    const Array &volatility() const { return sigma_.params(); }

    // calibration constraints

    // fixed reversions, only volatilities are free
    std::vector<bool> FixedReversions() {
        std::vector<bool> res(reversions_.size(), true);
        std::vector<bool> vol(volatilities_.size(), false);
        res.insert(res.end(), vol.begin(), vol.end());
        return res;
    }

    // fixed volatilities, only reversions are free
    std::vector<bool> FixedVolatilities() {
        std::vector<bool> res(reversions_.size(), false);
        std::vector<bool> vol(volatilities_.size(), true);
        res.insert(res.end(), vol.begin(), vol.end());
        return res;
    }

    std::vector<bool> MoveVolatility(Size i) {
        QL_REQUIRE(i < volatilities_.size(),
                   "volatility with index " << i << " does not exist (0..."
                                            << volatilities_.size() - 1 << ")");
        std::vector<bool> res(reversions_.size() + volatilities_.size(), true);
        res[reversions_.size() + i] = false;
        return res;
    }

    std::vector<bool> MoveReversion(Size i) {
        QL_REQUIRE(i < reversions_.size(),
                   "reversion with index " << i << " does not exist (0..."
                                           << reversions_.size() - 1 << ")");
        std::vector<bool> res(reversions_.size() + volatilities_.size(), true);
        res[i] = false;
        return res;
    }

    // With fixed reversion calibrate the volatilities one by one
    // to the given helpers. It is assumed that that volatility step
    // dates are suitable for this, i.e. they s