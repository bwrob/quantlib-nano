/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Roland Lichters
 Copyright (C) 2006, 2008, 2014 StatPro Italia srl
 Copyright (C) 2010 Robert Philipp

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

/*! \file piecewiseforwardspreadedtermstructure.hpp
    \brief Piecewise-forward-spreaded term structure
*/

#ifndef quantlib_piecewise_forward_spreaded_term_structure_hpp
#define quantlib_piecewise_forward_spreaded_term_structure_hpp

#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yield/forwardstructure.hpp>
#include <utility>
#include <vector>

namespace QuantLib {

  //! Term structure with an added vector of spreads on the instantaneous forward rate
  /*! The forward rate spread at any given date is interpolated
      between the input data.

      \note This term structure will remain linked to the original
            structure, i.e., any changes in the latter will be
            reflected in this structure as well.

      \ingroup yieldtermstructures
  */

  template <class Interpolator>
  class InterpolatedPiecewiseForwardSpreadedTermStructure : public ForwardRateStructure {
    public:
      InterpolatedPiecewiseForwardSpreadedTermStructure(Handle<YieldTermStructure>,
                                                     std::vector<Handle<Quote>> spreads,
                                                     std::vector<Date> dates,
                                                     Interpolator factory = Interpolator());

      /*! \deprecated Use the constructor without a day counter.
                      Deprecated in version 1.41.
      */
      [[deprecated("Use the constructor without DayCounter")]]
      InterpolatedPiecewiseForwardSpreadedTermStructure(Handle<YieldTermStructure>,
                                                     std::vector<Handle<Quote>> spreads,
                                                     std::vector<Date> dates,
                                                     const DayCounter& dc,
                                                     Interpolator factory = Interpolator());
      //! \name YieldTermStructure interface
      //@{
      DayCounter dayCounter() const override;
      Natural settlementDays() const override;
      Calendar calendar() const override;
      const Date& referenceDate() const override;
      Date maxDate() const override;
      //@}
    protected:
      //! returns the spreaded zero yield rate
      Rate zeroYieldImpl(Time) const override;
      Rate forwardImpl(Time) const override;
      void update() override;

    private:
      void updateInterpolation();
      Real calcSpread(Time t) const;
      Real calcSpreadPrimitive(Time t) const;
      Handle<YieldTermStructure> originalCurve_;
      std::vector<Handle<Quote> > spreads_;
      std::vector<Date> dates_;
      std::vector<Time> times_;
      std::vector<Spread> spreadValues_;
      Compounding comp_;
      Frequency freq_;
      Interpolator factory_;
      Interpolation interpolator_;
  };

    // inline definitions

    #ifndef __DOXYGEN__

    template <class T>
    inline InterpolatedPiecewiseForwardSpreadedTermStructure<
        T>::InterpolatedPiecewiseForwardSpreadedTermStructure(Handle<YieldTermStructure> h,
                                    