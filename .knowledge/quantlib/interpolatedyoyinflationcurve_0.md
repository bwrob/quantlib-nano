/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007, 2008, 2009 Chris Kenyon
 Copyright (C) 2009 StatPro Italia srl

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

/*! \file interpolatedyoyinflationcurve.hpp
    \brief Inflation term structure based on the interpolation of
           year-on-year rates.
*/

#ifndef quantlib_interpolated_yoy_inflationcurve_hpp
#define quantlib_interpolated_yoy_inflationcurve_hpp

#include <ql/termstructures/inflationtermstructure.hpp>
#include <ql/termstructures/interpolatedcurve.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <utility>

namespace QuantLib {

    //! Inflation term structure based on interpolated year-on-year rates
    /*! \note The provided rates are not YY inflation-swap quotes.

        \ingroup inflationtermstructures
    */
    template<class Interpolator>
    class InterpolatedYoYInflationCurve
        : public YoYInflationTermStructure,
          protected InterpolatedCurve<Interpolator> {
      public:
        InterpolatedYoYInflationCurve(const Date& referenceDate,
                                      std::vector<Date> dates,
                                      const std::vector<Rate>& rates,
                                      Frequency frequency,
                                      const DayCounter& dayCounter,
                                      const ext::shared_ptr<Seasonality>& seasonality = {},
                                      const Interpolator& interpolator = Interpolator());

        //! \name InflationTermStructure interface
        //@{
        Date maxDate() const override;
        //@}

        //! \name Inspectors
        //@{
        const std::vector<Date>& dates() const;
        const std::vector<Time>& times() const;
        const std::vector<Real>& data() const;
        const std::vector<Rate>& rates() const;
        std::vector<std::pair<Date,Rate> > nodes() const;
        //@}

      protected:
        //! \name YoYInflationTermStructure interface
        //@{
        Rate yoyRateImpl(Time t) const override;
        //@}
        mutable std::vector<Date> dates_;

        /*! Protected version for use when descendents don't want to
            (or can't) provide the points for interpolation on
            construction.
        */
        InterpolatedYoYInflationCurve(const Date& referenceDate,
                                      Date baseDate,
                                      Rate baseYoYRate,
                                      Frequency frequency,
                                      const DayCounter& dayCounter,
                                      const ext::shared_ptr<Seasonality>& seasonality = {},
                                      const Interpolator& interpolator = Interpolator());
    };

    typedef InterpolatedYoYInflationCurve<Linear> YoYInflationCurve;



    // template definitions

    template <class Interpolator>
    InterpolatedYoYInflationCurve<Interpolator>::InterpolatedYoYInflationCurve(
        const Date& referenceDate,
        std::vector<Date> dates,
        const std::vector<Rate>& rates,
        Frequency frequency,
        const DayCounter& dayCounter,
        const ext::shared_ptr<Seasonality>& seasonality,
        const Interpolator& interpolator)
    : YoYInflationTermStructure(referenceDa