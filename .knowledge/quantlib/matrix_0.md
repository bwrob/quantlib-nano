/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006 StatPro Italia srl
 Copyright (C) 2003, 2004 Ferdinando Ametrano
 Copyright (C) 2015 Michael von den Driesch
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

/*! \file matrix.hpp
    \brief matrix used in linear algebra.
*/

#ifndef quantlib_matrix_hpp
#define quantlib_matrix_hpp

#include <ql/math/array.hpp>
#include <ql/utilities/steppingiterator.hpp>
#include <initializer_list>
#include <iterator>

namespace QuantLib {

    //! %Matrix used in linear algebra.
    /*! This class implements the concept of Matrix as used in linear
        algebra. As such, it is <b>not</b> meant to be used as a
        container.
    */
    class Matrix {
      public:
        //! \name Constructors, destructor, and assignment
        //@{
        //! creates a null matrix
        Matrix();
        //! creates a matrix with the given dimensions
        Matrix(Size rows, Size columns);
        //! creates the matrix and fills it with <tt>value</tt>
        Matrix(Size rows, Size columns, Real value);
        //! creates the matrix and fills it with data from a range.
        /*! \warning if the range defined by [begin, end) is larger
            than the size of the matrix, a memory access violation
            might occur.  It is up to the user to avoid this.
        */
        template <class Iterator>
        Matrix(Size rows, Size columns, Iterator begin, Iterator end);
        Matrix(const Matrix&);
        Matrix(Matrix&&) noexcept;
        Matrix(std::initializer_list<std::initializer_list<Real>>);
        ~Matrix() = default;

        Matrix& operator=(const Matrix&);
        Matrix& operator=(Matrix&&) noexcept;

        bool operator==(const Matrix&) const;
        bool operator!=(const Matrix&) const;
        //@}

        //! \name Algebraic operators
        /*! \pre all matrices involved in an algebraic expression must have
                 the same size.
        */
        //@{
        const Matrix& operator+=(const Matrix&);
        const Matrix& operator-=(const Matrix&);
        const Matrix& operator*=(Real);
        const Matrix& operator/=(Real);
        //@}

        typedef Real* iterator;
        typedef const Real* const_iterator;
        typedef std::reverse_iterator<iterator> reverse_iterator;
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
        typedef Real* row_iterator;
        typedef const Real* const_row_iterator;
        typedef std::reverse_iterator<row_iterator> reverse_row_iterator;
        typedef std::reverse_iterator<const_row_iterator>
                                                const_reverse_row_iterator;
        typedef step_iterator<iterator> column_iterator;
        typedef step_iterator<const_iterator> const_column_iterator;
        typedef std::reverse_iterator<column_iterator>
                                                   reverse_column_iterator;
        typedef std::reverse_iterator<const_column_iterator>
                                             const_reverse_column_iterator;
        //! \name Iterator access
        //@{
        const_iterator begin() const;
        iterator begin();
        const_iterator end() const;
        iterator end();
        const_
