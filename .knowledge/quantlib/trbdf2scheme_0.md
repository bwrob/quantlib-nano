/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2018 Klaus Spanderen

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

/*! \file trbdf2scheme.hpp
    \brief trapezoidal BDF2 scheme
*/

#ifndef quantlib_tr_bdf2_scheme_hpp
#define quantlib_tr_bdf2_scheme_hpp

#include <ql/math/functional.hpp>
#include <ql/math/matrixutilities/bicgstab.hpp>
#include <ql/math/matrixutilities/gmres.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <ql/methods/finitedifferences/operatortraits.hpp>
#include <ql/methods/finitedifferences/schemes/boundaryconditionschemehelper.hpp>
#include <functional>
#include <utility>

namespace QuantLib {

    template <class TrapezoidalScheme>
    class TrBDF2Scheme {
      public:
        enum SolverType { BiCGstab, GMRES };

        // typedefs
        typedef OperatorTraits<FdmLinearOp> traits;
        typedef traits::operator_type operator_type;
        typedef traits::array_type array_type;
        typedef traits::bc_set bc_set;
        typedef traits::condition_type condition_type;

        // constructors
        TrBDF2Scheme(Real alpha,
                     ext::shared_ptr<FdmLinearOpComposite> map,
                     const ext::shared_ptr<TrapezoidalScheme>& trapezoidalScheme,
                     const bc_set& bcSet = bc_set(),
                     Real relTol = 1e-8,
                     SolverType solverType = BiCGstab);

        void step(array_type& a, Time t);
        void setStep(Time dt);

        Size numberOfIterations() const;
      protected:
        Array apply(const Array& r) const;

        Time dt_;
        Real beta_;
        ext::shared_ptr<Size> iterations_;

        const Real alpha_;
        const ext::shared_ptr<FdmLinearOpComposite> map_;
        const ext::shared_ptr<TrapezoidalScheme>& trapezoidalScheme_;
        const BoundaryConditionSchemeHelper bcSet_;
        const Real relTol_;
        const SolverType solverType_;
    };

    template <class TrapezoidalScheme>
    inline TrBDF2Scheme<TrapezoidalScheme>::TrBDF2Scheme(
        Real alpha,
        ext::shared_ptr<FdmLinearOpComposite> map,
        const ext::shared_ptr<TrapezoidalScheme>& trapezoidalScheme,
        const bc_set& bcSet,
        Real relTol,
        SolverType solverType)
    : dt_(Null<Real>()), beta_(Null<Real>()), iterations_(ext::make_shared<Size>(0U)),
      alpha_(alpha), map_(std::move(map)), trapezoidalScheme_(trapezoidalScheme), bcSet_(bcSet),
      relTol_(relTol), solverType_(solverType) {}

    template <class TrapezoidalScheme>
    inline void TrBDF2Scheme<TrapezoidalScheme>::setStep(Time dt) {
        dt_=dt;
        beta_= (1.0-alpha_)/(2.0-alpha_)*dt_;
    }

    template <class TrapezoidalScheme>
    inline Size TrBDF2Scheme<TrapezoidalScheme>::numberOfIterations() const {
        return *iterations_;
    }

    template <class TrapezoidalScheme>
    inline Array TrBDF2Scheme<TrapezoidalScheme>::apply(const Array& r) const {
        return r - beta_*map_->apply(r);
    }

    template <class TrapezoidalScheme>
    inline void TrBDF2Scheme<TrapezoidalScheme>::step(array_type& fn, Time t) {
        QL_REQUIRE(t-dt_ > -1e-8, "a step towards negative time given");

        const Time intermediateTimeStep = dt_*alpha_;

        array_type fStar = fn;
        trapezoidalScheme_->setStep