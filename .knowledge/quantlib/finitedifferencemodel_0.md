/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl

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

/*! \file finitedifferencemodel.hpp
    \brief generic finite difference model
*/

#ifndef quantlib_finite_difference_model_hpp
#define quantlib_finite_difference_model_hpp

#include <ql/methods/finitedifferences/boundarycondition.hpp>
#include <ql/methods/finitedifferences/operatortraits.hpp>
#include <ql/methods/finitedifferences/stepcondition.hpp>
#include <utility>

namespace QuantLib {

    //! Generic finite difference model
    /*! \ingroup findiff */
    template<class Evolver>
    class FiniteDifferenceModel {
      public:
        typedef typename Evolver::traits traits;
        typedef typename traits::operator_type operator_type;
        typedef typename traits::array_type array_type;
        typedef typename traits::bc_set bc_set;
        typedef typename traits::condition_type condition_type;
        // constructors
        FiniteDifferenceModel(const operator_type& L,
                              const bc_set& bcs,
                              std::vector<Time> stoppingTimes = std::vector<Time>())
        : evolver_(L, bcs), stoppingTimes_(std::move(stoppingTimes)) {
            std::sort(stoppingTimes_.begin(), stoppingTimes_.end());
            auto last = std::unique(stoppingTimes_.begin(), stoppingTimes_.end());
            stoppingTimes_.erase(last, stoppingTimes_.end());
        }
        FiniteDifferenceModel(Evolver evolver,
                              std::vector<Time> stoppingTimes = std::vector<Time>())
        : evolver_(std::move(evolver)), stoppingTimes_(std::move(stoppingTimes)) {
            std::sort(stoppingTimes_.begin(), stoppingTimes_.end());
            auto last = std::unique(stoppingTimes_.begin(), stoppingTimes_.end());
            stoppingTimes_.erase(last, stoppingTimes_.end());
        }
        // methods
        // array_type grid() const { return evolver.xGrid(); }
        const Evolver& evolver() const{ return evolver_; }
        /*! solves the problem between the given times.
            \warning being this a rollback, <tt>from</tt> must be a later
                     time than <tt>to</tt>.
        */
        void rollback(array_type& a,
                      Time from,
                      Time to,
                      Size steps) {
            rollbackImpl(a, from, to, steps, (const condition_type*)nullptr);
        }
        /*! solves the problem between the given times,
            applying a condition at every step.
            \warning being this a rollback, <tt>from</tt> must be a later
                     time than <tt>to</tt>.
        */
        void rollback(array_type& a,
                      Time from,
                      Time to,
                      Size steps,
                      const condition_type& condition) {
            rollbackImpl(a,from,to,steps,&condition);
        }
      private:
        void rollbackImpl(array_type& a,
                          Time from,
                          Time to,
                          Size steps,
                          const condition_type* condition) {

            QL_REQUIRE(from >= to,
                       "trying to roll back from " << from << " to " << to);

            Time dt = (from-to)/st
