/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Cristina Duminuco
 Copyright (C) 2007 Ferdinando Ametrano

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

/*! \file abcdatmvolcurve.hpp
    \brief Abcd-interpolated at-the-money (no-smile) interest rate vol curve
*/

#ifndef quantlib_abcd_atm_vol_curve_hpp
#define quantlib_abcd_atm_vol_curve_hpp

#include <ql/experimental/volatility/blackatmvolcurve.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/math/interpolations/abcdinterpolation.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>

namespace QuantLib {

    class Quote;

    //! Abcd-interpolated at-the-money (no-smile) volatility curve
    /*! blah blah
    */
    class AbcdAtmVolCurve : public BlackAtmVolCurve,
                            public LazyObject {
      public:
        //! floating reference date, floating market data
        AbcdAtmVolCurve(Natural settlementDays,
                        const Calendar& cal,
                        const std::vector<Period>& optionTenors,
                        const std::vector<Handle<Quote> >& volsHandles,
                        std::vector<bool> inclusionInInterpolationFlag = std::vector<bool>(1, true),
                        BusinessDayConvention bdc = Following,
                        const DayCounter& dc = Actual365Fixed());
        //! Returns k adjustment factors for option tenors used in interpolation
        std::vector<Real> k() const;
        //! Returns k adjustment factor at time t
        Real k(Time t) const;
        Real a() const;
        Real b() const;
        Real c() const;
        Real d() const;
        Real rmsError() const;
        Real maxError() const;
        EndCriteria::Type endCriteria() const;
        //! \name TermStructure interface
        //@{
        Date maxDate() const override;
        //@}
        //! \name VolatilityTermStructure interface
        //@{
        Real minStrike() const override;
        Real maxStrike() const override;
        //@}
        //! \name LazyObject interface
        //@{
        void update() override;
        void performCalculations() const override;
        //@}
        //! \name some inspectors
        //@{
        const std::vector<Period>& optionTenors() const;
        const std::vector<Period>& optionTenorsInInterpolation() const;
        const std::vector<Date>& optionDates() const;
        const std::vector<Time>& optionTimes() const;
        //@}
        //! \name Visitability
        //@{
        void accept(AcyclicVisitor&) override;
        //@}
      protected:
        //! \name BlackAtmVolCurve interface
        //@{
        //! spot at-the-money variance calculation (k adjusted)
        Real atmVarianceImpl(Time t) const override;
        //! spot at-the-money volatility calculation (k adjusted)
        Volatility atmVolImpl(Time t) const override;
        //@}
      private:
        void checkInputs() const;
        void initializeOptionDatesAndTimes() const;
        void initializeVolatilities();
        void registerWithMarketData();
        void interpolate();

        Size nOptionTenors_;
        std::vector<Period> optionTenors_;
        mutable std::vector<Period> actualOptionTenors_;
        mutable std::vector<Date> optionDates_;
        mutable std::vector<Time> optionTimes_;
        mutab
