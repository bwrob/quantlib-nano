/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003, 2004, 2005, 2006, 2007, 2008 StatPro Italia srl
 Copyright (C) 2009, 2015 Ferdinando Ametrano
 Copyright (C) 2015 Paolo Mazzocchi

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

/*! \file zerocurve.hpp
    \brief interpolated zero-rates structure
*/

#ifndef quantlib_zero_curve_hpp
#define quantlib_zero_curve_hpp

#include <ql/termstructures/yield/zeroyieldstructure.hpp>
#include <ql/termstructures/interpolatedcurve.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/interestrate.hpp>
#include <ql/utilities/dataformatters.hpp>
#include <utility>

namespace QuantLib {

    //! YieldTermStructure based on interpolation of zero rates
    /*! \ingroup yieldtermstructures */
    template <class Interpolator>
    class InterpolatedZeroCurve : public ZeroYieldStructure,
                                  protected InterpolatedCurve<Interpolator> {
      public:
        // constructor
        InterpolatedZeroCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& yields,
            const DayCounter& dayCounter,
            const Calendar& calendar = Calendar(),
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {},
            Compounding compounding = Continuous,
            Frequency frequency = Annual);
        InterpolatedZeroCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& yields,
            const DayCounter& dayCounter,
            const Calendar& calendar,
            const Interpolator& interpolator,
            Compounding compounding = Continuous,
            Frequency frequency = Annual);
        InterpolatedZeroCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& yields,
            const DayCounter& dayCounter,
            const Interpolator& interpolator,
            Compounding compounding = Continuous,
            Frequency frequency = Annual);
        //! \name TermStructure interface
        //@{
        Date maxDate() const override;
        //@}
        //! \name other inspectors
        //@{
        const std::vector<Time>& times() const;
        const std::vector<Date>& dates() const;
        const std::vector<Real>& data() const;
        const std::vector<Rate>& zeroRates() const;
        std::vector<std::pair<Date, Real> > nodes() const;
        //@}

      protected:
        explicit InterpolatedZeroCurve(
            const DayCounter&,
            const Interpolator& interpolator = {});
        InterpolatedZeroCurve(
            const Date& referenceDate,
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedZeroCurve(
            Natural settlementDays,
            const Calendar&,
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});

        //! \name ZeroYieldStructure implementation
        //@{
        Rate zeroYieldImpl(Time t) const override
