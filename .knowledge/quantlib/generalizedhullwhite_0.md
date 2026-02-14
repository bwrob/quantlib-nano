/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2010 SunTrust Bank
 Copyright (C) 2010, 2014 Cavit Hafizoglu

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

/*! \file generalizedhullwhite.hpp
    \brief generalized Hull-White model
*/

#ifndef quantlib_generalized_hull_white_hpp
#define quantlib_generalized_hull_white_hpp

#include <ql/experimental/shortrate/generalizedornsteinuhlenbeckprocess.hpp>
#include <ql/math/interpolation.hpp>
#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/processes/ornsteinuhlenbeckprocess.hpp>
#include <utility>

namespace QuantLib {

    //! Parameter that holds an interpolation object
    class InterpolationParameter : public Parameter {
    private:
        class Impl final : public Parameter::Impl {
        public:
          Real value(const Array&, Time t) const override { return interpolator_(t); }
          void reset(const Interpolation& interp) { interpolator_ = interp; }
        private:
            Interpolation interpolator_;
        };
    public:
        explicit InterpolationParameter(
            Size count,
            const Constraint& constraint = NoConstraint())
        : Parameter(count,
            ext::shared_ptr<Parameter::Impl>(
                new InterpolationParameter::Impl()),
                constraint)
        { }
        void reset(const Interpolation &interp) {
            ext::shared_ptr<InterpolationParameter::Impl> impl =
                ext::dynamic_pointer_cast<InterpolationParameter::Impl>(impl_);
            if (impl != nullptr)
                impl->reset(interp);
        }
    };

    //! Generalized Hull-White model class.
    /*! This class implements the standard Black-Karasinski model defined by
        \f[
        d f(r_t) = (\theta(t) - \alpha f(r_t))dt + \sigma dW_t,
        \f]
        where \f$ alpha \f$ and \f$ sigma \f$ are piecewise linear functions.

        \ingroup shortrate
    */
    class GeneralizedHullWhite : public OneFactorAffineModel,
                                 public TermStructureConsistentModel {
      public:

        GeneralizedHullWhite(
            const Handle<YieldTermStructure>& yieldtermStructure,
            const std::vector<Date>& speedstructure,
            const std::vector<Date>& volstructure,
            const std::vector<Real>& speed,
            const std::vector<Real>& vol,
            const std::function<Real(Real)>& f = {},
            const std::function<Real(Real)>& fInverse = {});

        template <class SpeedInterpolationTraits,class VolInterpolationTraits>
        GeneralizedHullWhite(
            const Handle<YieldTermStructure>& yieldtermStructure,
            const std::vector<Date>& speedstructure,
            const std::vector<Date>& volstructure,
            const std::vector<Real>& speed,
            const std::vector<Real>& vol,
            const SpeedInterpolationTraits &speedtraits,
            const VolInterpolationTraits &voltraits,
            const std::function<Real(Real)>& f = {},
            const std::function<Real(Real)>& fInverse = {}) :
            OneFactorAffineModel(2), TermStructureConsistentModel(yieldtermStructure),
            speedstructure_(speedstructure), volstructure_(volstructure),
            a_(arguments_[0]), sigma_(arguments_[1]),
            f_(f), fInverse_(fInverse)

