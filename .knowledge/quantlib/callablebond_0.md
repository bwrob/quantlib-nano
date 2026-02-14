/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Allen Kuo
 Copyright (C) 2017 BN Algorithms Ltd

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

/*! \file callablebond.hpp
    \brief callable bond classes
*/

#ifndef quantlib_callable_bond_hpp
#define quantlib_callable_bond_hpp

#include <ql/instruments/bond.hpp>
#include <ql/pricingengine.hpp>
#include <ql/instruments/callabilityschedule.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/handle.hpp>
#include <ql/quotes/simplequote.hpp>

namespace QuantLib {

    class Schedule;
    class DayCounter;

    //! Callable bond base class
    /*! Base callable bond class for fixed and zero coupon bonds.
        Defines commonalities between fixed and zero coupon callable
        bonds. At present, only European and Bermudan put/call schedules
        supported (no American optionality), as defined by the Callability
        class.

        \todo models/shortrate/calibrationHelpers
        \todo OAS/OAD
        \todo floating rate callable bonds ?

        \ingroup instruments
    */
    class CallableBond : public Bond {
      public:
        class arguments;
        class results;
        class engine;

        //! \name Inspectors
        //@{
        //! return the bond's put/call schedule
        const CallabilitySchedule& callability() const {
            return putCallSchedule_;
        }
        //@}

        //! \name Calculations
        //@{
        //! returns the Black implied forward yield volatility
        /*! the forward yield volatility, see Hull, Fourth Edition,
            Chapter 20, pg 536). Relevant only to European put/call
            schedules
        */
        Volatility impliedVolatility(
                              const Bond::Price& targetPrice,
                              const Handle<YieldTermStructure>& discountCurve,
                              Real accuracy,
                              Size maxEvaluations,
                              Volatility minVol,
                              Volatility maxVol) const;

        //! Calculate the Option Adjusted Spread (OAS)
        /*! Calculates the spread that needs to be added to the
            reference curve so that the theoretical model value
            matches the marketPrice.

         */
        Spread OAS(Real cleanPrice,
                   const Handle<YieldTermStructure>& engineTS,
                   const DayCounter& dayCounter,
                   Compounding compounding,
                   Frequency frequency,
                   Date settlementDate = Date(),
                   Real accuracy = 1.0e-10,
                   Size maxIterations = 100,
                   Rate guess = 0.0);

        //! Calculate the clean price based on the given
        //! option-adjust-spread (oas) over the given yield term
        //! structure (engineTS)
        Real cleanPriceOAS(Real oas,
                           const Handle<YieldTermStructure>& engineTS,
                           const DayCounter& dayCounter,
                           Compounding compounding,
                           Frequency frequency,
                           Date settlementDate = Date());

        //! Calculate the effective duration, i.e., the first
        //! differential of the dirty price w.r.t. a parallel shift of
