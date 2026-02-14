/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2002, 2003, 2008, 2009 Ferdinando Ametrano
 Copyright (C) 2004, 2007, 2008 StatPro Italia srl

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

/*! \file loginterpolation.hpp
    \brief log-linear and log-cubic interpolation between discrete points
*/

#ifndef quantlib_log_interpolation_hpp
#define quantlib_log_interpolation_hpp

#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/math/interpolations/cubicinterpolation.hpp>
#include <ql/math/interpolations/mixedinterpolation.hpp>
#include <ql/utilities/dataformatters.hpp>

namespace QuantLib {

    namespace detail {
        template <class I1, class I2> class LogInterpolationImpl;
    }

    //! %log-linear interpolation between discrete points
    /*! \ingroup interpolations
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class LogLinearInterpolation : public Interpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        LogLinearInterpolation(const I1& xBegin, const I1& xEnd,
                               const I2& yBegin) {
            impl_ = ext::make_shared<detail::LogInterpolationImpl<I1, I2>>(
                xBegin, xEnd, yBegin, Linear());
            impl_->update();
        }
    };

    //! log-linear interpolation factory and traits
    /*! \ingroup interpolations */
    class LogLinear {
      public:
        template <class I1, class I2>
        Interpolation interpolate(const I1& xBegin, const I1& xEnd,
                                  const I2& yBegin) const {
            return LogLinearInterpolation(xBegin, xEnd, yBegin);
        }
        static const bool global = false;
        static const Size requiredPoints = 2;
    };

    //! %log-cubic interpolation between discrete points
    /*! \ingroup interpolations */
    class LogCubicInterpolation : public Interpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        LogCubicInterpolation(const I1& xBegin, const I1& xEnd,
                              const I2& yBegin,
                              CubicInterpolation::DerivativeApprox da,
                              bool monotonic,
                              CubicInterpolation::BoundaryCondition leftC,
                              Real leftConditionValue,
                              CubicInterpolation::BoundaryCondition rightC,
                              Real rightConditionValue) {
            impl_ = ext::make_shared<detail::LogInterpolationImpl<I1, I2>>(
                xBegin, xEnd, yBegin,
                Cubic(da, monotonic,
                      leftC, leftConditionValue,
                      rightC, rightConditionValue));
            impl_->update();
        }
    };

    //! log-cubic interpolation factory and traits
    /*! \ingroup interpolations */
    class LogCubic {
      public:
        LogCubic(CubicInterpolation::DerivativeApprox da,
                  bool monotonic = true,
                  CubicInterpolation::BoundaryCondition leftCondition
                      = CubicInterpolation::SecondDerivative,
                  Real leftConditionValue = 0.0,
    