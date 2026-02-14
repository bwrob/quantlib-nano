/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2020, 2025 Marcin Rybacki

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

/*! \file ultimateforwardtermstructure.hpp
    \brief Ultimate Forward Rate term structure
*/

#ifndef quantlib_ultimate_forward_term_structure_hpp
#define quantlib_ultimate_forward_term_structure_hpp

#include <ql/math/rounding.hpp>
#include <ql/optional.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yield/zeroyieldstructure.hpp>
#include <utility>

namespace QuantLib {

    //! Ultimate forward term structure

    /*! Dutch regulatory term structure for pension funds with a
        parametrized extrapolation mechanism designed for
        discounting long dated liabilities.

        Relevant documentation can be found on the Dutch Central
        Bank website:

        FTK term structure documentation (Financieel toetsingskader):
        https://www.dnb.nl/media/4lmprzrk/vaststelling_methode_rentetermijnstructuur_ftk.pdf

        UFR 2013-2019 term structure documentation:
        https://www.dnb.nl/media/0vmbxaf4/methodologie-dnb.pdf

        UFR 2023 term structure documentation (p.46):
        https://www.tweedekamer.nl/downloads/document?id=2022D50944

        Optionally, computed zero rates may be rounded.
        The specified number of decimal places will affect the rate
        in decimal format; for example, rounding a rate of 1.5555%
        to 5 decimal places results in 0.015555 becoming 0.01556, or 1.556%.

        This term structure will remain linked to the original
        structure, i.e., any changes in the latter will be
        reflected in this structure as well.

        \ingroup yieldtermstructures

        \test
        - the correctness of the returned zero rates is tested by
          checking them against reference values obtained
          from the official source.
        - extrapolated forward is validated.
        - rates on the cut-off point are checked against those
          implied by the base curve.
        - inspectors are tested against the base curve.
        - incorrect input for cut-off point should raise an exception.
        - observability against changes in the underlying term
          structure and the additional components is checked.
        - rounding of output rate with predefined compounding.
    */

    class UltimateForwardTermStructure : public ZeroYieldStructure {
      public:
        UltimateForwardTermStructure(Handle<YieldTermStructure>,
                                     Handle<Quote> lastLiquidForwardRate,
                                     Handle<Quote> ultimateForwardRate,
                                     const Period& firstSmoothingPoint,
                                     Real alpha,
                                     const ext::optional<Integer>& roundingDigits = ext::nullopt,
                                     Compounding compounding = Compounded,
                                     Frequency frequency = Annual);
        //! \name YieldTermStructure interface
        //@{
        DayCounter dayCounter() const override;
        Calendar calendar() const override;
        Natural settlementDays() const override;
        const Date& referenceDate() const override;
        Date maxDate() const override;
        //@}
        //! \name Observe