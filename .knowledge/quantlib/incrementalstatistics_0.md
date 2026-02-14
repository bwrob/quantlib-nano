/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003 Ferdinando Ametrano
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
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

/*! \file incrementalstatistics.hpp
    \brief statistics tool based on incremental accumulation
           in the meantime, this is just a wrapper to the boost
           accumulator library, kept for backward compatibility
*/

#ifndef quantlib_incremental_statistics_hpp
#define quantlib_incremental_statistics_hpp

#include <ql/utilities/null.hpp>
#include <ql/errors.hpp>
#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/accumulators/statistics/count.hpp>
#include <boost/accumulators/statistics/sum.hpp>
#include <boost/accumulators/statistics/min.hpp>
#include <boost/accumulators/statistics/max.hpp>
#include <boost/accumulators/statistics/weighted_mean.hpp>
#include <boost/accumulators/statistics/weighted_variance.hpp>
#include <boost/accumulators/statistics/weighted_skewness.hpp>
#include <boost/accumulators/statistics/weighted_kurtosis.hpp>
#include <boost/accumulators/statistics/weighted_moment.hpp>

namespace QuantLib {

    //! Statistics tool based on incremental accumulation
    /*! It can accumulate a set of data and return statistics (e.g: mean,
        variance, skewness, kurtosis, error estimation, etc.).
        This class is a wrapper to the boost accumulator library.
    */

    class IncrementalStatistics {
      public:
        typedef Real value_type;
        IncrementalStatistics();
        //! \name Inspectors
        //@{
        //! number of samples collected
        Size samples() const;

        //! sum of data weights
        Real weightSum() const;

        /*! returns the mean, defined as
            \f[ \langle x \rangle = \frac{\sum w_i x_i}{\sum w_i}. \f]
        */
        Real mean() const;

        /*! returns the variance, defined as
            \f[ \frac{N}{N-1} \left\langle \left(
                x-\langle x \rangle \right)^2 \right\rangle. \f]
        */
        Real variance() const;

        /*! returns the standard deviation \f$ \sigma \f$, defined as the
            square root of the variance.
        */
        Real standardDeviation() const;

        /*! returns the error estimate \f$ \epsilon \f$, defined as the
            square root of the ratio of the variance to the number of
            samples.
        */
        Real errorEstimate() const;

        /*! returns the skewness, defined as
            \f[ \frac{N^2}{(N-1)(N-2)} \frac{\left\langle \left(
                x-\langle x \rangle \right)^3 \right\rangle}{\sigma^3}. \f]
            The above evaluates to 0 for a Gaussian distribution.
        */
        Real skewness() const;

        /*! returns the excess kurtosis, defined as
            \f[ \frac{N^2(N+1)}{(N-1)(N-2)(N-3)}
                \frac{\left\langle \left(x-\langle x \rangle \right)^4
                \right\rangle}{\sigma^4} - \frac{3(N-1)^2}{(N-2)(N-3)}. \f]
            The above evaluates to 0 for a Gaussian distribution.
        */
        Real kurtosis() const;

        /*! returns the minimum sample value */
        Real min() const;

        /*! returns the maximum sample value */
        Real max() const;


