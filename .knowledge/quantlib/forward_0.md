/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Allen Kuo

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

/*! \file forward.hpp
    \brief Base forward class
*/

#ifndef quantlib_forward_hpp
#define quantlib_forward_hpp

#include <ql/instrument.hpp>
#include <ql/position.hpp>
#include <ql/time/calendar.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/interestrate.hpp>
#include <ql/types.hpp>
#include <ql/handle.hpp>
#include <ql/payoff.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>

namespace QuantLib {

    //! Abstract base forward class
    /*! Derived classes must implement the virtual functions
        spotValue() (NPV or spot price) and spotIncome() associated
        with the specific relevant underlying (e.g. bond, stock,
        commodity, loan/deposit). These functions must be used to set the
        protected member variables underlyingSpotValue_ and
        underlyingIncome_ within performCalculations() in the derived
        class before the base-class implementation is called.

        spotIncome() refers generically to the present value of
        coupons, dividends or storage costs.

        discountCurve_ is the curve used to discount forward contract
        cash flows back to the evaluation day, as well as to obtain
        forward values for spot values/prices.

        incomeDiscountCurve_, which for generality is not
        automatically set to the discountCurve_, is the curve used to
        discount future income/dividends/storage-costs etc back to the
        evaluation date.

        \todo Add preconditions and tests

        \warning This class still needs to be rigorously tested

        \ingroup instruments
    */
    class Forward : public Instrument {
      public:
        //! \name Inspectors
        //@{
        virtual Date settlementDate() const;
        const Calendar& calendar() const;
        BusinessDayConvention businessDayConvention() const;
        const DayCounter& dayCounter() const;
        //! term structure relevant to the contract (e.g. repo curve)
        Handle<YieldTermStructure> discountCurve() const;
        //! term structure that discounts the underlying's income cash flows
        Handle<YieldTermStructure> incomeDiscountCurve() const;
        //! returns whether the instrument is still tradable.
        bool isExpired() const override;
        //@}

        //! returns spot value/price of an underlying financial instrument
        virtual Real spotValue() const = 0;
        //! NPV of income/dividends/storage-costs etc. of underlying instrument
        virtual Real spotIncome(const Handle<YieldTermStructure>&
                                               incomeDiscountCurve) const = 0;

        //! \name Calculations
        //@{
        //! forward value/price of underlying, discounting income/dividends
        /*! \note if this is a bond forward price, is must be a dirty
                  forward price.
        */
        virtual Real forwardValue() const;

        /*! Simple yield calculation based on underlying spot and
            forward values, taking into account underlying income.
            When \f$ t>0 \f$, call with:
            underlyingSpotValue=spotValue(t),
            forwardValue=strikePrice, to get current yield. For a
            repo, if \f$ t=0 \f$, i