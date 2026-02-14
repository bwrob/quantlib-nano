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

/*! \file forwardrateagreement.hpp
    \brief forward rate agreement
*/

#ifndef quantlib_forward_rate_agreement_hpp
#define quantlib_forward_rate_agreement_hpp

#include <ql/instruments/forward.hpp>

namespace QuantLib {

    class IborIndex;

    //! %Forward rate agreement (FRA) class
    /*! 1. Unlike the forward contract conventions on carryable
           financial assets (stocks, bonds, commodities), the
           valueDate for a FRA is taken to be the day when the forward
           loan or deposit begins and when full settlement takes place
           (based on the NPV of the contract on that date).
           maturityDate is the date when the forward loan or deposit
           ends. In fact, the FRA settles and expires on the
           valueDate, not on the (later) maturityDate. It follows that
           (maturityDate - valueDate) is the tenor/term of the
           underlying loan or deposit

        2. Choose position type = Long for an "FRA purchase" (future
           long loan, short deposit [borrower])

        3. Choose position type = Short for an "FRA sale" (future short
           loan, long deposit [lender])

        <b>Example: </b>
        \link FRA.cpp
        valuation of a forward-rate agreement
        \endlink

        \todo Add preconditions and tests

        \todo Differentiate between BBA (British)/AFB (French)
              [assumed here] and ABA (Australian) banker conventions
              in the calculations.

        \warning This class still needs to be rigorously tested

        \ingroup instruments
    */
    class ForwardRateAgreement: public Instrument {
      public:
        /*! When using this constructor, the forward rate will be
            forecast by the passed index.  This corresponds to
            useIndexedCoupon=true in the FraRateHelper class.
        */
        ForwardRateAgreement(
            const ext::shared_ptr<IborIndex>& index,
            const Date& valueDate,
            Position::Type type,
            Rate strikeForwardRate,
            Real notionalAmount,
            Handle<YieldTermStructure> discountCurve = {});

        /*! When using this constructor, a par-rate approximation will
            be used, i.e., the forward rate will be forecast from
            value date to maturity date by the forecast curve
            contained in the index.  This corresponds to
            useIndexedCoupon=false in the FraRateHelper class.
        */
        ForwardRateAgreement(
            const ext::shared_ptr<IborIndex>& index,
            const Date& valueDate,
            const Date& maturityDate,
            Position::Type type,
            Rate strikeForwardRate,
            Real notionalAmount,
            Handle<YieldTermStructure> discountCurve = {});

        //! \name Calculations
        //@{
        //! A FRA expires/settles on the value date
        bool isExpired() const override;
        //! The payoff on the value date
        Real amount() const;

        const Calendar& calendar() const;
        BusinessDayConvention businessDayConvention() const;
        const DayCounter& dayCounter() const;
        //! term structure relevant to the contract (e.g. repo curve)
