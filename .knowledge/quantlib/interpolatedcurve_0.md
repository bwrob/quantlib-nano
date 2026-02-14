/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 StatPro Italia srl

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

/*! \file interpolatedcurve.hpp
    \brief Helper class to build interpolated term structures
*/

#ifndef quantlib_interpolated_curve_hpp
#define quantlib_interpolated_curve_hpp

#include <ql/math/comparison.hpp>
#include <ql/math/interpolation.hpp>
#include <ql/time/date.hpp>
#include <ql/time/daycounter.hpp>
#include <utility>
#include <vector>

namespace QuantLib {

    //! Helper class to build interpolated term structures
    /*! Interpolated term structures can use protected or private
        inheritance from this class to obtain the relevant data
        members and implement correct copy behavior.
    */
    template <class Interpolator>
    class InterpolatedCurve {
      public:
        ~InterpolatedCurve() = default;

      protected:
        //! \name Building
        //@{
        InterpolatedCurve(std::vector<Time> times,
                          std::vector<Real> data,
                          const Interpolator& i = Interpolator())
        : times_(std::move(times)), data_(std::move(data)), interpolator_(i) {}

        InterpolatedCurve(std::vector<Time> times,
                          const Interpolator& i = Interpolator())
        : times_(std::move(times)), data_(times_.size()), interpolator_(i) {}

        InterpolatedCurve(Size n,
                          const Interpolator& i = Interpolator())
        : times_(n), data_(n), interpolator_(i) {}

        InterpolatedCurve(const Interpolator& i = Interpolator())
        : interpolator_(i) {}
        //@}

        //! \name Copying
        //@{
        InterpolatedCurve(const InterpolatedCurve& c)
        : times_(c.times_), data_(c.data_), interpolator_(c.interpolator_) {
            setupInterpolation();
        }

        InterpolatedCurve& operator=(const InterpolatedCurve& c) {
            times_ = c.times_;
            data_ = c.data_;
            interpolator_ = c.interpolator_;
            setupInterpolation();
            return *this;
        }
        //@}

        //! \name Moving
        //@{
        InterpolatedCurve(InterpolatedCurve&& c) noexcept
        : times_(std::move(c.times_)), data_(std::move(c.data_)), interpolator_(std::move(c.interpolator_)) {
            setupInterpolation();
        }

        InterpolatedCurve& operator=(InterpolatedCurve&& c) noexcept {
            times_ = std::move(c.times_);
            data_ = std::move(c.data_);
            interpolator_ = std::move(c.interpolator_);
            setupInterpolation();
            return *this;
        }
        //@}

        //! \name Utilities
        //@{
        void setupTimes(const std::vector<Date>& dates,
                        Date referenceDate,
                        const DayCounter& dayCounter) {
            times_.resize(dates.size());
            times_[0] = dayCounter.yearFraction(referenceDate, dates[0]);
            for (Size i = 1; i < dates.size(); i++) {
                QL_REQUIRE(dates[i] > dates[i-1],
                           "dates not sorted: " << dates[i] << " passed after " << dates[i-1]);

                times_[i] = dayCounter.yearFraction(referenceDate, dates[i]);
                QL_REQUIRE(!close(this->times_[i], this->times_[i-1]),
          