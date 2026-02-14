/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2014 Jose Aparicio

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

#ifndef quantlib_base_correl_structure_hpp
#define quantlib_base_correl_structure_hpp

#include <ql/quote.hpp>
#include <ql/utilities/dataformatters.hpp>
#include <ql/math/interpolations/bilinearinterpolation.hpp>
#include <ql/math/interpolations/bicubicsplineinterpolation.hpp>

#include <ql/experimental/credit/correlationstructure.hpp>

namespace QuantLib {


    /*! Matrix based Base Correlation Term Structure\par
    Loss level versus time interpolated scalar copula type parametric
    correlation term structure. Represents the correlation for the credit loss
    level of a given portfolio at a given loss level and time.

    \todo The relation to a given basket is to be made explicit for bespoke
    models to be implemented.
    \todo Consider moving to a matrix data structure. A matrix might make some
    computations heavy, template specialization on the dimension might be an
    alternative to having two classes, one for scalars and another for matrices.
    \todo Rethink all the data structure with a basket where current losses are
    not zero.
    \todo In principle the 2D interpolator is left optional since there are
    arbitrage issues on the interpolator type to be used. However one has to be
    careful when using non local interpolators like CubicSplines which have an
    effect on the past (calibrated) coupons of previous tenors.
    */
    template<class Interpolator2D_T>
    class BaseCorrelationTermStructure : public CorrelationTermStructure {
    public:
        /*
        @param correls Corresponds to: correls[iYear][iLoss]

        The Settlement date should in an ideal world coincide with the
        (implicit) basket inception date and its default term structures
        settlement dates.
        */
        BaseCorrelationTermStructure(
            Natural settlementDays,
            const Calendar& cal,
            BusinessDayConvention bdc,
            const std::vector<Period>& tenors,// sorted
            const std::vector<Real>& lossLevel,//sorted
            const std::vector<std::vector<Handle<Quote> > >& correls,
            const DayCounter& dc = DayCounter()
            )
        : CorrelationTermStructure(settlementDays, cal, bdc, dc),
          correlHandles_(correls),
          correlations_(correls.size(), correls.front().size()),
          nTrancheTenors_(tenors.size()),
          nLosses_(lossLevel.size()),
          tenors_(tenors),
          lossLevel_(lossLevel),
          trancheTimes_(tenors.size(), 0.) {
              checkTrancheTenors();

              for (auto& tenor : tenors_)
                  trancheDates_.push_back(
                      calendar().advance(referenceDate(), tenor, businessDayConvention()));

              initializeTrancheTimes();
              checkInputs(correlations_.rows(), correlations_.columns());
                updateMatrix();
              registerWithMarketData();
              // call factory
              setupInterpolation();
        }
    private:
        virtual void setupInterpolation() ;
    public:
      Size correlationSize() const override { return 1; }
      //! Implicit correlation for the given loss interval.
      Real ImplicitCorrelatio
