/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003, 2004, 2005, 2006, 2007 Ferdinando Ametrano

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

/*! \file sequencestatistics.hpp
    \brief Statistics tools for sequence (vector, list, array) samples
*/

#ifndef quantlib_sequence_statistics_hpp
#define quantlib_sequence_statistics_hpp

#include <ql/math/statistics/statistics.hpp>
#include <ql/math/statistics/incrementalstatistics.hpp>
#include <ql/math/matrix.hpp>

namespace QuantLib {

    //! Statistics analysis of N-dimensional (sequence) data
    /*! It provides 1-dimensional statistics as discrepancy plus
        N-dimensional (sequence) statistics (e.g. mean,
        variance, skewness, kurtosis, etc.) with one component for each
        dimension of the sample space.

        For most of the statistics this class relies on
        the StatisticsType underlying class to provide 1-D methods that
        will be iterated for all the components of the N-D data. These
        lifted methods are the union of all the methods that might be
        requested to the 1-D underlying StatisticsType class, with the
        usual compile-time checks provided by the template approach.

        \test the correctness of the returned values is tested by
              checking them against numerical calculations.
    */
    template <class StatisticsType>
    class GenericSequenceStatistics {
      public:
        // typedefs
        typedef StatisticsType statistics_type;
        typedef std::vector<typename StatisticsType::value_type> value_type;
        // constructor
        GenericSequenceStatistics(Size dimension = 0);
        //! \name inspectors
        //@{
        Size size() const { return dimension_; }
        //@}
        //! \name covariance and correlation
        //@{
        //! returns the covariance Matrix
        Matrix covariance() const;
        //! returns the correlation Matrix
        Matrix correlation() const;
        //@}
        //! \name 1-D inspectors lifted from underlying statistics class
        //@{
        Size samples() const;
        Real weightSum() const;
        //@}
        //! \name N-D inspectors lifted from underlying statistics class
        //@{
        // void argument list
        std::vector<Real> mean() const;
        std::vector<Real> variance() const;
        std::vector<Real> standardDeviation() const;
        std::vector<Real> downsideVariance() const;
        std::vector<Real> downsideDeviation() const;
        std::vector<Real> semiVariance() const;
        std::vector<Real> semiDeviation() const;
        std::vector<Real> errorEstimate() const;
        std::vector<Real> skewness() const;
        std::vector<Real> kurtosis() const;
        std::vector<Real> min() const;
        std::vector<Real> max() const;

        // single argument list
        std::vector<Real> gaussianPercentile(Real y) const;
        std::vector<Real> percentile(Real y) const;

        std::vector<Real> gaussianPotentialUpside(Real percentile) const;
        std::vector<Real> potentialUpside(Real percentile) const;

        std::vector<Real> gaussianValueAtRisk(Real percentile) const;
        std::vector<Real> valueAtRisk(Real percentile) const;

        std::vector<Real> gaussianExpectedShortfall(Real percentile) const;
        std::v