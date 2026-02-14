/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Joseph Wang
 Copyright (C) 2012 Liquidnet Holdings, Inc.

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

/*! \file garch.hpp
    \brief GARCH volatility model
*/

#ifndef quantlib_garch_volatility_model_hpp
#define quantlib_garch_volatility_model_hpp

#include <ql/volatilitymodel.hpp>
#include <ql/math/optimization/problem.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <vector>

namespace QuantLib {

    //! GARCH volatility model
    /*! Volatilities are assumed to be expressed on an annual basis.
    */
    class Garch11 : public VolatilityCompositor {
      public:
        typedef TimeSeries<Volatility> time_series;

        enum Mode {
            MomentMatchingGuess,   /*!< The initial guess is a moment
                                        matching estimates for
                                        mean(r2), acf(0), and acf(1). */
            GammaGuess,            /*!< The initial guess is an
                                        estimate of gamma based on the
                                        property:
                                        acf(i+1) = gamma*acf(i) for i > 1. */
            BestOfTwo,             /*!< The best of the two above modes */
            DoubleOptimization     /*!< Double optimization */
        };

        //! \name Constructors
        //@{
        Garch11(Real a, Real b, Real vl)
        : alpha_(a), beta_(b), gamma_(1 - a - b),
          vl_(vl), logLikelihood_(0), mode_(BestOfTwo) {}

        Garch11(const time_series& qs, Mode mode = BestOfTwo)
        : alpha_(0), beta_(0), vl_(0), logLikelihood_(0), mode_(mode) {
            calibrate(qs);
        };
        //@}

        //! \name Inspectors
        //@{
        Real alpha() const { return alpha_; }
        Real beta() const { return beta_; }
        Real omega() const { return vl_ * gamma_; }
        Real ltVol() const { return vl_; }
        Real logLikelihood() const { return logLikelihood_; }
        Mode mode() const { return mode_; }
        //@}

        //! \name VolatilityCompositor interface
        //@{
        time_series calculate(const time_series& quoteSeries) override {
            return calculate(quoteSeries, alpha(), beta(), omega());
        }
        void calibrate(const time_series& quoteSeries) override {
            const auto values = quoteSeries.values();
            calibrate(values.cbegin(), values.cend());
        }
        //@}

        //! \name Additional interface
        //@{
        static time_series calculate(const time_series& quoteSeries,
                                     Real alpha, Real beta, Real omega);

        void calibrate(const time_series& quoteSeries,
                       OptimizationMethod& method,
                       const EndCriteria& endCriteria) {
            const auto values = quoteSeries.values();
            calibrate(values.cbegin(), values.cend(),
                      method, endCriteria);
        }

        void calibrate(const time_series& quoteSeries,
                       OptimizationMethod& method,
                       const EndCriteria& endCriteria,
                       const Array& initialGuess) {
            const auto values = quoteSeries.values();
            calibrate(values.cbegin(), values.ce