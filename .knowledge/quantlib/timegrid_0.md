/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2001, 2002, 2003 Sadruddin Rejeb
 Copyright (C) 2005, 2006 StatPro Italia srl

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

/*! \file timegrid.hpp
    \brief discrete time grid
*/

#ifndef quantlib_time_grid_hpp
#define quantlib_time_grid_hpp

#include <ql/errors.hpp>
#include <ql/math/comparison.hpp>
#include <vector>
#include <algorithm>
#include <iterator>
#include <numeric>
#include <cmath>

namespace QuantLib {

    //! time grid class
    /*! \todo what was the rationale for limiting the grid to
              positive times? Investigate and see whether we
              can use it for negative ones as well.
    */
    class TimeGrid {
      public:
        //! \name Constructors
        //@{
        TimeGrid() = default;
        //! Regularly spaced time-grid
        TimeGrid(Time end, Size steps);
        //! Time grid with mandatory time points
        /*! Mandatory points are guaranteed to belong to the grid.
            No additional points are added.
        */
        template <class Iterator>
        TimeGrid(Iterator begin, Iterator end)
        : mandatoryTimes_(begin, end) {
            QL_REQUIRE(begin != end, "empty time sequence");
            std::sort(mandatoryTimes_.begin(),mandatoryTimes_.end());
            // We seem to assume that the grid begins at 0.
            // Let's enforce the assumption for the time being
            // (even though I'm not sure that I agree.)
            QL_REQUIRE(mandatoryTimes_.front() >= 0.0,
                       "negative times not allowed");
            auto e = std::unique(mandatoryTimes_.begin(), mandatoryTimes_.end(),
                                 static_cast<bool (*)(Real, Real)>(close_enough));
            mandatoryTimes_.resize(e - mandatoryTimes_.begin());

            if (mandatoryTimes_[0] > 0.0)
                times_.push_back(0.0);

            times_.insert(times_.end(),
                          mandatoryTimes_.begin(), mandatoryTimes_.end());

            dt_.reserve(times_.size()-1);
            std::adjacent_difference(times_.begin()+1,times_.end(),
                                     std::back_inserter(dt_));

        }
        //! Time grid with mandatory time points
        /*! Mandatory points are guaranteed to belong to the grid.
            Additional points are then added with regular spacing
            between pairs of mandatory times in order to reach the
            desired number of steps.
        */
        template <class Iterator>
        TimeGrid(Iterator begin, Iterator end, Size steps)
        : mandatoryTimes_(begin, end) {
            QL_REQUIRE(begin != end, "empty time sequence");
            std::sort(mandatoryTimes_.begin(),mandatoryTimes_.end());
            // We seem to assume that the grid begins at 0.
            // Let's enforce the assumption for the time being
            // (even though I'm not sure that I agree.)
            QL_REQUIRE(mandatoryTimes_.front() >= 0.0,
                       "negative times not allowed");
            auto e = std::unique(mandatoryTimes_.begin(), mandatoryTimes_.end(),
                                 static_cast<bool (*)(Real, Real)>(close_enough));
            mandatoryTimes_.resize(e - mandatoryTimes_.begin());

            Time last = mandatoryTimes_.bac
