/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003 Ferdinando Ametrano
 Copyright (C) 2003 RiskMap srl

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

/*! \file generalstatistics.hpp
    \brief statistics tool
*/

#ifndef quantlib_general_statistics_hpp
#define quantlib_general_statistics_hpp

#include <ql/utilities/null.hpp>
#include <ql/errors.hpp>
#include <vector>
#include <algorithm>
#include <utility>

namespace QuantLib {

    //! Statistics tool
    /*! This class accumulates a set of data and returns their
        statistics (e.g: mean, variance, skewness, kurtosis,
        error estimation, percentile, etc.) based on the empirical
        distribution (no gaussian assumption)

        It doesn't suffer the numerical instability problem of
        IncrementalStatistics. The downside is that it stores all
        samples, thus increasing the memory requirements.
    */
    class GeneralStatistics {
      public:
        typedef Real value_type;
        GeneralStatistics();
        //! \name Inspectors
        //@{
        //! number of samples collected
        Size samples() const;

        //! collected data
        const std::vector<std::pair<Real,Real> >& data() const;

        //! sum of data weights
        Real weightSum() const;

        /*! returns the mean, defined as
            \f[ \langle x \rangle = \frac{\sum w_i x_i}{\sum w_i}. \f]
        */
        Real mean() const;

        /*! returns the variance, defined as
            \f[ \sigma^2 = \frac{N}{N-1} \left\langle \left(
                x-\langle x \rangle \right)^2 \right\rangle. \f]
        */
        Real variance() const;

        /*! returns the standard deviation \f$ \sigma \f$, defined as the
            square root of the variance.
        */
        Real standardDeviation() const;

        /*! returns the error estimate on the mean value, defined as
            \f$ \epsilon = \sigma/\sqrt{N}. \f$
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

        /*! Expectation value of a function \f$ f \f$ on a given
            range \f$ \mathcal{R} \f$, i.e.,
            \f[ \mathrm{E}\left[f \;|\; \mathcal{R}\right] =
                \frac{\sum_{x_i \in \mathcal{R}} f(x_i) w_i}{
                      \sum_{x_i \in \mathcal{R}} w_i}. \f]
            The range is passed as a boolean function returning
            <tt>true</tt> if the argument belongs to the range
            or <tt>false</tt> otherwise.

            The function returns a pair made of the result and
            the num