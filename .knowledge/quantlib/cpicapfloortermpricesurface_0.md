/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2010, 2011 Chris Kenyon

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

/*! \file cpicapfloortermpricesurface.hpp
    \brief cpi inflation cap and floor term price structure.
*/

#ifndef quantlib_cpi_capfloor_term_price_surface_hpp
#define quantlib_cpi_capfloor_term_price_surface_hpp

#include <ql/termstructures/inflationtermstructure.hpp>
#include <ql/math/interpolation.hpp>
#include <ql/math/interpolations/interpolation2d.hpp>
#include <ql/experimental/inflation/polynomial2Dspline.hpp>
#include <ql/indexes/inflationindex.hpp>


namespace QuantLib {

    //! Provides cpi cap/floor prices by interpolation and put/call parity (not cap/floor/swap* parity).
    /*! The inflation index MUST contain a ZeroInflationTermStructure as
        this is used to create ATM.  Unlike YoY price surfaces we
        assume that 1) an ATM ZeroInflationTermStructure is available
        and 2) that it is safe to use it.  This is supported by the
        fact that no stripping is required for CPI cap/floors as they
        only give one flow.

        cpi cap/floors have a single (one) flow (unlike nominal
        caps) because they observe cumulative inflation up to
        their maturity.  Options are on CPI(T)/CPI(0) but strikes
        are quoted for yearly average inflation, so require transformation
        via (1+quote)^T to obtain actual strikes.  These are consistent
        with ZCIIS quoting conventions.

        The observationLag is that for the referenced instrument prices.
        Strikes are as-quoted not as-used.
    */
    class CPICapFloorTermPriceSurface : public TermStructure {
      public:
        CPICapFloorTermPriceSurface(
            Real nominal,
            Real baseRate, // avoids an uncontrolled crash if index has no TS
            const Period& observationLag,
            const Calendar& cal, // calendar in index may not be useful
            const BusinessDayConvention& bdc,
            const DayCounter& dc,
            ext::shared_ptr<ZeroInflationIndex>  zii,
            CPI::InterpolationType interpolationType,
            Handle<YieldTermStructure> yts,
            const std::vector<Rate>& cStrikes,
            const std::vector<Rate>& fStrikes,
            const std::vector<Period>& cfMaturities,
            const Matrix& cPrice,
            const Matrix& fPrice);

        //! \name InflationTermStructure interface
        //@{
        virtual Period observationLag() const;
        virtual Frequency frequency() const;
        virtual Date baseDate() const;
        virtual Rate baseRate() const;
        //@}

        //! inspectors
        /*! \note you don't know if price() is a cap or a floor
                  without checking the ZeroInflation ATM level.
        */
        //@{
        virtual Real nominal() const;
        virtual BusinessDayConvention businessDayConvention() const;
        ext::shared_ptr<ZeroInflationIndex> zeroInflationIndex() const { return zii_; }
        //@}

        Rate atmRate(Date maturity) const;

        //! \warning you MUST remind the compiler in any descendants with the using:: mechanism
        //!          because you overload the names
        //! remember that the strikes use the quoting convention
        //@{
        virtual Real price(const Peri