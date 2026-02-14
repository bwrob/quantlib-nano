/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2005, 2006, 2007, 2008, 2009 StatPro Italia srl
 Copyright (C) 2009, 2015 Ferdinando Ametrano
 Copyright (C) 2015 Paolo Mazzocchi

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

/*! \file forwardcurve.hpp
    \brief interpolated forward-rate structure
*/

#ifndef quantlib_forward_curve_hpp
#define quantlib_forward_curve_hpp

#include <ql/termstructures/yield/forwardstructure.hpp>
#include <ql/termstructures/interpolatedcurve.hpp>
#include <ql/math/interpolations/backwardflatinterpolation.hpp>
#include <utility>

namespace QuantLib {

    //! YieldTermStructure based on interpolation of forward rates
    /*! \ingroup yieldtermstructures */
    template <class Interpolator>
    class InterpolatedForwardCurve : public ForwardRateStructure,
                                     protected InterpolatedCurve<Interpolator> {
      public:
        // constructor
        InterpolatedForwardCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& forwards,
            const DayCounter& dayCounter,
            const Calendar& cal = Calendar(),
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedForwardCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& forwards,
            const DayCounter& dayCounter,
            const Calendar& calendar,
            const Interpolator& interpolator);
        InterpolatedForwardCurve(
            const std::vector<Date>& dates,
            const std::vector<Rate>& forwards,
            const DayCounter& dayCounter,
            const Interpolator& interpolator);
        //! \name TermStructure interface
        //@{
        Date maxDate() const override;
        //@}
        //! \name other inspectors
        //@{
        const std::vector<Time>& times() const;
        const std::vector<Date>& dates() const;
        const std::vector<Real>& data() const;
        const std::vector<Rate>& forwards() const;
        std::vector<std::pair<Date, Real> > nodes() const;
        //@}

      protected:
        explicit InterpolatedForwardCurve(
            const DayCounter&,
            const Interpolator& interpolator = {});
        InterpolatedForwardCurve(
            const Date& referenceDate,
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});
        InterpolatedForwardCurve(
            Natural settlementDays,
            const Calendar&,
            const DayCounter&,
            const std::vector<Handle<Quote> >& jumps = {},
            const std::vector<Date>& jumpDates = {},
            const Interpolator& interpolator = {});

        //! \name ForwardRateStructure implementation
        //@{
        Rate forwardImpl(Time t) const override;
        Rate zeroYieldImpl(Time t) const override;
        //@}
        mutable std::vector<Date> dates_;
      private:
        void initialize();
    };

    //! Term structure based on flat interpolation of forward rates
    /*! \ingroup yieldtermstructures */

    typedef InterpolatedForwardCurve<Backward