/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2002, 2003, 2006 Ferdinando Ametrano
 Copyright (C) 2004, 2005, 2006, 2007 StatPro Italia srl

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

/*! \file interpolation2d.hpp
    \brief abstract base classes for 2-D interpolations
*/

#ifndef quantlib_interpolation2D_hpp
#define quantlib_interpolation2D_hpp

#include <ql/math/interpolations/extrapolation.hpp>
#include <ql/math/comparison.hpp>
#include <ql/math/matrix.hpp>
#include <ql/errors.hpp>
#include <ql/types.hpp>
#include <vector>

namespace QuantLib {

    //! base class for 2-D interpolations.
    /*! Classes derived from this class will provide interpolated
        values from two sequences of length \f$ N \f$ and \f$ M \f$,
        representing the discretized values of the \f$ x \f$ and \f$ y
        \f$ variables, and a \f$ N \times M \f$ matrix representing
        the tabulated function values.

        \warning See the Interpolation class for information about the
                 required lifetime of the underlying data.
    */
    class Interpolation2D : public Extrapolator {
      protected:
        //! abstract base class for 2-D interpolation implementations
        class Impl {
          public:
            virtual ~Impl() = default;
            virtual void calculate() = 0;
            virtual Real xMin() const = 0;
            virtual Real xMax() const = 0;
            virtual std::vector<Real> xValues() const = 0;
            virtual Size locateX(Real x) const = 0;
            virtual Real yMin() const = 0;
            virtual Real yMax() const = 0;
            virtual std::vector<Real> yValues() const = 0;
            virtual Size locateY(Real y) const = 0;
            virtual const Matrix& zData() const = 0;
            virtual bool isInRange(Real x, Real y) const = 0;
            virtual Real value(Real x, Real y) const = 0;
        };
        ext::shared_ptr<Impl> impl_;
      public:
        //! basic template implementation
        template <class I1, class I2, class M>
        class templateImpl : public Impl {
          public:
            templateImpl(const I1& xBegin, const I1& xEnd,
                         const I2& yBegin, const I2& yEnd,
                         const M& zData)
            : xBegin_(xBegin), xEnd_(xEnd), yBegin_(yBegin), yEnd_(yEnd),
              zData_(zData) {
                QL_REQUIRE(xEnd_-xBegin_ >= 2,
                           "not enough x points to interpolate: at least 2 "
                           "required, " << xEnd_-xBegin_ << " provided");
                QL_REQUIRE(yEnd_-yBegin_ >= 2,
                           "not enough y points to interpolate: at least 2 "
                           "required, " << yEnd_-yBegin_ << " provided");
            }
            Real xMin() const override { return *xBegin_; }
            Real xMax() const override { return *(xEnd_ - 1); }
            std::vector<Real> xValues() const override { return std::vector<Real>(xBegin_, xEnd_); }
            Real yMin() const override { return *yBegin_; }
            Real yMax() const override { return *(yEnd_ - 1); }
            std::vector<Real> yValues() const override { return std::vector<Real>(yBegin_, yEnd_); }
            const Matrix& zData() const override { return zData_; }
            bool isInRange(R
