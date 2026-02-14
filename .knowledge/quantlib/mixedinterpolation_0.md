/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2010 Ferdinando Ametrano

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

/*! \file mixedinterpolation.hpp
    \brief mixed interpolation between discrete points
*/

#ifndef quantlib_mixed_interpolation_hpp
#define quantlib_mixed_interpolation_hpp

#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/math/interpolations/cubicinterpolation.hpp>
#include <ql/utilities/dataformatters.hpp>

namespace QuantLib {

    namespace detail {

        template <class I1, class I2>
        class MixedInterpolationImpl;

    }


    struct MixedInterpolation {
        enum Behavior {
            ShareRanges,  /*!< Define both interpolations over the
                               whole range defined by the passed
                               iterators. This is the default
                               behavior. */
            SplitRanges   /*!< Define the first interpolation over the
                               first part of the range, and the second
                               interpolation over the second part. */
        };
    };

    //! mixed linear/cubic interpolation between discrete points
    /*! \ingroup interpolations
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class MixedLinearCubicInterpolation : public Interpolation {
      public:
        /*! \pre the \f$ x \f$ values must be sorted. */
        template <class I1, class I2>
        MixedLinearCubicInterpolation(const I1& xBegin, const I1& xEnd,
                                      const I2& yBegin, Size n,
                                      MixedInterpolation::Behavior behavior,
                                      CubicInterpolation::DerivativeApprox da,
                                      bool monotonic,
                                      CubicInterpolation::BoundaryCondition leftC,
                                      Real leftConditionValue,
                                      CubicInterpolation::BoundaryCondition rightC,
                                      Real rightConditionValue) {
            impl_ = ext::make_shared<detail::MixedInterpolationImpl<I1, I2>>(
                xBegin, xEnd, yBegin, n, behavior,
                Linear(),
                Cubic(da, monotonic,
                      leftC, leftConditionValue,
                      rightC, rightConditionValue));
            impl_->update();
        }
    };

    //! mixed linear/cubic interpolation factory and traits
    /*! \ingroup interpolations */
    class MixedLinearCubic {
      public:
        MixedLinearCubic(Size n,
                         MixedInterpolation::Behavior behavior,
                         CubicInterpolation::DerivativeApprox da,
                         bool monotonic = true,
                         CubicInterpolation::BoundaryCondition leftCondition
                             = CubicInterpolation::SecondDerivative,
                         Real leftConditionValue = 0.0,
                         CubicInterpolation::BoundaryCondition rightCondition
                             = CubicInterpolation::SecondDerivative,
                         Real rightConditionValue = 0.0)
        : n_(n), behavior_(behavior), da_(da), monoto
