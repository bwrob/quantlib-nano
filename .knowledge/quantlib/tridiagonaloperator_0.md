/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006 StatPro Italia srl
 Copyright (C) 2011 Ferdinando Ametrano

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

/*! \file tridiagonaloperator.hpp
    \brief tridiagonal operator
*/

#ifndef quantlib_tridiagonal_operator_hpp
#define quantlib_tridiagonal_operator_hpp

#include <ql/math/array.hpp>
#include <ql/math/comparison.hpp>
#include <ql/shared_ptr.hpp>

namespace QuantLib {

    //! Base implementation for tridiagonal operator
    /*! \warning to use real time-dependent algebra, you must overload
                 the corresponding operators in the inheriting
                 time-dependent class.

        \ingroup findiff
    */
    class TridiagonalOperator {
        // unary operators
        friend TridiagonalOperator operator+(const TridiagonalOperator&);
        friend TridiagonalOperator operator-(const TridiagonalOperator&);
        // binary operators
        friend TridiagonalOperator operator+(const TridiagonalOperator&,
                                             const TridiagonalOperator&);
        friend TridiagonalOperator operator-(const TridiagonalOperator&,
                                             const TridiagonalOperator&);
        friend TridiagonalOperator operator*(Real,
                                             const TridiagonalOperator&);
        friend TridiagonalOperator operator*(const TridiagonalOperator&,
                                             Real);
        friend TridiagonalOperator operator/(const TridiagonalOperator&,
                                             Real);
      public:
        typedef Array array_type;
        // constructors
        explicit TridiagonalOperator(Size size = 0);
        TridiagonalOperator(const Array& low,
                            const Array& mid,
                            const Array& high);
        TridiagonalOperator(const TridiagonalOperator&) = default;
        TridiagonalOperator(TridiagonalOperator&&) noexcept;
        TridiagonalOperator& operator=(const TridiagonalOperator&);
        TridiagonalOperator& operator=(TridiagonalOperator&&) noexcept;
        ~TridiagonalOperator() = default;
        //! \name Operator interface
        //@{
        //! apply operator to a given array
        Array applyTo(const Array& v) const;
        //! solve linear system for a given right-hand side
        Array solveFor(const Array& rhs) const;
        /*! solve linear system for a given right-hand side
            without result Array allocation. The rhs and result parameters
            can be the same Array, in which case rhs will be changed
        */
        void solveFor(const Array& rhs,
                      Array& result) const;
        //! solve linear system with SOR approach
        Array SOR(const Array& rhs,
                  Real tol) const;
        //! identity instance
        static TridiagonalOperator identity(Size size);
        //@}
        //! \name Inspectors
        //@{
        Size size() const { return n_; }
        bool isTimeDependent() const { return !!timeSetter_; }
        const Array& lowerDiagonal() const { return lowerDiagonal_; }
        const Array& diagonal() const { return diagonal_; }
        const Array& upperDiagon