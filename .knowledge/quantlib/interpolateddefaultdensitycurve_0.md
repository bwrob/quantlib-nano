/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
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

/*! \file interpolateddefaultdensitycurve.hpp
    \brief interpolated default-density term structure
*/

#ifndef quantlib_interpolated_default_density_curve_hpp
#define quantlib_interpolated_default_density_curve_hpp

#include <ql/termstructures/credit/defaultdensitystructure.hpp>
#include <ql/termstructures/interpolatedcurve.hpp>
#include <utility>

namespace QuantLib {

    //! DefaultProbabilityTermStructure based on interpolation of default densities
    /*! \ingroup defaultprobabilitytermstructures */
    template <class Interpolator>
    class InterpolatedDefaultDensityCurve
        : public DefaultDensityStructure,
          protected InterpolatedCurve<Interpolator> {
      public:
        InterpolatedDefaultDensityCurve(
            const std::vector<Date>& dates,
            const std::vector<Real>& densities,
            const DayCounter& dayCounter,
            const Calendar& calendar = Calendar(),
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedDefaultDensityCurve(
            const std::vector<Date>& dates,
            const std::vector<Real>& densities,
            const DayCounter& dayCounter,
            const Calendar& calendar,
            const Interpolator& interpolator);
        InterpolatedDefaultDensityCurve(
            const std::vector<Date>& dates,
            const std::vector<Real>& densities,
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
        const std::vector<Real>& defaultDensities() const;
        std::vector<std::pair<Date, Real> > nodes() const;
        //@}
      protected:
        InterpolatedDefaultDensityCurve(
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedDefaultDensityCurve(
            const Date& referenceDate,
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedDefaultDensityCurve(
            Natural settlementDays,
            const Calendar&,
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        //! \name DefaultDensityStructure implementation
        //@{
        Real defaultDensityImpl(Time) const override;
        Probability survivalProbabilityImpl(Time) const override;
        //@}
        mutable std::vector<Date> dates_;
      private:
        void initialize(con