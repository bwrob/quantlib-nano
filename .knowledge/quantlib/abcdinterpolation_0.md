/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Ferdinando Ametrano
 Copyright (C) 2007 Cristina Duminuco
 Copyright (C) 2007 Giorgio Facchinetti

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

/*! \file abcdinterpolation.hpp
    \brief Abcd interpolation interpolation between discrete points
*/

#ifndef quantlib_abcd_interpolation_hpp
#define quantlib_abcd_interpolation_hpp

#include <ql/math/interpolation.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/termstructures/volatility/abcd.hpp>
#include <ql/termstructures/volatility/abcdcalibration.hpp>
#include <utility>

namespace QuantLib {

    class EndCriteria;
    class OptimizationMethod;

    namespace detail {

        class AbcdCoeffHolder {
          public:
            AbcdCoeffHolder(Real a,
                            Real b,
                            Real c,
                            Real d,
                            bool aIsFixed,
                            bool bIsFixed,
                            bool cIsFixed,
                            bool dIsFixed)
            : a_(a), b_(b), c_(c), d_(d),

              error_(Null<Real>()), maxError_(Null<Real>()) {
                if (a_ != Null<Real>())
                    aIsFixed_ = aIsFixed;
                else a_ = -0.06;
                if (b_ != Null<Real>())
                    bIsFixed_ = bIsFixed;
                else b_ = 0.17;
                if (c_ != Null<Real>())
                    cIsFixed_ = cIsFixed;
                else c_ = 0.54;
                if (d_ != Null<Real>())
                    dIsFixed_ = dIsFixed;
                else d_ = 0.17;

                AbcdMathFunction::validate(a, b, c, d);
            }
            virtual ~AbcdCoeffHolder() = default;
            Real a_, b_, c_, d_;
            bool aIsFixed_ = false, bIsFixed_ = false, cIsFixed_ = false, dIsFixed_ = false;
            std::vector<Real> k_;
            Real error_, maxError_;
            EndCriteria::Type abcdEndCriteria_ = EndCriteria::None;
        };

        template <class I1, class I2>
        class AbcdInterpolationImpl final : public Interpolation::templateImpl<I1,I2>,
                                            public AbcdCoeffHolder {
          public:
            AbcdInterpolationImpl(const I1& xBegin,
                                  const I1& xEnd,
                                  const I2& yBegin,
                                  Real a,
                                  Real b,
                                  Real c,
                                  Real d,
                                  bool aIsFixed,
                                  bool bIsFixed,
                                  bool cIsFixed,
                                  bool dIsFixed,
                                  bool vegaWeighted,
                                  ext::shared_ptr<EndCriteria> endCriteria,
                                  ext::shared_ptr<OptimizationMethod> optMethod)
            : Interpolation::templateImpl<I1, I2>(xBegin, xEnd, yBegin),
              AbcdCoeffHolder(a, b, c, d, aIsFixed, bIsFixed, cIsFixed, dIsFixed),
              endCriteria_(std::move(endCriteria)), optMethod_(std::move(optMethod)),
              vegaWeighted_(vegaWeighted) {}

            void update() override {
            