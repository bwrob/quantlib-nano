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

/*! \file gaussian1dmodel.hpp
    \brief basic interface for one factor interest rate models
*/

// uncomment to enable NTL support (see below for more details and references)
// #define GAUSS1D_ENABLE_NTL

#ifndef quantlib_gaussian1dmodel_hpp
#define quantlib_gaussian1dmodel_hpp

#include <ql/models/model.hpp>
#include <ql/models/parameter.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/indexes/swapindex.hpp>
#include <ql/instruments/vanillaswap.hpp>
#include <ql/time/date.hpp>
#include <ql/time/period.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/stochasticprocess.hpp>
#include <ql/utilities/null.hpp>
#include <ql/patterns/lazyobject.hpp>

#ifdef GAUSS1D_ENABLE_NTL
#include <boost/math/bindings/rr.hpp>
#endif

#if BOOST_VERSION < 106700
#include <boost/functional/hash.hpp>
#else
#include <boost/container_hash/hash.hpp>
#endif

#include <unordered_map>

namespace QuantLib {

/*! One factor interest rate model interface class
    The only methods that must be implemented by subclasses
    are the numeraire and zerobond methods for an input array
    of state variable values. The variable $y$ is understood
    to be the standardized (zero mean, unit variance) version
    of the model's original state variable $x$.

    NTL support may be enabled by defining GAUSS1D_ENABLE_NTL in this
    file. For details on NTL see
             http://www.shoup.net/ntl/

    \warning the variance of the state process conditional on
    $x(t)=x$ must be independent of the value of $x$

*/

class Gaussian1dModel : public TermStructureConsistentModel, public LazyObject {
  public:
    ext::shared_ptr<StochasticProcess1D> stateProcess() const;

    Real numeraire(Time t,
                   Real y = 0.0,
                   const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;

    Real zerobond(Time T,
                  Time t = 0.0,
                  Real y = 0.0,
                  const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;

    Real numeraire(const Date& referenceDate,
                   Real y = 0.0,
                   const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;

    Real zerobond(const Date& maturity,
                  const Date& referenceDate = Date(),
                  Real y = 0.0,
                  const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>()) const;

    Real zerobondOption(const Option::Type& type,
                        const Date& expiry,
                        const Date& valueDate,
                        const Date& maturity,
                        Rate strike,
                        const Date& referenceDate = Date(),
                        Real y = 0.0,
                        const Handle<YieldTermStructure>& yts = Handle<YieldTermStructure>(),
                        Real yStdDevs = 7.0,
                        Size yGridPoints = 64,
                        bool extrapolatePayoff = true,
                        bool flatPayoffExtrapolation = false) const;

    Real
    forwardRate(const Date& fixing,
                const Date& referenceDate = Date(),
                Real y = 0.0,
      