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

/*! \file convexmonotoneinterpolation.hpp
    \brief convex monotone interpolation method
*/

#ifndef quantlib_convex_monotone_interpolation_hpp
#define quantlib_convex_monotone_interpolation_hpp

#include <ql/math/interpolation.hpp>
#include <map>

namespace QuantLib {

    namespace detail {
        template<class I1, class I2> class ConvexMonotoneImpl;
        class SectionHelper;
    }

    //! Convex monotone yield-curve interpolation method.
    /*! Enhances implementation of the convex monotone method
        described in "Interpolation Methods for Curve Construction" by
        Hagan & West AMF Vol 13, No2 2006.

        A setting of monotonicity = 1 and quadraticity = 0 will
        reproduce the basic Hagan/West method. However, this can
        produce excessive gradients which can mean P&L swings for some
        curves.  Setting monotonicity < 1 and/or quadraticity > 0
        produces smoother curves.  Extra enhancement to avoid negative
        values (if required) is in place.

        \ingroup interpolations
        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    template <class I1, class I2>
    class ConvexMonotoneInterpolation : public Interpolation {
        typedef std::map<Real, ext::shared_ptr<detail::SectionHelper> >
                                                                   helper_map;
      public:
        ConvexMonotoneInterpolation(const I1& xBegin, const I1& xEnd,
                                    const I2& yBegin, Real quadraticity,
                                    Real monotonicity, bool forcePositive,
                                    bool flatFinalPeriod = false,
                                    const helper_map& preExistingHelpers =
                                                               helper_map()) {
            impl_ = ext::shared_ptr<Interpolation::Impl>(
                   new detail::ConvexMonotoneImpl<I1,I2>(xBegin,
                                                         xEnd,
                                                         yBegin,
                                                         quadraticity,
                                                         monotonicity,
                                                         forcePositive,
                                                         flatFinalPeriod,
                                                         preExistingHelpers));
            impl_->update();
        }

        ConvexMonotoneInterpolation(Interpolation& interp)
        : Interpolation(interp) {}

        std::map<Real, ext::shared_ptr<detail::SectionHelper> >
        getExistingHelpers() {
            ext::shared_ptr<detail::ConvexMonotoneImpl<I1,I2> > derived =
                ext::dynamic_pointer_cast<detail::ConvexMonotoneImpl<I1,I2>,
                                            Interpolation::Impl>(impl_);
            return derived->getExistingHelpers();
        }
    };

    //! Convex-monotone interpolation factory and traits
    /*! \ingroup interpolations */
    class ConvexMonotone {
      public:
        static const bool global = true;
  