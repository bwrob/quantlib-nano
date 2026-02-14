/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007, 2008, 2009, 2010 Ferdinando Ametrano
 Copyright (C) 2007 Chiara Fornarola
 Copyright (C) 2009 StatPro Italia srl
 Copyright (C) 2009 Nathan Abbott

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

/*! \file bondfunctions.hpp
    \brief bond functions
*/

#ifndef quantlib_bond_functions_hpp
#define quantlib_bond_functions_hpp

#include <ql/cashflows/cashflows.hpp>
#include <ql/cashflows/duration.hpp>
#include <ql/cashflow.hpp>
#include <ql/interestrate.hpp>
#include <ql/instruments/bond.hpp>
#include <ql/shared_ptr.hpp>

namespace QuantLib {

    // forward declarations
    class Bond;
    class DayCounter;
    class YieldTermStructure;

    //! Bond adapters of CashFlows functions
    /*! See CashFlows for functions' documentation.

        These adapters calls into CashFlows functions passing as input the
        Bond cashflows, the dirty price (i.e. npv) calculated from clean
        price, the bond settlement date (unless another date is given), zero
        ex-dividend days, and excluding any cashflow on the settlement date.

        Prices are always clean, as per market convention.
    */
    struct BondFunctions {
        //! \name Date inspectors
        //@{
        static Date startDate(const Bond& bond);
        static Date maturityDate(const Bond& bond);
        static bool isTradable(const Bond& bond,
                               Date settlementDate = Date());
        //@}

        //! \name CashFlow inspectors
        //@{
        static Leg::const_reverse_iterator
        previousCashFlow(const Bond& bond,
                         Date refDate = Date());
        static Leg::const_iterator nextCashFlow(const Bond& bond,
                                                Date refDate = Date());
        static Date previousCashFlowDate(const Bond& bond,
                                         Date refDate = Date());
        static Date nextCashFlowDate(const Bond& bond,
                                     Date refDate = Date());
        static Real previousCashFlowAmount(const Bond& bond,
                                           Date refDate = Date());
        static Real nextCashFlowAmount(const Bond& bond,
                                       Date refDate = Date());
        //@}

        //! \name Coupon inspectors
        //@{
        static Rate previousCouponRate(const Bond& bond,
                                       Date settlementDate = Date());
        static Rate nextCouponRate(const Bond& bond,
                                   Date settlementDate = Date());
        static Date accrualStartDate(const Bond& bond,
                                     Date settlementDate = Date());
        static Date accrualEndDate(const Bond& bond,
                                   Date settlementDate = Date());
        static Date referencePeriodStart(const Bond& bond,
                                         Date settlementDate = Date());
        static Date referencePeriodEnd(const Bond& bond,
                                       Date settlementDate = Date());
        static Time accrualPeriod(const Bond& bond,
                                  Date settlementDate = Date());
        static Date::serial_type accrualDays(const Bond& bond,

