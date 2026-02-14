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

#ifndef onefactor_affine_survival_hpp
#define onefactor_affine_survival_hpp

#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/stochasticprocess.hpp>
#include <ql/termstructures/credit/hazardratestructure.hpp>
#include <utility>

namespace QuantLib {
    
    /*! Survival probability term structure based on a one factor stochastic
    model of the default intensity.
    */
    /*
    While deriving from the hazard rate class the HRTS refers only to the
    deterministic part of the model. The probabilities depend on this 
    component and the stochastic part and are rewritten here.
    Derived classes need to specify the deterministic part 
    of the hazard rate if any (the one returned by 'hazardRateImpl'). It
    is needed for the conditional/forward probabilities.
     */
    class OneFactorAffineSurvivalStructure 
        : public HazardRateStructure {
    public:
        // implement remaining constructors.....
      explicit OneFactorAffineSurvivalStructure(
          ext::shared_ptr<OneFactorAffineModel> model,
          const DayCounter& dayCounter = DayCounter(),
          const std::vector<Handle<Quote> >& jumps = std::vector<Handle<Quote> >(),
          const std::vector<Date>& jumpDates = std::vector<Date>())
      : HazardRateStructure(dayCounter, jumps, jumpDates), model_(std::move(model)) {}

      OneFactorAffineSurvivalStructure(
          ext::shared_ptr<OneFactorAffineModel> model,
          const Date& referenceDate,
          const Calendar& cal = Calendar(),
          const DayCounter& dayCounter = DayCounter(),
          const std::vector<Handle<Quote> >& jumps = std::vector<Handle<Quote> >(),
          const std::vector<Date>& jumpDates = std::vector<Date>())
      : HazardRateStructure(referenceDate, Calendar(), dayCounter, jumps, jumpDates),
        model_(std::move(model)) {}

      OneFactorAffineSurvivalStructure(
          ext::shared_ptr<OneFactorAffineModel> model,
          Natural settlementDays,
          const Calendar& calendar,
          const DayCounter& dayCounter = DayCounter(),
          const std::vector<Handle<Quote> >& jumps = std::vector<Handle<Quote> >(),
          const std::vector<Date>& jumpDates = std::vector<Date>())
      : HazardRateStructure(settlementDays, calendar, dayCounter, jumps, jumpDates),
        model_(std::move(model)) {}

      //! \name TermStructure interface
      //@{
      // overwrite on mkt models (e.g. bootstraps)
      Date maxDate() const override { return Date::maxDate(); }

      /* Notice this is not calling hazard rate methods, these are
         stochastic now.
      */
      /*!
        Returns the probability at a future time dTgt, conditional to
        survival at a prior time dFwd and to the realization of a particular
        hazard rate value at dFwd.
        \param dFwd Time of the forward survival calculation and HR
                    realization.
        \param dTgt Target time of survival probability.
        \param yVal Realized value of the HR at time dFwd.
        \param extrapolate Allow curve extrapolation.
        \return Survival probability.

        \todo turn into a protected method to be called by
              defaults