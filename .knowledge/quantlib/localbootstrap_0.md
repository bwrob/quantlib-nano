/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Simon Ibbotson

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

/*! \file localbootstrap.hpp
    \brief localised-term-structure bootstrapper for most curve types.
*/

#ifndef quantlib_local_bootstrap_hpp
#define quantlib_local_bootstrap_hpp

#include <ql/termstructures/bootstraphelper.hpp>
#include <ql/math/optimization/costfunction.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <ql/math/optimization/armijo.hpp>
#include <ql/math/optimization/levenbergmarquardt.hpp>
#include <ql/math/optimization/problem.hpp>
#include <ql/utilities/dataformatters.hpp>
#include <ql/shared_ptr.hpp>

namespace QuantLib {

    /*! \deprecated Use SimpleCostFunction instead.
                    Deprecated in version 1.40.
    */
    template <class Curve>
    class [[deprecated("Use SimpleCostFunction instead")]] PenaltyFunction : public CostFunction {
        typedef typename Curve::traits_type Traits;
        typedef typename Traits::helper helper;
        typedef
          typename std::vector< ext::shared_ptr<helper> >::const_iterator
                                                              helper_iterator;
      public:
        PenaltyFunction(Curve* curve,
                        Size initialIndex,
                        helper_iterator rateHelpersStart,
                        helper_iterator rateHelpersEnd)
        : curve_(curve), initialIndex_(initialIndex),
          localisation_(std::distance(rateHelpersStart, rateHelpersEnd)),
          rateHelpersStart_(rateHelpersStart), rateHelpersEnd_(rateHelpersEnd) {}

        Real value(const Array& x) const override;
        Array values(const Array& x) const override;

      private:
        Curve* curve_;
        Size initialIndex_;
        Size localisation_;
        helper_iterator rateHelpersStart_;
        helper_iterator rateHelpersEnd_;
    };


    //! Localised-term-structure bootstrapper for most curve types.
    /*! This algorithm enables a localised fitting for non-local
        interpolation methods.

        As in the similar class (IterativeBootstrap) the input term
        structure is solved on a number of market instruments which
        are passed as a vector of handles to BootstrapHelper
        instances. Their maturities mark the boundaries of the
        interpolated segments.

        Unlike the IterativeBootstrap class, the solution for each
        interpolated segment is derived using a local
        approximation. This restricts the risk profile s.t.  the risk
        is localised. Therefore, we obtain a local IR risk profile
        whilst using a smoother interpolation method. Particularly
        good for the convex-monotone spline method.
    */
    template <class Curve>
    class LocalBootstrap {
        typedef typename Curve::traits_type Traits;
        typedef typename Curve::interpolator_type Interpolator;
      public:
        LocalBootstrap(Size localisation = 2,
                       bool forcePositive = true,
                       Real accuracy = Null<Real>());
        void setup(Curve* ts);
        void calculate() const;

      private:
        mutable bool validCurve_ = false;
        Curve* ts_;
        Size localisation_;
        bool forcePositive_;
        Real accuracy_;
    };



    // templ
