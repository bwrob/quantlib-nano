/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2013, 2016 Peter Caspers

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

/*! \file nonstandardswap.hpp
    \brief vanilla swap but possibly with period dependent nominal and strike
*/

#ifndef quantlib_nonstandard_swap_hpp
#define quantlib_nonstandard_swap_hpp

#include <ql/instruments/swap.hpp>
#include <ql/instruments/fixedvsfloatingswap.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>
#include <ql/optional.hpp>

namespace QuantLib {

    class IborIndex;
    class SwapIndex;

    //! nonstandard swap

    class NonstandardSwap : public Swap {
      public:
        class arguments;
        class results;
        class engine;
        explicit NonstandardSwap(const FixedVsFloatingSwap &fromVanilla);
        NonstandardSwap(Swap::Type type,
                        std::vector<Real> fixedNominal,
                        const std::vector<Real>& floatingNominal,
                        Schedule fixedSchedule,
                        std::vector<Real> fixedRate,
                        DayCounter fixedDayCount,
                        Schedule floatingSchedule,
                        ext::shared_ptr<IborIndex> iborIndex,
                        Real gearing,
                        Spread spread,
                        DayCounter floatingDayCount,
                        bool intermediateCapitalExchange = false,
                        bool finalCapitalExchange = false,
                        ext::optional<BusinessDayConvention> paymentConvention = ext::nullopt);
        NonstandardSwap(Swap::Type type,
                        std::vector<Real> fixedNominal,
                        std::vector<Real> floatingNominal,
                        Schedule fixedSchedule,
                        std::vector<Real> fixedRate,
                        DayCounter fixedDayCount,
                        Schedule floatingSchedule,
                        ext::shared_ptr<IborIndex> iborIndex,
                        std::vector<Real> gearing,
                        std::vector<Spread> spread,
                        DayCounter floatingDayCount,
                        bool intermediateCapitalExchange = false,
                        bool finalCapitalExchange = false,
                        ext::optional<BusinessDayConvention> paymentConvention = ext::nullopt);
        //! \name Inspectors
        //@{
        Swap::Type type() const;
        const std::vector<Real> &fixedNominal() const;
        const std::vector<Real> &floatingNominal() const;

        const Schedule &fixedSchedule() const;
        const std::vector<Real> &fixedRate() const;
        const DayCounter &fixedDayCount() const;

        const Schedule &floatingSchedule() const;
        const ext::shared_ptr<IborIndex> &iborIndex() const;
        Spread spread() const;
        Real gearing() const;
        const std::vector<Spread>& spreads() const;
        const std::vector<Real>& gearings() const;
        const DayCounter &floatingDayCount() const;

        BusinessDayConvention paymentConvention() const;

        const Leg &fixedLeg() const;
        const Leg &floatingLeg() const;
        //@}

        //! \name Results
        //@{
        //@}
        // other
        void setupArguments(PricingEngine::arguments* args) const overr
