/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Chris Kenyon
 Copyright (C) 2009 Bernd Engelmann

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

/*! \file yoycapfloortermpricesurface.hpp
    \brief yoy inflation cap and floor term-price structure
*/

#ifndef quantlib_yoy_capfloor_term_price_surface_hpp
#define quantlib_yoy_capfloor_term_price_surface_hpp

#include <ql/indexes/inflationindex.hpp>
#include <ql/termstructures/inflation/piecewiseyoyinflationcurve.hpp>
#include <ql/termstructures/inflation/inflationhelpers.hpp>
#include <ql/experimental/inflation/polynomial2Dspline.hpp>
#include <cmath>

namespace QuantLib {

    //! Abstract base class, inheriting from InflationTermStructure
    /*! Since this can create a yoy term structure it does take
        a YoY index.

        \todo deal with index interpolation.
    */
    class YoYCapFloorTermPriceSurface : public TermStructure {
      public:
        YoYCapFloorTermPriceSurface(Natural fixingDays,
                                    const Period& yyLag,
                                    const ext::shared_ptr<YoYInflationIndex>& yii,
                                    CPI::InterpolationType interpolation,
                                    Handle<YieldTermStructure> nominal,
                                    const DayCounter& dc,
                                    const Calendar& cal,
                                    const BusinessDayConvention& bdc,
                                    const std::vector<Rate>& cStrikes,
                                    const std::vector<Rate>& fStrikes,
                                    const std::vector<Period>& cfMaturities,
                                    const Matrix& cPrice,
                                    const Matrix& fPrice);

        bool indexIsInterpolated() const;
        virtual Period observationLag() const;
        virtual Frequency frequency() const;

        //! atm yoy swaps from put-call parity on cap/floor data
        /*! uses interpolation (on surface price data), yearly maturities. */
        virtual std::pair<std::vector<Time>, std::vector<Rate> >
        atmYoYSwapTimeRates() const = 0;
        virtual std::pair<std::vector<Date>, std::vector<Rate> >
        atmYoYSwapDateRates() const = 0;

        //! derived from yoy swap rates
        virtual ext::shared_ptr<YoYInflationTermStructure> YoYTS() const = 0;
        //! index yoy is based on
        ext::shared_ptr<YoYInflationIndex> yoyIndex() const { return yoyIndex_; }

        //! inspectors
        /*! \note you don't know if price() is a cap or a floor
                  without checking the YoYSwapATM level.
            \note atm cap/floor prices are generally
                  inaccurate because they are from extrapolation
                  and intersection.
        */
        //@{
        virtual BusinessDayConvention businessDayConvention() const {return bdc_;}
        virtual Natural fixingDays() const {return fixingDays_;}
        virtual Date baseDate() const = 0;
        virtual Real price(const Date& d, Rate k) const = 0;
        virtual Real capPrice(const Date& d, Rate k) const = 0;
        virtual Real floorPrice(const Date& d, Rate k) const = 0;
        virtual Rate atmYoYSwapRate(const Date &d,
                                    bool extrapo
