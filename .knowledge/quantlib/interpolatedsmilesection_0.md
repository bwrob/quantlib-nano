/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Ferdinando Ametrano
 Copyright (C) 2006 François du Vignaud
 Copyright (C) 2015 Peter Caspers

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

/*! \file interpolatedsmilesection.hpp
    \brief Interpolated smile section class
*/

#ifndef quantlib_interpolated_smile_section_hpp
#define quantlib_interpolated_smile_section_hpp

#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/quotes/simplequote.hpp>
#include <ql/termstructure.hpp>
#include <ql/termstructures/volatility/smilesection.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <utility>

namespace QuantLib {

    template<class Interpolator>
    class InterpolatedSmileSection : public SmileSection,
                                     public LazyObject {
      public:
        InterpolatedSmileSection(Time expiryTime,
                                 std::vector<Rate> strikes,
                                 const std::vector<Handle<Quote> >& stdDevHandles,
                                 Handle<Quote> atmLevel,
                                 const Interpolator& interpolator = Interpolator(),
                                 const DayCounter& dc = Actual365Fixed(),
                                 VolatilityType type = ShiftedLognormal,
                                 Real shift = 0.0);
        InterpolatedSmileSection(Time expiryTime,
                                 std::vector<Rate> strikes,
                                 const std::vector<Real>& stdDevs,
                                 Real atmLevel,
                                 const Interpolator& interpolator = Interpolator(),
                                 const DayCounter& dc = Actual365Fixed(),
                                 VolatilityType type = ShiftedLognormal,
                                 Real shift = 0.0);
        InterpolatedSmileSection(const Date& d,
                                 std::vector<Rate> strikes,
                                 const std::vector<Handle<Quote> >& stdDevHandles,
                                 Handle<Quote> atmLevel,
                                 const DayCounter& dc = Actual365Fixed(),
                                 const Interpolator& interpolator = Interpolator(),
                                 const Date& referenceDate = Date(),
                                 VolatilityType type = ShiftedLognormal,
                                 Real shift = 0.0);
        InterpolatedSmileSection(const Date& d,
                                 std::vector<Rate> strikes,
                                 const std::vector<Real>& stdDevs,
                                 Real atmLevel,
                                 const DayCounter& dc = Actual365Fixed(),
                                 const Interpolator& interpolator = Interpolator(),
                                 const Date& referenceDate = Date(),
                                 VolatilityType type = ShiftedLognormal,
                                 Real shift = 0.0);

        void performCalculations() const override;
        Real varianceImpl(Rate strike) const override;
        Volatility volatilityImpl(Rate strike) const override;
        Real minStrike() const override { return strikes_.front(); }
