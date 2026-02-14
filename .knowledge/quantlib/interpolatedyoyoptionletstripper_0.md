/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Chris Kenyon

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

/*! \file interpolatedyoyoptionletstripper.hpp
    \brief interpolated yoy inflation-cap stripping
*/

#ifndef quantlib_interpolated_yoy_optionlet_stripper_hpp
#define quantlib_interpolated_yoy_optionlet_stripper_hpp

#include <ql/experimental/inflation/genericindexes.hpp>
#include <ql/experimental/inflation/piecewiseyoyoptionletvolatility.hpp>
#include <ql/experimental/inflation/yoyoptionlethelpers.hpp>
#include <ql/experimental/inflation/yoyoptionletstripper.hpp>
#include <ql/instruments/makeyoyinflationcapfloor.hpp>
#include <ql/math/solvers1d/brent.hpp>
#include <utility>


namespace QuantLib {

    /*! The interpolated version interpolates along each K (as opposed
        to fitting a model, say).

        \bug Tests currently fail.
    */
    template <class Interpolator1D>
    class InterpolatedYoYOptionletStripper : public YoYOptionletStripper {
      public:

        //! YoYOptionletStripper interface
        //@{
        void initialize(const ext::shared_ptr<YoYCapFloorTermPriceSurface>&,
                        const ext::shared_ptr<YoYInflationCapFloorEngine>&,
                        Real slope) const override;
        Rate minStrike() const override { return YoYCapFloorTermPriceSurface_->strikes().front(); }
        Rate maxStrike() const override { return YoYCapFloorTermPriceSurface_->strikes().back(); }
        std::vector<Rate> strikes() const override {
            return YoYCapFloorTermPriceSurface_->strikes();
        }
        std::pair<std::vector<Rate>, std::vector<Volatility> > slice(const Date& d) const override;
        //@}

      protected:
        mutable std::vector<ext::shared_ptr<YoYOptionletVolatilitySurface> > volCurves_;

        // used to set up the first point on each vol curve
        // using assumptions on unobserved vols at start
        class ObjectiveFunction {
          public:
            ObjectiveFunction(YoYInflationCapFloor::Type type,
                              Real slope,
                              Rate K,
                              Period& lag,
                              Natural fixingDays,
                              const ext::shared_ptr<YoYInflationIndex>& anIndex,
                              const ext::shared_ptr<YoYCapFloorTermPriceSurface>&,
                              ext::shared_ptr<YoYInflationCapFloorEngine> p,
                              Real priceToMatch);
            Real operator()(Volatility guess) const;
          protected:
            Real slope_;
            Rate K_;
            Frequency frequency_;
            bool indexIsInterpolated_;
            std::vector<Time> tvec_;
            std::vector<Date> dvec_;
            mutable std::vector<Volatility> vvec_;
            ext::shared_ptr<YoYInflationCapFloor> capfloor_;
            Real priceToMatch_;
            ext::shared_ptr<YoYCapFloorTermPriceSurface> surf_;
            Period lag_;
            ext::shared_ptr<YoYInflationCapFloorEngine> p_;
        };
    };


    // template definitions

    template <class Interpolator1D>
    InterpolatedYoYOptionletStripper<Interpolator1D>::ObjectiveFunction::ObjectiveFunction(
        YoYInflationCapFloor::Type type,
        Real slope,
        Rate K,
 