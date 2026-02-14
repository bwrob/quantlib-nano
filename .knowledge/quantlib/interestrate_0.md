/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2004 Ferdinando Ametrano

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

/*! \file interestrate.hpp
    \brief Instrument rate class
*/

#ifndef quantlib_interest_rate_hpp
#define quantlib_interest_rate_hpp

#include <ql/compounding.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>

namespace QuantLib {

    //! Concrete interest rate class
    /*! This class encapsulate the interest rate compounding algebra.
        It manages day-counting conventions, compounding conventions,
        conversion between different conventions, discount/compound factor
        calculations, and implied/equivalent rate calculations.

        \test Converted rates are checked against known good results
    */
    class InterestRate {
      public:
        //! \name constructors
        //@{
        //! Default constructor returning a null interest rate.
        InterestRate();
        //! Standard constructor
        InterestRate(Rate r, DayCounter dc, Compounding comp, Frequency freq);
        //@}
        //! \name conversions
        //@{
        operator Rate() const { return r_; }
        //@}
        //! \name inspectors
        //@{
        Rate rate() const { return r_; }
        const DayCounter& dayCounter() const { return dc_; }
        Compounding compounding() const { return comp_; }
        Frequency frequency() const {
            return freqMakesSense_ ? Frequency(Integer(freq_)) : NoFrequency;
        }
        //@}

        //! \name discount/compound factor calculations
        //@{
        //! discount factor implied by the rate compounded at time t.
        /*! \warning Time must be measured using InterestRate's own
                     day counter.
        */
        DiscountFactor discountFactor(Time t) const {
            return 1.0/compoundFactor(t);
        }

        //! discount factor implied by the rate compounded between two dates
        DiscountFactor discountFactor(const Date& d1,
                                      const Date& d2,
                                      const Date& refStart = Date(),
                                      const Date& refEnd = Date()) const {
            QL_REQUIRE(d2>=d1,
                       "d1 (" << d1 << ") "
                       "later than d2 (" << d2 << ")");
            Time t = dc_.yearFraction(d1, d2, refStart, refEnd);
            return discountFactor(t);
        }

        //! compound factor implied by the rate compounded at time t.
        /*! returns the compound (a.k.a capitalization) factor
            implied by the rate compounded at time t.

            \warning Time must be measured using InterestRate's own
                     day counter.
        */
        Real compoundFactor(Time t) const;

        //! compound factor implied by the rate compounded between two dates
        /*! returns the compound (a.k.a capitalization) factor
            implied by the rate compounded between two dates.
        */
        Real compoundFactor(const Date& d1,
                            const Date& d2,
                            const Date& refStart = Date(),
                            const Date& refEnd = Date()) const {
            QL_REQUIRE(d2>=d1,
                       "d1 (" << d1 << ") "
                       "later than d2 ("
