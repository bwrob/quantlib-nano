/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003, 2004, 2008 StatPro Italia srl

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

#ifndef quantlib_test_utilities_hpp
#define quantlib_test_utilities_hpp

#include <ql/indexes/indexmanager.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <ql/instruments/barriertype.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <ql/quote.hpp>
#include <ql/patterns/observable.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <boost/test/unit_test.hpp>
#if BOOST_VERSION < 105900
#include <boost/test/floating_point_comparison.hpp>
#else
#include <boost/test/tools/floating_point_comparison.hpp>
#endif
#include <cmath>
#include <iomanip>
#include <numeric>
#include <string>
#include <utility>
#include <vector>

// This adapts the BOOST_CHECK_SMALL and BOOST_CHECK_CLOSE macros to
// support a struct as Real for arguments, while fully transparant to regular doubles.
// Unfortunately boost does not provide a portable way to customize these macros' behaviour,
// so we need to define wrapper macros QL_CHECK_SMALL etc.
//
// It is required to have a function `value` defined that returns the double-value
// of the Real type (or a value function in the Real type's namespace for ADT).

namespace QuantLib {
    // overload this function in case Real is something different - it should alway return double
    inline double value(double x) {
        return x;
    }
}

using QuantLib::value;

#define QL_CHECK_SMALL(FPV, T)  BOOST_CHECK_SMALL(value(FPV), value(T))
#define QL_CHECK_CLOSE(L, R, T) BOOST_CHECK_CLOSE(value(L), value(R), value(T))
#define QL_CHECK_CLOSE_FRACTION(L, R, T) BOOST_CHECK_CLOSE_FRACTION(value(L), value(R), value(T))

namespace QuantLib {

    std::string payoffTypeToString(const ext::shared_ptr<Payoff>&);
    std::string exerciseTypeToString(const ext::shared_ptr<Exercise>&);
    std::string barrierTypeToString(Barrier::Type type);


    ext::shared_ptr<YieldTermStructure>
    flatRate(const Date& today,
             const ext::shared_ptr<Quote>& forward,
             const DayCounter& dc);

    ext::shared_ptr<YieldTermStructure>
    flatRate(const Date& today,
             Rate forward,
             const DayCounter& dc);

    ext::shared_ptr<YieldTermStructure>
    flatRate(const ext::shared_ptr<Quote>& forward,
             const DayCounter& dc);

    ext::shared_ptr<YieldTermStructure>
    flatRate(Rate forward,
             const DayCounter& dc);


    ext::shared_ptr<BlackVolTermStructure>
    flatVol(const Date& today,
            const ext::shared_ptr<Quote>& volatility,
            const DayCounter& dc);

    ext::shared_ptr<BlackVolTermStructure>
    flatVol(const Date& today,
            Volatility volatility,
            const DayCounter& dc);

    ext::shared_ptr<BlackVolTermStructure>
    flatVol(const ext::shared_ptr<Quote>& volatility,
            const DayCounter& dc);

    ext::shared_ptr<BlackVolTermStructure>
    flatVol(Volatility volatility,
            const DayCounter& dc);


    Real relativeError(Real x1, Real x2, Real reference);

    //bool checkAbsError(Real x1, Real x2, Real tolerance){
    //    return std::fabs(x1 - x2) < tolerance;
    //};

    