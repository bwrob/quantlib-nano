/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Chris Kenyon
 Copyright (C) 2021 Ralf Konrad Eckel

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

/*! \file inflationindex.hpp
    \brief base classes for inflation indexes
*/

#ifndef quantlib_inflation_index_hpp
#define quantlib_inflation_index_hpp

#include <ql/currency.hpp>
#include <ql/handle.hpp>
#include <ql/index.hpp>
#include <ql/indexes/region.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>

namespace QuantLib {

    class ZeroInflationIndex;
    class YoYInflationIndex;

    struct CPI {

        //! when you observe an index, how do you interpolate between fixings?
        enum InterpolationType {
            AsIndex, //!< same interpolation as index
            Flat,    //!< flat from previous fixing
            Linear   //!< linearly between bracketing fixings
        };

        //! interpolated inflation fixing
        /*! \param index              The index whose fixing should be retrieved
            \param date               The date without lag; usually, the payment
                                      date for some inflation-based coupon.
            \param observationLag     The observation lag to be subtracted from the
                                      passed date; for instance, if the passed date is
                                      in May and the lag is three months, the inflation
                                      fixing from February (and March, in case of
                                      interpolation) will be observed.
            \param interpolationType  The interpolation type (flat or linear)
        */
        static Real laggedFixing(const ext::shared_ptr<ZeroInflationIndex>& index,
                                 const Date& date,
                                 const Period& observationLag,
                                 InterpolationType interpolationType);


        //! interpolated year-on-year inflation rate
        /*! \param index              The index whose fixing should be retrieved
            \param date               The date without lag; usually, the payment
                                      date for some inflation-based coupon.
            \param observationLag     The observation lag to be subtracted from the
                                      passed date; for instance, if the passed date is
                                      in May and the lag is three months, the year-on-year
                                      rate from February (and March, in case of
                                      interpolation) will be observed.
            \param interpolationType  The interpolation type (flat or linear)
        */
        static Real laggedYoYRate(const ext::shared_ptr<YoYInflationIndex>& index,
                                  const Date& date,
                                  const Period& observationLag,
                                  InterpolationType interpolationType);
    };


    //! Base class for inflation-rate indexes,
    class InflationIndex : public Index {
      public:
        InflationIndex(std::string familyName,
                       Region region,
                       bool revised,
                       Frequency frequency,
                       const Period& availabilitiyLag
