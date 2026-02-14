/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2015 Jose Aparicio

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

#ifndef quantlib_interpolated_affine_hazard_rate_curve_hpp
#define quantlib_interpolated_affine_hazard_rate_curve_hpp

#include <ql/stochasticprocess.hpp>
#include <ql/experimental/credit/onefactoraffinesurvival.hpp>
#include <ql/termstructures/credit/probabilitytraits.hpp>
#include <ql/termstructures/interpolatedcurve.hpp>
#include <ql/termstructures/bootstraphelper.hpp>
#include <utility>

namespace QuantLib {

    /*! DefaultProbabilityTermStructure based on interpolation of a
    deterministic hazard rate component plus a stochastic one factor
    rate.
    */
    /*
    The hazard rate structure here refers to the deterministic term
    structure added on top of the affine model intensity. It is typically
    employed to match the current market implied probabilities. The total
    probabilities keep their meaning and are those of the affine model. An
    example of this is the CIR++ model as employed in credit.

    (Although this is not usually the preferred way one can instead match the
    model to price the market.)

    Notice that here, hazardRateImpl(Time) returns the deterministic part of
    the hazard rate and not E[\lambda] This is what the bootstrapping
    requires but it might be confusing.

    \todo Redesign?:
    The Affine model type is meant to model short rates; most methods
    if not all still have sense here, though discounts mean probabilities.
    This is not satisfactory, the affine models might need more structure
    or reusing these classes should be reconsidered.
    \todo Implement forward default methods.
    \todo Implement statistics methods (expected values etc)

    */
    /*! \ingroup defaultprobabilitytermstructures */
    template <class Interpolator>
    class InterpolatedAffineHazardRateCurve
        : public OneFactorAffineSurvivalStructure,
          protected InterpolatedCurve<Interpolator> {
      public:
        InterpolatedAffineHazardRateCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& hazardRates,
            const DayCounter& dayCounter,
            const ext::shared_ptr<OneFactorAffineModel>& model,
            const Calendar& cal = Calendar(),
            const std::vector<Handle<Quote> >& jumps = std::vector<Handle<Quote> >(),
            const std::vector<Date>& jumpDates = std::vector<Date>(),
            const Interpolator& interpolator = Interpolator());
        InterpolatedAffineHazardRateCurve(const std::vector<Date>& dates,
                                          const std::vector<Rate>& hazardRates,
                                          const DayCounter& dayCounter,
                                          const ext::shared_ptr<OneFactorAffineModel>& model,
                                          const Calendar& calendar,
                                          const Interpolator& interpolator);
        InterpolatedAffineHazardRateCurve(const std::vector<Date>& dates,
                                          const std::vector<Rate>& hazardRates,
                                          const DayCounter& dayCounter,
                                          const ext::shared_ptr<OneFactorAffineModel>& model,

