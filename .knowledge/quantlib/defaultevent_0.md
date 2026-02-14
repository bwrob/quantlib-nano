/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 StatPro Italia srl
 Copyright (C) 2009 Jose Aparicio

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

/*! \file defaultevent.hpp
    \brief Classes for default-event description.
*/

#ifndef quantlib_default_event_hpp
#define quantlib_default_event_hpp

#include <ql/event.hpp>
#include <ql/currency.hpp>
#include <ql/math/comparison.hpp>
#include <ql/experimental/credit/defaulttype.hpp>
#include <ql/experimental/credit/defaultprobabilitykey.hpp>
#include <map>

namespace QuantLib {

    /**
    @class DefaultEvent
    @brief Credit event on a bond of a certain seniority(ies)/currency

      Represents a credit event affecting all bonds with a given \
      seniority and currency. It assumes that all such bonds suffer \
      the event simultaneously.
      Some events affect all seniorities and this has to be encoded
      through a different set of events of the same event type.
      The event is an actual realization, not a contractual reference,
      as such it contains only an atomic type.
    */
    class DefaultEvent : public Event {
      public:
        class DefaultSettlement : public Event {
          public:
            friend class DefaultEvent;
          protected:
            /*! Default settlement events encode the settlement date
                and the recovery rates for the affected
                seniorities. Specific events might require different
                sets of recoveries to be present. The way these
                objects are constructed is a prerogative of the
                particular event class.
            */
            DefaultSettlement(const Date& date,
                              const std::map<Seniority, Real>& recoveryRates);
            /*! When NoSeniority is passed all seniorities are assumed
                to have settled to the recovery passed.
            */
            DefaultSettlement(const Date& date = Date(),
                              Seniority seniority = NoSeniority,
                              Real recoveryRate = 0.4);
          public:
            Date date() const override;
            /*! Returns the recovery rate of a default event which has already
                settled.
            */
            Real recoveryRate(Seniority sen) const;
            void accept(AcyclicVisitor&) override;

          private:
            Date settlementDate_;
            //! Realized recovery rates
            std::map<Seniority, Real> recoveryRates_;
        };
      private:
        // for some reason, gcc chokes on the default parameter below
        // unless we use the typedef
        typedef std::map<Seniority, Real> rate_map;
      public:
        /*! Credit event with optional settlement
            information. Represents a credit event that has taken
            place. Realized events are of an atomic type.  If the
            settlement information is given seniorities present are
            the seniorities/bonds affected by the event.
        */
        DefaultEvent(const Date& creditEventDate,
                     const DefaultType& atomicEvType,
                     Currency curr,
                     Seniority bondsSen,
                     // Settlement information:
                     const Date& settleDate = Date(),

