/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2001, 2002, 2003 Sadruddin Rejeb
 Copyright (C) 2012 Mateusz Kapturski

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

/*! \file constraint.hpp
    \brief Abstract constraint class
*/

#ifndef quantlib_optimization_constraint_h
#define quantlib_optimization_constraint_h

#include <ql/math/array.hpp>
#include <algorithm>
#include <utility>

namespace QuantLib {

    //! Base constraint class
    class Constraint {
      protected:
        //! Base class for constraint implementations
        class Impl {
          public:
            virtual ~Impl() = default;
            //! Tests if params satisfy the constraint
            virtual bool test(const Array& params) const = 0;
            //! Returns upper bound for given parameters
            virtual Array upperBound(const Array& params) const {
                return Array(params.size(),
                             std::numeric_limits < Array::value_type > ::max());
            }
            //! Returns lower bound for given parameters
            virtual Array lowerBound(const Array& params) const {
                return Array(params.size(),
                             -std::numeric_limits < Array::value_type > ::max());
            }
        };
        ext::shared_ptr<Impl> impl_;
      public:
        bool empty() const { return !impl_; }
        bool test(const Array& p) const { return impl_->test(p); }
        Array upperBound(const Array& params) const {
            Array result = impl_->upperBound(params);
            QL_REQUIRE(params.size() == result.size(),
                       "upper bound size (" << result.size()
                                            << ") not equal to params size ("
                                            << params.size() << ")");
            return result;
        }
        Array lowerBound(const Array& params) const {
            Array result = impl_->lowerBound(params);
            QL_REQUIRE(params.size() == result.size(),
                       "lower bound size (" << result.size()
                                            << ") not equal to params size ("
                                            << params.size() << ")");
            return result;
        }
        Real update(Array& p, const Array& direction, Real beta) const;
        Constraint(ext::shared_ptr<Impl> impl = ext::shared_ptr<Impl>());
    };

    //! No constraint
    class NoConstraint : public Constraint {
      private:
        class Impl final : public Constraint::Impl {
          public:
            bool test(const Array&) const override { return true; }
        };
      public:
        NoConstraint()
        : Constraint(ext::shared_ptr<Constraint::Impl>(
                                                   new NoConstraint::Impl)) {}
    };

    //! %Constraint imposing positivity to all arguments
    class PositiveConstraint : public Constraint {
      private:
        class Impl final : public Constraint::Impl {
          public:
            bool test(const Array& params) const override {
                return std::all_of(params.begin(), params.end(), [](Real p) { return p > 0.0; });
            }
            Array upperBound(const Array& params) const override {
                return Array(params.size(),
                  