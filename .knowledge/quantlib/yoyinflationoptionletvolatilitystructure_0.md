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

/*! \file yoyinflationoptionletvolatilitystructure.hpp
    \brief yoy inflation volatility structures
 */

#ifndef quantlib_yoy_optionlet_volatility_structures_hpp
#define quantlib_yoy_optionlet_volatility_structures_hpp

#include <ql/termstructures/voltermstructure.hpp>
#include <ql/termstructures/volatility/volatilitytype.hpp>
#include <ql/math/interpolation.hpp>
#include <ql/time/calendars/target.hpp>
#include <ql/quote.hpp>

namespace QuantLib {

    /*! Abstract interface ... no data, only results.

        Basically used to change the BlackVariance() methods to
        totalVariance.  Also deal with lagged observations of an index
        with a (usually different) availability lag.
    */
    class YoYOptionletVolatilitySurface : public VolatilityTermStructure {
    public:
        //! \name Constructor
        //! calculate the reference date based on the global evaluation date
        YoYOptionletVolatilitySurface(Natural settlementDays,
                                      const Calendar&,
                                      BusinessDayConvention bdc,
                                      const DayCounter& dc,
                                      const Period& observationLag,
                                      Frequency frequency,
                                      bool indexIsInterpolated,
                                      VolatilityType volType = ShiftedLognormal,
                                      Real displacement = 0.0);

        ~YoYOptionletVolatilitySurface() override = default;

        //! \name Volatility (only)
        //@{
        //! Returns the volatility for a given maturity date and strike rate
        //! that observes inflation, by default, with the observation lag
        //! of the term structure.
        //! Because inflation is highly linked to dates (for interpolation, periods, etc)
        //! we do NOT provide a time version.
        Volatility volatility(const Date& maturityDate,
                              Rate strike,
                              const Period &obsLag = Period(-1,Days),
                              bool extrapolate = false) const;
        //! returns the volatility for a given option tenor and strike rate
        Volatility volatility(const Period& optionTenor,
                              Rate strike,
                              const Period &obsLag = Period(-1,Days),
                              bool extrapolate = false) const;
        /*! Returns the volatility for a given time and strike rate. No adjustments
          due to lags and interpolation are applied to the input time. */
        Volatility volatility(Time time, Rate strike) const;

        //! Returns the volatility type
        virtual VolatilityType volatilityType() const { return volType_; }
        //! Returns the displacement for lognormal volatilities
        virtual Real displacement() const { return displacement_; }

        //! Returns the total integrated variance for a given exercise date and strike rate.
        /*! Total integrated variance is useful because it scales out
         t for the optionlet pricing formulae.  Note that it is
         called "total" because the surface does