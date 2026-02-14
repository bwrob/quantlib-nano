/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007, 2011 Ferdinando Ametrano
 Copyright (C) 2007 Giorgio Facchinetti
 Copyright (C) 2007 Cristina Duminuco
 Copyright (C) 2007 StatPro Italia srl
 Copyright (C) 2017 Joseph Jeisman
 Copyright (C) 2017 Fabrice Lecuyer

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

/*! \file iborcoupon.hpp
    \brief Coupon paying a Libor-type index
*/

#ifndef quantlib_ibor_coupon_hpp
#define quantlib_ibor_coupon_hpp

#include <ql/cashflows/floatingratecoupon.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/patterns/singleton.hpp>
#include <ql/time/schedule.hpp>
#include <ql/optional.hpp>

namespace QuantLib {

    //! %Coupon paying a Libor-type index
    class IborCoupon : public FloatingRateCoupon {
      public:
        IborCoupon(const Date& paymentDate,
                   Real nominal,
                   const Date& startDate,
                   const Date& endDate,
                   Natural fixingDays,
                   const ext::shared_ptr<IborIndex>& index,
                   Real gearing = 1.0,
                   Spread spread = 0.0,
                   const Date& refPeriodStart = Date(),
                   const Date& refPeriodEnd = Date(),
                   const DayCounter& dayCounter = DayCounter(),
                   bool isInArrears = false,
                   const Date& exCouponDate = Date());
        //! \name Inspectors
        //@{
        const ext::shared_ptr<IborIndex>& iborIndex() const { return iborIndex_; }
        bool hasFixed() const;
        //@}
        //! \name FloatingRateCoupon interface
        //@{
        Date fixingDate() const override;
        // implemented in order to manage the case of par coupon
        Rate indexFixing() const override;
        void setPricer(const ext::shared_ptr<FloatingRateCouponPricer>&) override;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
        /*! \name Internal calculations

            You won't probably need these methods unless you're implementing
            a coupon pricer.
        */
        //@{
        //! Start of the deposit period underlying the index fixing
        const Date& fixingValueDate() const;
        //! End of the deposit period underlying the index fixing
        const Date& fixingMaturityDate() const;
        //! End of the deposit period underlying the coupon fixing
        /*! This might be not the same as fixingMaturityDate if par coupons are used. */
        const Date& fixingEndDate() const;
        //! Period underlying the index fixing, as a year fraction
        Time spanningTimeIndexMaturity() const;
        //! Period underlying the coupon fixing, as a year fraction
        /*! This might be not the same as spanningTimeIndexMaturity if par coupons are used. */
        Time spanningTime() const;
        //@}

      private:
        friend class IborCouponPricer;
        ext::shared_ptr<IborIndex> iborIndex_;
        Date fixingDate_;
        // computed by coupon pricer (depending on par coupon flag) and stored here
        void initializeCachedData() const;
        mutable bool cachedDataIsInitialized_ = false;
        mutable Date fixingValueDate_, fixingEndDate_, fixingMaturityDate_;
        mutable Time spanningTime_, spanningTi