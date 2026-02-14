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

/*! \file xabrinterpolation.hpp
    \brief generic interpolation class for sabr style underlying models
           like the Hagan 2002 expansion, Doust's no arbitrage sabr,
           Andreasen's zabr expansion for the masses and similar
*/

#ifndef ql_xabr_interpolation_hpp
#define ql_xabr_interpolation_hpp

#include <ql/math/interpolation.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <ql/math/optimization/levenbergmarquardt.hpp>
#include <ql/math/optimization/method.hpp>
#include <ql/math/optimization/projectedcostfunction.hpp>
#include <ql/math/optimization/simplex.hpp>
#include <ql/math/randomnumbers/haltonrsg.hpp>
#include <ql/pricingengines/blackformula.hpp>
#include <ql/termstructures/volatility/volatilitytype.hpp>
#include <ql/utilities/dataformatters.hpp>
#include <ql/utilities/null.hpp>
#include <utility>

namespace QuantLib::detail {

template <typename Model> class XABRCoeffHolder {
  public:
    XABRCoeffHolder(const Time t,
                    const Real& forward,
                    const std::vector<Real>& params,
                    const std::vector<bool>& paramIsFixed,
                    std::vector<Real> addParams)
    : t_(t), forward_(forward), params_(params), paramIsFixed_(paramIsFixed.size(), false),
      error_(Null<Real>()), maxError_(Null<Real>()), addParams_(std::move(addParams)) {
        QL_REQUIRE(t > 0.0, "expiry time must be positive: " << t
                                                             << " not allowed");
        QL_REQUIRE(params.size() == Model().dimension(),
                   "wrong number of parameters (" << params.size()
                                                  << "), should be "
                                                  << Model().dimension());
        QL_REQUIRE(paramIsFixed.size() == Model().dimension(),
                   "wrong number of fixed parameters flags ("
                       << paramIsFixed.size() << "), should be "
                       << Model().dimension());

        for (Size i = 0; i < params.size(); ++i) {
            if (params[i] != Null<Real>())
                paramIsFixed_[i] = paramIsFixed[i];
        }
        Model().defaultValues(params_, paramIsFixed_, forward_, t_, addParams_);
        updateModelInstance();
    }
    virtual ~XABRCoeffHolder() = default;

    void updateModelInstance() {
        modelInstance_ = Model().instance(t_, forward_, params_, addParams_);
    }

    /*! Expiry, Forward */
    Real t_;
    const Real &forward_;
    /*! Parameters */
    std::vector<Real> params_;
    std::vector<bool> paramIsFixed_;
    std::vector<Real> weights_;
    /*! Interpolation results */
    Real error_, maxError_;
    EndCriteria::Type XABREndCriteria_ = EndCriteria::None;
    /*! Model instance (if required) */
    ext::shared_ptr<typename Model::type> modelInstance_;
    /*! additional parameters */
    std::vector<Real> addParams_;
};

template <class I1, class I2, typename Model>
class