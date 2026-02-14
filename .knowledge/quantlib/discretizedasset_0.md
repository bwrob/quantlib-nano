/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2001, 2002, 2003 Sadruddin Rejeb
 Copyright (C) 2004, 2005, 2006 StatPro Italia srl

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

/*! \file discretizedasset.hpp
    \brief Discretized asset classes
*/

#ifndef quantlib_discretized_asset_hpp
#define quantlib_discretized_asset_hpp

#include <ql/exercise.hpp>
#include <ql/math/comparison.hpp>
#include <ql/numericalmethod.hpp>
#include <utility>

namespace QuantLib {

    //! Discretized asset class used by numerical methods
    class DiscretizedAsset {
      public:
        DiscretizedAsset()
        : latestPreAdjustment_(QL_MAX_REAL),
          latestPostAdjustment_(QL_MAX_REAL) {}
        virtual ~DiscretizedAsset() = default;

        //! \name inspectors
        //@{
        Time time() const { return time_; }
        Time& time() { return time_; }

        const Array& values() const { return values_; }
        Array& values() { return values_; }

        const ext::shared_ptr<Lattice>& method() const {
            return method_;
        }
        //@}

        /*! \name High-level interface

            Users of discretized assets should use these methods in
            order to initialize, evolve and take the present value of
            the assets.  They call the corresponding methods in the
            Lattice interface, to which we refer for
            documentation.

            @{
        */
        void initialize(const ext::shared_ptr<Lattice>&,
                        Time t);
        void rollback(Time to);
        void partialRollback(Time to);
        Real presentValue();
        //@}

        /*! \name Low-level interface

            These methods (that developers should override when
            deriving from DiscretizedAsset) are to be used by
            numerical methods and not directly by users, with the
            exception of adjustValues(), preAdjustValues() and
            postAdjustValues() that can be used together with
            partialRollback().

            @{
        */

        /*! This method should initialize the asset values to an Array
            of the given size and with values depending on the
            particular asset.
        */
        virtual void reset(Size size) = 0;

        /*! This method will be invoked after rollback and before any
            other asset (i.e., an option on this one) has any chance to
            look at the values. For instance, payments happening at times
            already spanned by the rollback will be added here.

            This method is not virtual; derived classes must override
            the protected preAdjustValuesImpl() method instead.
        */
        void preAdjustValues();

        /*! This method will be invoked after rollback and after any
            other asset had their chance to look at the values. For
            instance, payments happening at the present time (and therefore
            not included in an option to be exercised at this time) will be
            added here.

            This method is not virtual; derived classes must override
            the protected postAdjustValuesImpl() method instead.
        */
        void postAdjustValues();

        /*! This method performs both pre- and post-adjustment */
        void adjustValues()