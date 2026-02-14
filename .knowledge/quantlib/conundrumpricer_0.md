/*
 Copyright (C) 2006 Giorgio Facchinetti
 Copyright (C) 2006 Mario Pucci
 Copyright (C) 2023 Andre Miemiec


 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it
 under the terms of the QuantLib license.  You should have received a
 copy of the license along with this program; if not, please email
 <quantlib-dev@lists.sf.net>. The license is also available online at
 <https://www.quantlib.org/license.shtml>.


 This program is distributed in the hope that it will be useful, but
 WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 or FITNESS FOR A PARTICULAR PURPOSE. See the license for more details. */

/*! \file conundrumpricer.hpp
    \brief CMS-coupon pricer
*/

#ifndef quantlib_conundrum_pricer_hpp
#define quantlib_conundrum_pricer_hpp

#include <ql/cashflows/couponpricer.hpp>
#include <ql/instruments/payoffs.hpp>

namespace QuantLib {

    class CmsCoupon;
    class YieldTermStructure;
    class Quote;

    class VanillaOptionPricer {
      public:
        virtual ~VanillaOptionPricer() = default;
        virtual Real operator()(Real strike,
                                Option::Type optionType,
                                Real deflator) const = 0;
    };

    class MarketQuotedOptionPricer : public VanillaOptionPricer {
      public:
        MarketQuotedOptionPricer(
                Rate forwardValue,
                Date expiryDate,
                const Period& swapTenor,
                const ext::shared_ptr<SwaptionVolatilityStructure>&
                                                         volatilityStructure);

        Real operator()(Real strike, Option::Type optionType, Real deflator) const override;

      private:
        Rate forwardValue_;
        Date expiryDate_;
        Period swapTenor_;
        ext::shared_ptr<SwaptionVolatilityStructure> volatilityStructure_;
        ext::shared_ptr<SmileSection> smile_;
    };

    class GFunction {
      public:
        virtual ~GFunction() = default;
        virtual Real operator()(Real x) = 0;
        virtual Real firstDerivative(Real x) = 0;
        virtual Real secondDerivative(Real x) = 0;
    };

    class GFunctionFactory {
      public:
        enum YieldCurveModel { Standard,
                               ExactYield,
                               ParallelShifts,
                               NonParallelShifts
        };

        GFunctionFactory() = delete;

        static ext::shared_ptr<GFunction>
        newGFunctionStandard(Size q,
                             Real delta,
                             Size swapLength);
        static ext::shared_ptr<GFunction>
        newGFunctionExactYield(const CmsCoupon& coupon);
        static ext::shared_ptr<GFunction>
        newGFunctionWithShifts(const CmsCoupon& coupon,
                               const Handle<Quote>& meanReversion);
      private:
        class GFunctionStandard : public GFunction {
          public:
            GFunctionStandard(Size q,
                              Real delta,
                              Size swapLength)
            : q_(q), delta_(delta), swapLength_(swapLength) {}
            Real operator()(Real x) override;
            Real firstDerivative(Real x) override;
            Real secondDerivative(Real x) override;

          protected:
            /* number of period per year */
            const int q_;
            /* fraction of a period between the swap start date and
               the pay date  */
            Real delta_;
            /* length of swap*/
            Size swapLength_;
        };

        class GFunctionExactYield : public GFunction {
          public:
            GFunctionExactYield(const CmsCoupon& coupon);
            Real operator()(Real x) override;
            Real firstDerivative(Real x) override;
            Real secondDerivative(Real x) override;


