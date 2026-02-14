/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 Dirk Eddelbuettel
 Copyright (C) 2006, 2009, 2010 Klaus Spanderen
 Copyright (C) 2010 Kakhkhor Abdijalilov
 Copyright (C) 2010 Slava Mazur

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

/*! \file generallinearleastsquares.hpp
    \brief general linear least square regression
*/

#ifndef quantlib_general_linear_least_squares_hpp
#define quantlib_general_linear_least_squares_hpp

#include <ql/qldefines.hpp>
#include <ql/math/matrixutilities/svd.hpp>
#include <ql/math/array.hpp>
#include <vector>

namespace QuantLib {

    //! general linear least squares regression
    /*! References:
    "Numerical Recipes in C", 2nd edition,
    Press, Teukolsky, Vetterling, Flannery,

    \test the correctness of the returned values is tested by
    checking their properties.
    */
    class GeneralLinearLeastSquares {
    public:
        template <class xContainer, class yContainer, class vContainer>
        GeneralLinearLeastSquares(const xContainer & x,
                                  const yContainer & y, const vContainer & v);

        template<class xIterator, class yIterator, class vIterator>
        GeneralLinearLeastSquares(xIterator xBegin, xIterator xEnd,
                                  yIterator yBegin, yIterator yEnd,
                                  vIterator vBegin, vIterator vEnd);

        const Array& coefficients()   const { return a_; }
        const Array& residuals()      const { return residuals_; }

        //! standard parameter errors as given by Excel, R etc.
        const Array& standardErrors() const { return standardErrors_; }
        //! modeling uncertainty as definied in Numerical Recipes
        const Array& error()          const { return err_;}

        Size size() const { return residuals_.size(); }

        Size dim() const { return a_.size(); }

    protected:
        Array a_, err_, residuals_, standardErrors_;

        template <class xIterator, class yIterator, class vIterator>
        void calculate(
            xIterator xBegin, xIterator xEnd,
            yIterator yBegin, yIterator yEnd,
            vIterator vBegin);
    };

    template <class xContainer, class yContainer, class vContainer> inline
    GeneralLinearLeastSquares::GeneralLinearLeastSquares(const xContainer & x,
                                                         const yContainer & y,
                                                         const vContainer & v)
    : a_(v.size(), 0.0),
      err_(v.size(), 0.0),
      residuals_(y.size()),
      standardErrors_(v.size()) {
        calculate(x.begin(), x.end(), y.begin(), y.end(), v.begin());
    }

    template<class xIterator, class yIterator, class vIterator> inline
    GeneralLinearLeastSquares::GeneralLinearLeastSquares(
                                            xIterator xBegin, xIterator xEnd,
                                            yIterator yBegin, yIterator yEnd,
                                            vIterator vBegin, vIterator vEnd)
    : a_(std::distance(vBegin, vEnd), 0.0),
      err_(a_.size(), 0.0),
      residuals_(std::distance(yBegin, yEnd)),
      standardErrors_(a_.size()) {
        calculate(xBegin, xEnd, yBegin, yEnd, vBegin);
    }


    template <class xIterator, class yIterator, class vIterator>
    void G