/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Ferdinando Ametrano
 Copyright (C) 2007 François du Vignaud
 Copyright (C) 2007 Marco Bianchetti
 Copyright (C) 2007 Katiuscia Manzoni

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

/*! \file historicalforwardratesanalysis.hpp
    \brief Statistical analysis of historical forward rates
*/

#ifndef quantlib_historical_forward_rates_analysis_hpp
#define quantlib_historical_forward_rates_analysis_hpp

#include <ql/indexes/iborindex.hpp>
#include <ql/indexes/swapindex.hpp>
#include <ql/math/matrix.hpp>
#include <ql/math/statistics/sequencestatistics.hpp>
#include <ql/quotes/simplequote.hpp>
#include <ql/termstructures/yield/piecewiseyieldcurve.hpp>
#include <ql/termstructures/yield/ratehelpers.hpp>
#include <ql/time/calendar.hpp>
#include <ql/time/date.hpp>
#include <utility>

namespace QuantLib {

    template<class Traits, class Interpolator>
    void historicalForwardRatesAnalysis(
                SequenceStatistics& statistics,
                std::vector<Date>& skippedDates,
                std::vector<std::string>& skippedDatesErrorMessage,
                std::vector<Date>& failedDates,
                std::vector<std::string>& failedDatesErrorMessage,
                std::vector<Period>& fixingPeriods,
                const Date& startDate,
                const Date& endDate,
                const Period& step,
                const ext::shared_ptr<InterestRateIndex>& fwdIndex,
                const Period& initialGap,
                const Period& horizon,
                const std::vector<ext::shared_ptr<IborIndex> >& iborIndexes,
                const std::vector<ext::shared_ptr<SwapIndex> >& swapIndexes,
                const DayCounter& yieldCurveDayCounter,
                Real yieldCurveAccuracy = 1.0e-12,
                const Interpolator& i = Interpolator()) {


        statistics.reset();
        skippedDates.clear();
        skippedDatesErrorMessage.clear();
        failedDates.clear();
        failedDatesErrorMessage.clear();
        fixingPeriods.clear();

        SavedSettings backup;
        Settings::instance().enforcesTodaysHistoricFixings() = true;

        std::vector<ext::shared_ptr<RateHelper> > rateHelpers;

        // Create DepositRateHelper
        std::vector<ext::shared_ptr<SimpleQuote> > iborQuotes;
        std::vector<ext::shared_ptr<IborIndex> >::const_iterator ibor;
        for (ibor=iborIndexes.begin(); ibor!=iborIndexes.end(); ++ibor) {
            ext::shared_ptr<SimpleQuote> quote(new SimpleQuote);
            iborQuotes.push_back(quote);
            Handle<Quote> quoteHandle(quote);
            rateHelpers.push_back(ext::shared_ptr<RateHelper> (new
                DepositRateHelper(quoteHandle,
                                  (*ibor)->tenor(),
                                  (*ibor)->fixingDays(),
                                  (*ibor)->fixingCalendar(),
                                  (*ibor)->businessDayConvention(),
                                  (*ibor)->endOfMonth(),
                                  (*ibor)->dayCounter())));
        }

        // Create SwapRateHelper
        std::vector<ext::shared_ptr<SimpleQuote> > swapQuotes;
        std::vector<ext::shared_ptr<SwapIndex> >::const_iterator swap;
        for (swap=swapIndexes.begin(); 