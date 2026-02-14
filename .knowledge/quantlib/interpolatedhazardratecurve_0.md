/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Jose Aparicio
 Copyright (C) 2008 Chris Kenyon
 Copyright (C) 2008 Roland Lichters
 Copyright (C) 2008, 2009 StatPro Italia srl

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

/*! \file interpolatedhazardratecurve.hpp
    \brief interpolated hazard-rate term structure
*/

#ifndef quantlib_interpolated_hazard_rate_curve_hpp
#define quantlib_interpolated_hazard_rate_curve_hpp

#include <ql/termstructures/credit/hazardratestructure.hpp>
#include <ql/termstructures/interpolatedcurve.hpp>
#include <utility>

namespace QuantLib {

    //! DefaultProbabilityTermStructure based on interpolation of hazard rates
    /*! \ingroup defaultprobabilitytermstructures */
    template <class Interpolator>
    class InterpolatedHazardRateCurve
        : public HazardRateStructure,
          protected InterpolatedCurve<Interpolator> {
      public:
        InterpolatedHazardRateCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& hazardRates,
            const DayCounter& dayCounter,
            const Calendar& cal = Calendar(),
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedHazardRateCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& hazardRates,
            const DayCounter& dayCounter,
            const Calendar& calendar,
            const Interpolator& interpolator);
        InterpolatedHazardRateCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& hazardRates,
            const DayCounter& dayCounter,
            const Interpolator& interpolator);
        //! \name TermStructure interface
        //@{
        Date maxDate() const override;
        //@}
        //! \name other inspectors
        //@{
        const std::vector<Time>& times() const;
        const std::vector<Date>& dates() const;
        const std::vector<Real>& data() const;
        const std::vector<Rate>& hazardRates() const;
        std::vector<std::pair<Date, Real> > nodes() const;
        //@}
      protected:
        InterpolatedHazardRateCurve(
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedHazardRateCurve(
            const Date& referenceDate,
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedHazardRateCurve(
            Natural settlementDays,
            const Calendar&,
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        //! \name DefaultProbabilityTermStructure implementation
        //@{
        Real hazardRateImpl(Time) const override;
        Probability survivalProbabilityImpl(Time) const override;
        //@}
        mutable std::vector<Date> dates_;
      private:
        void initialize();
    };


    // inline
