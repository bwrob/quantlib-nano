/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
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

/*! \file riskstatistics.hpp
    \brief empirical-distribution risk measures
*/

#ifndef quantlib_risk_statistics_h
#define quantlib_risk_statistics_h

#include <ql/math/statistics/gaussianstatistics.hpp>

namespace QuantLib {

    //! empirical-distribution risk measures
    /*! This class wraps a somewhat generic statistic tool and adds
        a number of risk measures (e.g.: value-at-risk, expected
        shortfall, etc.) based on the data distribution as reported by
        the underlying statistic tool.

        \todo add historical annualized volatility

    */
    template <class S>
    class GenericRiskStatistics : public S {
      public:
        typedef typename S::value_type value_type;

        /*! returns the variance of observations below the mean,
            \f[ \frac{N}{N-1}
                \mathrm{E}\left[ (x-\langle x \rangle)^2 \;|\;
                                  x < \langle x \rangle \right]. \f]

            See Markowitz (1959).
        */
        Real semiVariance() const;

        /*! returns the semi deviation, defined as the
            square root of the semi variance.
        */
        Real semiDeviation() const;

        /*! returns the variance of observations below 0.0,
            \f[ \frac{N}{N-1}
                \mathrm{E}\left[ x^2 \;|\; x < 0\right]. \f]
        */
        Real downsideVariance() const;

        /*! returns the downside deviation, defined as the
            square root of the downside variance.
        */
        Real downsideDeviation() const;

        /*! returns the variance of observations below target,
            \f[ \frac{N}{N-1}
                \mathrm{E}\left[ (x-t)^2 \;|\;
                                  x < t \right]. \f]

            See Dembo and Freeman, "The Rules Of Risk", Wiley (2001).
        */
        Real regret(Real target) const;

        //! potential upside (the reciprocal of VAR) at a given percentile
        Real potentialUpside(Real percentile) const;

        //! value-at-risk at a given percentile
        Real valueAtRisk(Real percentile) const;

        //! expected shortfall at a given percentile
        /*! returns the expected loss in case that the loss exceeded
            a VaR threshold,

            \f[ \mathrm{E}\left[ x \;|\; x < \mathrm{VaR}(p) \right], \f]

            that is the average of observations below the
            given percentile \f$ p \f$.
            Also know as conditional value-at-risk.

            See Artzner, Delbaen, Eber and Heath,
            "Coherent measures of risk", Mathematical Finance 9 (1999)
        */
        Real expectedShortfall(Real percentile) const;

        /*! probability of missing the given target, defined as
            \f[ \mathrm{E}\left[ \Theta \;|\; (-\infty,\infty) \right] \f]
            where
            \f[ \Theta(x) = \left\{
                \begin{array}{ll}
                1 & x < t \\
                0 & x \geq t
                \end{array}
                \right. \f]
        */
        Real shortfall(Real target) const;

        /*! averaged shortfallness, defined as
            \f[ \mathrm{E}\left[ t-x \;|\; x<t \right] \f]
        */
        Real averageShortfall(Real target) c
