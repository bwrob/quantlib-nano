/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007, 2008 Chris Kenyon
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

/*! \file interpolatedzeroinflationcurve.hpp
    \brief Inflation term structure based on the interpolation of zero rates.
*/

#ifndef quantlib_interpolated_zeroinflationcurve_hpp
#define quantlib_interpolated_zeroinflationcurve_hpp

#include <ql/termstructures/inflationtermstructure.hpp>
#include <ql/termstructures/interpolatedcurve.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <utility>

namespace QuantLib {

    //! Inflation term structure based on the interpolation of zero rates.
    /*! \ingroup inflationtermstructures */
    template<class Interpolator>
    class InterpolatedZeroInflationCurve
        : public ZeroInflationTermStructure,
          protected InterpolatedCurve<Interpolator> {
      public:
        InterpolatedZeroInflationCurve(const Date& referenceDate,
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
        //! \name ZeroInflationTermStructure Interface
        //@{
        Rate zeroRateImpl(Time t) const override;
        //@}
        mutable std::vector<Date> dates_;

        /*! Protected version for use when descendents don't want to
            (or can't) provide the points for interpolation on
            construction.
        */
        InterpolatedZeroInflationCurve(const Date& referenceDate,
                                       Date baseDate,
                                       Frequency frequency,
                                       const DayCounter& dayCounter,
                                       const ext::shared_ptr<Seasonality>& seasonality = {},
                                       const Interpolator &interpolator = Interpolator());
    };

    typedef InterpolatedZeroInflationCurve<Linear> ZeroInflationCurve;



    // template definitions

    template <class Interpolator>
    InterpolatedZeroInflationCurve<Interpolator>::InterpolatedZeroInflationCurve(
        const Date& referenceDate,
        std::vector<Date> dates,
        const std::vector<Rate>& rates,
        Frequency frequency,
        const DayCounter& dayCounter,
        const ext::shared_ptr<Seasonality>& seasonality,
        const Interpolator& interpolator)
    : ZeroInflationTermStructure(referenceDate, dates.at(0), frequency, dayCounter, seasonality),
      InterpolatedCurve<Interpolator>(std::vector<Time>(), rates, interpola