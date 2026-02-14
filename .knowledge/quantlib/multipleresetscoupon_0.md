/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Toyin Akin
 Copyright (C) 2021 Marcin Rybacki

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

/*! \file multipleresetscoupon.hpp
    \brief Coupon compounding or averaging multiple fixings
*/

#ifndef quantlib_multiple_resets_coupon_hpp
#define quantlib_multiple_resets_coupon_hpp

#include <ql/cashflows/couponpricer.hpp>
#include <ql/cashflows/floatingratecoupon.hpp>
#include <ql/cashflows/rateaveraging.hpp>
#include <ql/time/schedule.hpp>
#include <vector>

namespace QuantLib {

    class IborIndex;

    //! multiple-reset coupon
    /*! %Coupon paying a rate calculated by compounding or averaging
        multiple fixings during its accrual period.
    */
    class MultipleResetsCoupon : public FloatingRateCoupon {
      public:
        /*! \param resetSchedule the schedule for the multiple resets. The first and last
                                 dates are also the start and end dates of the coupon.
                                 Each period specified by the schedule is the underlying
                                 period for one fixing; the corresponding fixing date is
                                 the passed number of fixing days before the start of
                                 the period.
            \param couponSpread  an optional spread added to the final coupon rate.
            \param rateSpread    an optional spread added to each of the underlying fixings.
            \param gearing       an optional multiplier for the final coupon rate.
        */
        MultipleResetsCoupon(const Date& paymentDate,
                             Real nominal,
                             const Schedule& resetSchedule,
                             Natural fixingDays,
                             const ext::shared_ptr<IborIndex>& index,
                             Real gearing = 1.0,
                             Rate couponSpread = 0.0,
                             Rate rateSpread = 0.0,
                             const Date& refPeriodStart = Date(),
                             const Date& refPeriodEnd = Date(),
                             const DayCounter& dayCounter = DayCounter(),
                             const Date& exCouponDate = Date());

        //! \name Inspectors
        //@{
        //! fixing dates for the rates to be compounded
        const std::vector<Date>& fixingDates() const { return fixingDates_; }
        //! accrual (compounding) periods
        const std::vector<Time>& dt() const { return dt_; }
        //! value dates for the rates to be compounded
        const std::vector<Date>& valueDates() const { return valueDates_; }
        //! rate spread
        Spread rateSpread() const { return rateSpread_; }
        //@}
        //! \name FloatingRateCoupon interface
        //@{
        //! the date when the coupon is fully determined
        Date fixingDate() const override { return fixingDates_.back(); }
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      private:
        Date fixingDate(const Date& valueDate) const;

        std::vector<Date> valueDates_, fixingDates_;
        Size n_;
        std::vector<Time> dt_;
        Rate rateSpread_;
    };


    class MultipleResetsPricer: public Flo
