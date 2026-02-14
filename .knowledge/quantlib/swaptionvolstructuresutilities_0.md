/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Cristina Duminuco
 Copyright (C) 2006 Ferdinando Ametrano
 Copyright (C) 2006 François du Vignaud
 Copyright (C) 2006 Giorgio Facchinetti

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

#ifndef quantlib_test_swaption_volatility_structures_utilities_hpp
#define quantlib_test_swaption_volatility_structures_utilities_hpp

#include <ql/time/period.hpp>
#include <ql/math/matrix.hpp>
#include <ql/quotes/simplequote.hpp>
#include <ql/time/calendars/target.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolmatrix.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <iostream>
#include <vector>

namespace QuantLib {

    struct SwaptionTenors {
        std::vector<Period> options;
        std::vector<Period> swaps;
    };
    struct SwaptionMarketConventions {
        Calendar calendar;
        BusinessDayConvention optionBdc;
        DayCounter dayCounter;
        void setConventions() {
            calendar = TARGET();
            optionBdc = ModifiedFollowing;
            dayCounter = Actual365Fixed();
        }
    };
    struct AtmVolatility {
        SwaptionTenors tenors;
        Matrix vols;
        std::vector<std::vector<Handle<Quote> > > volsHandle;
        void setMarketData() {
            tenors.options.resize(6);
            tenors.options[0] = Period(1, Months);
            tenors.options[1] = Period(6, Months);
            tenors.options[2] = Period(1, Years);
            tenors.options[3] = Period(5, Years);
            tenors.options[4] = Period(10, Years);
            tenors.options[5] = Period(30, Years);
            tenors.swaps.resize(4);
            tenors.swaps[0] = Period(1, Years);
            tenors.swaps[1] = Period(5, Years);
            tenors.swaps[2] = Period(10, Years);
            tenors.swaps[3] = Period(30, Years);
            vols = Matrix(tenors.options.size(), tenors.swaps.size());
            vols[0][0]=0.1300; vols[0][1]=0.1560; vols[0][2]=0.1390; vols[0][3]=0.1220;
            vols[1][0]=0.1440; vols[1][1]=0.1580; vols[1][2]=0.1460; vols[1][3]=0.1260;
            vols[2][0]=0.1600; vols[2][1]=0.1590; vols[2][2]=0.1470; vols[2][3]=0.1290;
            vols[3][0]=0.1640; vols[3][1]=0.1470; vols[3][2]=0.1370; vols[3][3]=0.1220;
            vols[4][0]=0.1400; vols[4][1]=0.1300; vols[4][2]=0.1250; vols[4][3]=0.1100;
            vols[5][0]=0.1130; vols[5][1]=0.1090; vols[5][2]=0.1070; vols[5][3]=0.0930;
            volsHandle.resize(tenors.options.size());
            for (Size i=0; i<tenors.options.size(); i++){
                volsHandle[i].resize(tenors.swaps.size());
                for (Size j=0; j<tenors.swaps.size(); j++)
                    // every handle must be reassigned, as the ones created by
                    // default are all linked together.
                    volsHandle[i][j] = Handle<Quote>(ext::shared_ptr<Quote>(new
                        SimpleQuote(vols[i][j])));
            }
        };
    };
    struct VolatilityCube {
        SwaptionTenors tenors;
        Matrix volSpreads;
        std::vector<std::vector<Handle<Quote> > > volSpreadsHandle;
        std::vector<Spread> strikeSpreads;
        void setMarketData() {
            tenors.options.resize(3);
            ten
