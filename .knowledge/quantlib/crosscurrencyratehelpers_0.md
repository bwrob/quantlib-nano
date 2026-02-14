/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2021 Marcin Rybacki
 Copyright (C) 2025 Uzair Beg

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

/*! \file crosscurrencyratehelpers.hpp
    \brief FX and cross currency basis swaps rate helpers
*/

#ifndef quantlib_crosscurrencyratehelpers_hpp
#define quantlib_crosscurrencyratehelpers_hpp

#include <ql/termstructures/yield/ratehelpers.hpp>

namespace QuantLib {

    class CrossCurrencySwapRateHelperBase : public RelativeDateRateHelper {
      public:
        void setTermStructure(YieldTermStructure* t) override;

      protected:
        CrossCurrencySwapRateHelperBase(const Handle<Quote>& quote,
                                        const Period& tenor,
                                        Natural fixingDays,
                                        Calendar calendar,
                                        BusinessDayConvention convention,
                                        bool endOfMonth,
                                        Handle<YieldTermStructure> collateralCurve,
                                        Integer paymentLag);

        void initializeDatesFromLegs(const Leg& firstLeg, const Leg& secondLeg);

        Period tenor_;
        Natural fixingDays_;
        Calendar calendar_;
        BusinessDayConvention convention_;
        bool endOfMonth_;
        Integer paymentLag_;

        Handle<YieldTermStructure> collateralHandle_;

        RelinkableHandle<YieldTermStructure> termStructureHandle_;

        Date initialNotionalExchangeDate_;
        Date finalNotionalExchangeDate_;
    };


    //! Base class for cross-currency basis swap rate helpers
    class CrossCurrencyBasisSwapRateHelperBase : public CrossCurrencySwapRateHelperBase {
      protected:
        CrossCurrencyBasisSwapRateHelperBase(const Handle<Quote>& basis,
                                             const Period& tenor,
                                             Natural fixingDays,
                                             Calendar calendar,
                                             BusinessDayConvention convention,
                                             bool endOfMonth,
                                             ext::shared_ptr<IborIndex> baseCurrencyIndex,
                                             ext::shared_ptr<IborIndex> quoteCurrencyIndex,
                                             Handle<YieldTermStructure> collateralCurve,
                                             bool isFxBaseCurrencyCollateralCurrency,
                                             bool isBasisOnFxBaseCurrencyLeg,
                                             Frequency paymentFrequency = NoFrequency,
                                             Integer paymentLag = 0);

        void initializeDates() override;
        const Handle<YieldTermStructure>& baseCcyLegDiscountHandle() const;
        const Handle<YieldTermStructure>& quoteCcyLegDiscountHandle() const;

        ext::shared_ptr<IborIndex> baseCcyIdx_;
        ext::shared_ptr<IborIndex> quoteCcyIdx_;
        bool isFxBaseCurrencyCollateralCurrency_;
        bool isBasisOnFxBaseCurrencyLeg_;
        Frequency paymentFrequency_;

        Leg baseCcyIborLeg_;
        Leg quoteCcyIborLeg_;
    };


    //! Rate helper for bootstrapping over constant-notional 