/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003, 2004 Roman Gitlin

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

/*! \file multicubicspline.hpp
    \brief N-dimensional cubic spline interpolation between discrete points
*/

#ifndef quantlib_multi_cubic_spline_hpp
#define quantlib_multi_cubic_spline_hpp

#include <ql/errors.hpp>
#include <ql/types.hpp>
#include <algorithm>
#include <functional>
#include <utility>
#include <vector>

namespace QuantLib {

    namespace detail {

        // data structures

        typedef std::vector<std::vector<Real> > SplineGrid;

        // different termination markers are necessary
        // to maintain separation of possibly overlapping types
        struct EmptyArg {};  // arg_type termination marker
        struct EmptyRes {};  // res_type termination marker
        struct EmptyDim {};  // size_t termination marker

        template<class X> struct DataTable {
            DataTable(const std::vector<Size>::const_iterator &i) {
                std::vector<X> temp(*i, X(i + 1));
                data_table_.swap(temp);
            }
            DataTable(const SplineGrid::const_iterator &i) {
                std::vector<X> temp(i->size(), X(i + 1));
                data_table_.swap(temp);
            }
            template<class U> DataTable(const std::vector<U> &v) {
                DataTable temp(v.begin());
                data_table_.swap(temp.data_table_);
            }
            Size size() const {
                return data_table_.size();
            }
            const X &operator[](Size n) const {return data_table_[n];}
            X &operator[](Size n) {return data_table_[n];}
            std::vector<X> data_table_;
        };

        template<> struct DataTable<Real> {
            DataTable(Size n) : data_table_(n) {}
            DataTable(const std::vector<Size>::const_iterator& i)
            : data_table_(*i) {}
            DataTable(const SplineGrid::const_iterator &i)
            : data_table_(i->size()) {}
            template<class U> DataTable(const std::vector<U> &v) {
                DataTable temp(v.begin());
                data_table_.swap(temp.data_table_);
            }
            Size size() const {
                return data_table_.size();
            }
            Real operator[](Size n) const {return data_table_[n];}
            Real& operator[](Size n) {return data_table_[n];}
            std::vector<Real> data_table_;
        };

        typedef DataTable<Real> base_data_table;

        template<class X, class Y> struct Data {
            Data()
            : first(X()), second(Y()) {}
            Data(const SplineGrid::const_iterator &i)
            : first(*i), second(i + 1) {}
            Data(const SplineGrid &v)
            : first(v[0]), second(v.begin()+1) {}
            void swap(Data<X, Y> &d) noexcept {
                first.swap(d.first);
                second.swap(d.second);
            }
            X first;
            Y second;
        };

        template<> struct Data<std::vector<Real>, EmptyArg> {
            Data() = default;
            Data(const SplineGrid::const_iterator &i)
            : first(*i) {}
            Data(const SplineGrid &v)
            : first(v[0]) {}
            Data(std::vector<Real> v) : first(std::move(v)) {}
            void 