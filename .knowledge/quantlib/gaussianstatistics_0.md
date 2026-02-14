/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003 Ferdinando Ametrano
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl

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

/*! \file gaussianstatistics.hpp
    \brief statistics tool for gaussian-assumption risk measures
*/

#ifndef quantlib_gaussian_statistics_h
#define quantlib_gaussian_statistics_h

#include <ql/math/distributions/normaldistribution.hpp>
#include <ql/math/statistics/generalstatistics.hpp>

namespace QuantLib {

    //! Statistics tool for gaussian-assumption risk measures
    /*! This class wraps a somewhat generic statistic tool and adds
        a number of gaussian risk measures (e.g.: value-at-risk, expected
        shortfall, etc.) based on the mean and variance provided by
        the underlying statistic tool.
    */
    template<class Stat>
    class GenericGaussianStatistics : public Stat {
      public:
        typedef typename Stat::value_type value_type;
        GenericGaussianStatistics() = default;
        explicit GenericGaussianStatistics(const Stat& s) : Stat(s) {}
        //! \name Gaussian risk measures
        //@{
        /*! returns the downside variance, defined as
            \f[ \frac{N}{N-1} \times \frac{ \sum_{i=1}^{N}
                \theta \times x_i^{2}}{ \sum_{i=1}^{N} w_i} \f],
            where \f$ \theta \f$ = 0 if x > 0 and
            \f$ \theta \f$ =1 if x <0
        */
        Real gaussianDownsideVariance() const {
            return gaussianRegret(0.0);
        }

        /*! returns the downside deviation, defined as the
            square root of the downside variance.
        */
        Real gaussianDownsideDeviation() const {
            return std::sqrt(gaussianDownsideVariance());
        }

        /*! returns the variance of observations below target
            \f[ \frac{\sum w_i (min(0, x_i-target))^2 }{\sum w_i}. \f]

            See Dembo, Freeman "The Rules Of Risk", Wiley (2001)
        */
        Real gaussianRegret(Real target) const;


        /*! gaussian-assumption y-th percentile, defined as the value x
            such that \f[ y = \frac{1}{\sqrt{2 \pi}}
                                      \int_{-\infty}^{x} \exp (-u^2/2) du \f]
        */
        Real gaussianPercentile(Real percentile) const;
        Real gaussianTopPercentile(Real percentile) const;

        //! gaussian-assumption Potential-Upside at a given percentile
        Real gaussianPotentialUpside(Real percentile) const;

        //! gaussian-assumption Value-At-Risk at a given percentile
        Real gaussianValueAtRisk(Real percentile) const;

        //! gaussian-assumption Expected Shortfall at a given percentile
        /*! Assuming a gaussian distribution it
            returns the expected loss in case that the loss exceeded
            a VaR threshold,

            \f[ \mathrm{E}\left[ x \;|\; x < \mathrm{VaR}(p) \right], \f]

            that is the average of observations below the
            given percentile \f$ p \f$.
            Also know as conditional value-at-risk.

            See Artzner, Delbaen, Eber and Heath,
            "Coherent measures of risk", Mathematical Finance 9 (1999)
        */
        Real gaussianExpectedShortfall(Real percentile) const;

        //! gaussian-assumption Shortfall (observations below target)
        Real gaus
