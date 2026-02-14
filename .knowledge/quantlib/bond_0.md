/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2004 Jeff Yu
 Copyright (C) 2004 M-Dimension Consulting Inc.
 Copyright (C) 2005, 2006, 2007, 2008 StatPro Italia srl
 Copyright (C) 2007, 2008, 2009 Ferdinando Ametrano
 Copyright (C) 2007 Chiara Fornarola
 Copyright (C) 2008 Simon Ibbotson

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

/*! \file bond.hpp
    \brief concrete bond class
*/

#ifndef quantlib_bond_hpp
#define quantlib_bond_hpp

#include <ql/instrument.hpp>

#include <ql/time/calendar.hpp>
#include <ql/cashflow.hpp>
#include <ql/compounding.hpp>

#include <vector>

namespace QuantLib {

    class DayCounter;

    //! Base bond class
    /*! Derived classes must fill the uninitialized data members.

        \warning Most methods assume that the cash flows are stored
                 sorted by date, the redemption(s) being after any
                 cash flow at the same date. In particular, if there's
                 one single redemption, it must be the last cash flow,

        \ingroup instruments

        \test
        - price/yield calculations are cross-checked for consistency.
        - price/yield calculations are checked against known good
          values.
    */
    class Bond : public Instrument {
      public:
        //! Bond price information
        class Price {
          public:
            enum Type { Dirty, Clean };
            Price() : amount_(Null<Real>()), type_(Bond::Price::Clean) {}
            Price(Real amount, Type type) : amount_(amount), type_(type) {}
            Real amount() const {
                QL_REQUIRE(amount_ != Null<Real>(), "no amount given");
                return amount_;
            }
            Type type() const { return type_; }
            bool isValid() const { return amount_ != Null<Real>(); }
          private:
            Real amount_;
            Type type_;
        };

        //! constructor for amortizing or non-amortizing bonds.
        /*! Redemptions and maturity are calculated from the coupon
            data, if available.  Therefore, redemptions must not be
            included in the passed cash flows.
        */
        Bond(Natural settlementDays,
             Calendar calendar,
             const Date& issueDate = Date(),
             const Leg& coupons = Leg());

        //! old constructor for non amortizing bonds.
        /*! \warning The last passed cash flow must be the bond
                     redemption. No other cash flow can have a date
                     later than the redemption date.
        */
        Bond(Natural settlementDays,
             Calendar calendar,
             Real faceAmount,
             const Date& maturityDate,
             const Date& issueDate = Date(),
             const Leg& cashflows = Leg());

        class arguments;
        class results;
        class engine;

        //! \name Instrument interface
        //@{
        bool isExpired() const override;
        //@}
        //! \name Observable interface
        //@{
        void deepUpdate() override;
        //@}
        //! \name Inspectors
        //@{
        Natural settlementDays() const;
        const Calendar& calendar() const;

        const std::vector<Real>& notionals() const;
        virtual Real notional(Date d = Date()) const;

        /*! \note returns all the cash