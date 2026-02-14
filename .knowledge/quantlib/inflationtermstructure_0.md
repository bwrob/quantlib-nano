/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007, 2009 Chris Kenyon

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

/*! \file inflationtermstructure.hpp
    \brief Base classes for inflation term structures.
*/

#ifndef quantlib_inflation_termstructure_hpp
#define quantlib_inflation_termstructure_hpp

#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/inflation/seasonality.hpp>

namespace QuantLib {

    class InflationIndex;

    //! Interface for inflation term structures.
    /*! \ingroup inflationtermstructures */
    class InflationTermStructure : public TermStructure {
      public:
        //! \name Constructors
        //@{
        InflationTermStructure(Date baseDate,
                               Frequency frequency,
                               const DayCounter& dayCounter = DayCounter(),
                               ext::shared_ptr<Seasonality> seasonality = {},
                               Rate baseRate = Null<Rate>());

        InflationTermStructure(const Date& referenceDate,
                               Date baseDate,
                               Frequency frequency,
                               const DayCounter& dayCounter = DayCounter(),
                               ext::shared_ptr<Seasonality> seasonality = {},
                               Rate baseRate = Null<Rate>());

        InflationTermStructure(Natural settlementDays,
                               const Calendar& calendar,
                               Date baseDate,
                               Frequency frequency,
                               const DayCounter& dayCounter = DayCounter(),
                               ext::shared_ptr<Seasonality> seasonality = {},
                               Rate baseRate = Null<Rate>());
        //@}

        QL_DEPRECATED_DISABLE_WARNING
        ~InflationTermStructure() override = default;
        QL_DEPRECATED_ENABLE_WARNING

        //! \name Inflation interface
        //@{
        /*! \deprecated Do not use; inflation curves always have an explicit
                        base date now.
                        Deprecated in version 1.39.
        */
        [[deprecated("Do not use; inflation curves always have an explicit base date now.")]]
        virtual Period observationLag() const;

        virtual Frequency frequency() const;
        virtual Rate baseRate() const;

        //! minimum (base) date
        /*! The last date for which we have information. */
        virtual Date baseDate() const;

        /*! \deprecated Do not use; inflation curves always have an explicit
                        base date now.
                        Deprecated in version 1.39.
        */
        [[deprecated("Do not use; inflation curves always have an explicit base date now.")]]
        bool hasExplicitBaseDate() const {
            return true;
        }
        //@}

        //! \name Seasonality
        //@{
        void setSeasonality(const ext::shared_ptr<Seasonality>& seasonality);
        ext::shared_ptr<Seasonality> seasonality() const;
        bool hasSeasonality() const;
        //@}

      protected:
        void checkRange(const Date&,
                        bool extrapolate) const;
        void checkRange(Time t,
                        bool extrapolate) const;

        ex
