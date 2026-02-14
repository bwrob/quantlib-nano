/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2005, 2006 StatPro Italia srl
 Copyright (C) 2005 Charles Whitmore
 Copyright (C) 2007, 2008, 2009, 2010, 2011 Ferdinando Ametrano
 Copyright (C) 2008 Toyin Akin

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

/*! \file cashflows.hpp
    \brief Cash-flow analysis functions
*/

#ifndef quantlib_cashflows_hpp
#define quantlib_cashflows_hpp

#include <ql/cashflows/duration.hpp>
#include <ql/cashflow.hpp>
#include <ql/interestrate.hpp>
#include <ql/shared_ptr.hpp>

namespace QuantLib {

    class YieldTermStructure;

    //! %cashflow-analysis functions
    /*! \todo add tests */
    class CashFlows {
      private:
        class IrrFinder {
          public:
            IrrFinder(const Leg& leg,
                      Real npv,
                      DayCounter dayCounter,
                      Compounding comp,
                      Frequency freq,
                      const ext::optional<bool>& includeSettlementDateFlows,
                      Date settlementDate,
                      Date npvDate);

            Real operator()(Rate y) const;
            Real derivative(Rate y) const;
          private:
            void checkSign() const;

            const Leg& leg_;
            Real npv_;
            DayCounter dayCounter_;
            Compounding compounding_;
            Frequency frequency_;
            ext::optional<bool> includeSettlementDateFlows_;
            Date settlementDate_, npvDate_;
        };
      public:
        CashFlows() = delete;
        CashFlows(CashFlows&&) = delete;
        CashFlows(const CashFlows&) = delete;
        CashFlows& operator=(CashFlows&&) = delete;
        CashFlows& operator=(const CashFlows&) = delete;
        ~CashFlows() = default;

        //! \name Date functions
        //@{
        static Date startDate(const Leg& leg);
        static Date maturityDate(const Leg& leg);
        static bool isExpired(const Leg& leg,
                              const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                              Date settlementDate = Date());
        //@}

        //! \name CashFlow functions
        //@{
        //! the last cashflow paying before or at the given date
        static Leg::const_reverse_iterator
        previousCashFlow(const Leg& leg,
                         const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                         Date settlementDate = Date());
        //! the first cashflow paying after the given date
        static Leg::const_iterator
        nextCashFlow(const Leg& leg,
                     const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                     Date settlementDate = Date());
        static Date
        previousCashFlowDate(const Leg& leg,
                             const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                             Date settlementDate = Date());
        static Date
        nextCashFlowDate(const Leg& leg,
                         const ext::optional<bool>& includeSettlementDateFlows = ext::nullopt,
                         Date settlementDate = Date());
        static Real
        previousCashFlowAmount(const Leg& leg,
                               const ext::optional<bool>& include