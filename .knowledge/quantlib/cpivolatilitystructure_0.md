/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009, 2011 Chris Kenyon

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

/*! \file cpivolatilitystructure.hpp
    \brief zero inflation (i.e. CPI/RPI/HICP/etc.) volatility structures
 */

#ifndef quantlib_cpi_volatility_structure_hpp
#define quantlib_cpi_volatility_structure_hpp

#include <ql/termstructures/voltermstructure.hpp>

namespace QuantLib {

    //! zero inflation (i.e. CPI/RPI/HICP/etc.) volatility structures
    /*! Abstract interface. CPI volatility is always with respect to
        some base date.  Also deal with lagged observations of an index
        with a (usually different) availability lag.
    */
    class CPIVolatilitySurface : public VolatilityTermStructure {
      public:
        /*! calculates the reference date based on the global
            evaluation date.
        */
        CPIVolatilitySurface(Natural settlementDays,
                             const Calendar&,
                             BusinessDayConvention bdc,
                             const DayCounter& dc,
                             const Period& observationLag,
                             Frequency frequency,
                             bool indexIsInterpolated);

        //! \name Volatility
        /*! by default, inflation is observed with the lag
            of the term structure.

            Because inflation is highly linked to dates (for
            interpolation, periods, etc) time-based overload of the
            methods are not provided.
        */
        //@{
        //! Returns the volatility for a given maturity date and strike rate.
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

        //! Returns the total integrated variance for a given exercise
        //! date and strike rate.
        /*! Total integrated variance is useful because it scales out
            t for the optionlet pricing formulae.  Note that it is
            called "total" because the surface does not know whether
            it represents Black, Bachelier or Displaced Diffusion
            variance.  These are virtual so alternate connections
            between const vol and total var are possible.
        */
        virtual Volatility totalVariance(const Date& exerciseDate,
                                         Rate strike,
                                         const Period &obsLag = Period(-1,Days),
                                         bool extrapolate = false) const;
        //! returns the total integrated variance for a given option
        //! tenor and strike rate.
        virtual Volatility totalVaria