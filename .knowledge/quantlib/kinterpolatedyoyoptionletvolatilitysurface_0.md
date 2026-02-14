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

/*! \file kinterpolatedyoyoptionletvolatilitysurface.hpp
    \brief K-interpolated yoy optionlet volatility
*/

#ifndef quantlib_k_interpolated_yoy_optionlet_volatility_surface_hpp
#define quantlib_k_interpolated_yoy_optionlet_volatility_surface_hpp

#include <ql/experimental/inflation/yoyoptionletstripper.hpp>
#include <utility>

namespace QuantLib {

    //! K-interpolated YoY optionlet volatility
    /*! The stripper provides curves in the T direction along each K.
        We don't know whether this is interpolating or fitting in the
        T direction.  Our K direction interpolations are not model
        fitting.

        An alternative design would be a
        FittedYoYOptionletVolatilitySurface taking a model, e.g. SABR
        in the interest rate world.  This could use the same stripping
        in the T direction along each K.

        \bug Tests currently fail.
    */
    template<class Interpolator1D>
    class KInterpolatedYoYOptionletVolatilitySurface
        : public YoYOptionletVolatilitySurface {
      public:
        //! \name Constructor
        //! calculate the reference date based on the global evaluation date
        KInterpolatedYoYOptionletVolatilitySurface(
            Natural settlementDays,
            const Calendar&,
            BusinessDayConvention bdc,
            const DayCounter& dc,
            const Period& lag,
            const ext::shared_ptr<YoYCapFloorTermPriceSurface>& capFloorPrices,
            ext::shared_ptr<YoYInflationCapFloorEngine> pricer,
            ext::shared_ptr<YoYOptionletStripper> yoyOptionletStripper,
            Real slope,
            const Interpolator1D& interpolator = Interpolator1D(),
            VolatilityType volType = ShiftedLognormal,
            Real displacement = 0.0);

        Real minStrike() const override;
        Real maxStrike() const override;
        Date maxDate() const override;
        std::pair<std::vector<Rate>, std::vector<Volatility> > Dslice(
                                                         const Date &d) const;

      protected:
        virtual Volatility volatilityImpl(const Date &d,
                                          Rate strike) const;
        Volatility volatilityImpl(Time length, Rate strike) const override;
        virtual void performCalculations() const;

        ext::shared_ptr<YoYCapFloorTermPriceSurface> capFloorPrices_;
        ext::shared_ptr<YoYInflationCapFloorEngine> yoyInflationCouponPricer_;
        ext::shared_ptr<YoYOptionletStripper> yoyOptionletStripper_;

        mutable Interpolator1D factory1D_;
        mutable Real slope_;
        mutable bool lastDateisSet_ = false;
        mutable Date lastDate_;
        mutable Interpolation tempKinterpolation_;
        mutable std::pair<std::vector<Rate>, std::vector<Volatility> > slice_;
      private:
        void updateSlice(const Date &d) const;
    };


    // template definitions

    template <class Interpolator1D>
    KInterpolatedYoYOptionletVolatilitySurface<Interpolator1D>::
        KInterpolatedYoYOptionletVolatilitySurface(
            const Natural settlementDays,
            const Calendar& cal,
            const BusinessDayConvention bdc,
            cons