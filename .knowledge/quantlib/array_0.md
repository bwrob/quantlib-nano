/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006, 2009 StatPro Italia srl
 Copyright (C) 2004 Ferdinando Ametrano

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

/*! \file array.hpp
    \brief 1-D array used in linear algebra.
*/

#ifndef quantlib_array_hpp
#define quantlib_array_hpp

#include <ql/types.hpp>
#include <ql/errors.hpp>
#include <ql/utilities/null.hpp>
#include <iterator>
#include <functional>
#include <algorithm>
#include <numeric>
#include <vector>
#include <initializer_list>
#include <iomanip>
#include <memory>
#include <type_traits>

namespace QuantLib {

    //! 1-D array used in linear algebra.
    /*! This class implements the concept of vector as used in linear
        algebra.
        As such, it is <b>not</b> meant to be used as a container -
        <tt>std::vector</tt> should be used instead.

        \test construction of arrays is checked in a number of cases
    */
    class Array {
      public:
        //! \name Constructors, destructor, and assignment
        //@{
        //! creates the array with size 0
        Array() : Array(static_cast<Size>(0)) {}
        //! creates the array with the given dimension
        explicit Array(Size size);
        //! creates the array and fills it with <tt>value</tt>
        Array(Size size, Real value);
        /*! \brief creates the array and fills it according to
            \f$ a_{0} = value, a_{i}=a_{i-1}+increment \f$
        */
        Array(Size size, Real value, Real increment);
        Array(const Array&);
        Array(Array&&) noexcept;
        Array(std::initializer_list<Real>);
        template <typename T, typename = std::enable_if_t<std::is_convertible_v<T, Real>>>
        Array(std::initializer_list<T> init);
        //! creates the array from an iterable sequence
        template <class ForwardIterator>
        Array(ForwardIterator begin, ForwardIterator end);
        ~Array() = default;

        Array& operator=(const Array&);
        Array& operator=(Array&&) noexcept;

        bool operator==(const Array&) const;
        bool operator!=(const Array&) const;
        //@}
        /*! \name Vector algebra

            <tt>v += x</tt> and similar operation involving a scalar value
            are shortcuts for \f$ \forall i : v_i = v_i + x \f$

            <tt>v *= w</tt> and similar operation involving two vectors are
            shortcuts for \f$ \forall i : v_i = v_i \times w_i \f$

            \pre all arrays involved in an algebraic expression must have
            the same size.
        */
        //@{
        const Array& operator+=(const Array&);
        const Array& operator+=(Real);
        const Array& operator-=(const Array&);
        const Array& operator-=(Real);
        const Array& operator*=(const Array&);
        const Array& operator*=(Real);
        const Array& operator/=(const Array&);
        const Array& operator/=(Real);
        //@}
        //! \name Element access
        //@{
        //! read-only
        Real operator[](Size) const;
        Real at(Size) const;
        Real front() const;
        Real back() const;
        //! read-write
        Real& operator[](Size);
        Real& at(Size);
        Real& front();
        Real& back();
        //@}
        //! \name