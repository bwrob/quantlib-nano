/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2019 SoftSolutions! S.r.l.
 Copyright (C) 2025 Peter Caspers

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

/*! \file globalbootstrap.hpp
    \brief global bootstrap, with additional restrictions
*/

#ifndef quantlib_global_bootstrap_hpp
#define quantlib_global_bootstrap_hpp

#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/math/optimization/levenbergmarquardt.hpp>
#include <ql/termstructures/bootstraphelper.hpp>
#include <ql/utilities/dataformatters.hpp>
#include <algorithm>
#include <functional>
#include <utility>

namespace QuantLib {

class MultiCurveBootstrap;

class MultiCurveBootstrapContributor {
public:
    virtual ~MultiCurveBootstrapContributor() = default;
    virtual void
    setParentBootstrapper(const ext::shared_ptr<MultiCurveBootstrap>& b) const = 0;
    virtual Array setupCostFunction() const = 0;
    virtual void setCostFunctionArgument(const Array& v) const = 0;
    virtual Array evaluateCostFunction() const = 0;
    virtual void setToValid() const = 0;
};

class MultiCurveBootstrap : public ext::enable_shared_from_this<MultiCurveBootstrap> {
  public:
    explicit MultiCurveBootstrap(Real accuracy);
    explicit MultiCurveBootstrap(ext::shared_ptr<OptimizationMethod> optimizer = nullptr,
                        ext::shared_ptr<EndCriteria> endCriteria = nullptr);
    void add(const MultiCurveBootstrapContributor* c);
    void addObserver(Observer* o);
    void runMultiCurveBootstrap();
    void setOtherContributorsToValid() const;
    void finalizeCalculation();

  private:
    ext::shared_ptr<OptimizationMethod> optimizer_;
    ext::shared_ptr<EndCriteria> endCriteria_;
    std::vector<const MultiCurveBootstrapContributor*> contributors_;
    std::vector<Observer*> observers_;
};

class AdditionalBootstrapVariables {
  public:
    virtual ~AdditionalBootstrapVariables() = default;
    // Initialize variables to initial guesses and return them.
    virtual Array initialize(bool validData) = 0;
    // Update variables to given values.
    virtual void update(const Array& x) = 0;
};

/*! Global boostrapper, with additional restrictions

  The additionalDates functor must return a set of additional dates to add to the
  interpolation grid. These dates must only depend on the global evaluation date.

  The additionalPenalties functor must yield at least as many values such that

  number of (usual, alive) rate helpers + number of additional values >= number of data points - 1

  (note that the data points contain t=0). These values are treated as additional
  error terms in the optimization. The usual rate helpers return quoteError here.
  All error terms are equally weighted.

  The additionalHelpers are registered with the curve like the usual rate helpers,
  but no pillar dates or error terms are added for them. Pillars and error terms
  have to be added by additionalDates and additionalPenalties.

  The additionalVariables interface manages a set of additional variables to add
  to the optimization. This is useful to optimize model parameters used by rate
  helpers, for example, convexity adjustments for futures. See SimpleQuoteVariables
  for a concrete implementation of this interface.

  WARNING: This class is known to work with Traits Discount, ZeroYield, 