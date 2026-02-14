/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2014 Peter Caspers

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

/*! \file zabrinterpolatedsmilesection.hpp
    \brief zabr interpolating smile section
*/

#ifndef quantlib_zabr_interpolated_smile_section_hpp
#define quantlib_zabr_interpolated_smile_section_hpp

#include <ql/experimental/volatility/zabrinterpolation.hpp>
#include <ql/handle.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/quotes/simplequote.hpp>
#include <ql/termstructures/volatility/smilesection.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <utility>

namespace QuantLib {

template <typename Evaluation>
class ZabrInterpolatedSmileSection : public SmileSection, public LazyObject {
  public:
    //! \name Constructors
    //@{
    //! all market data are quotes
    ZabrInterpolatedSmileSection(
        const Date& optionDate,
        Handle<Quote> forward,
        const std::vector<Rate>& strikes,
        bool hasFloatingStrikes,
        Handle<Quote> atmVolatility,
        const std::vector<Handle<Quote> >& volHandles,
        Real alpha,
        Real beta,
        Real nu,
        Real rho,
        Real gamma,
        bool isAlphaFixed = false,
        bool isBetaFixed = false,
        bool isNuFixed = false,
        bool isRhoFixed = false,
        bool isGammaFixed = false,
        bool vegaWeighted = true,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    //! no quotes
    ZabrInterpolatedSmileSection(
        const Date& optionDate,
        const Rate& forward,
        const std::vector<Rate>& strikes,
        bool hasFloatingStrikes,
        const Volatility& atmVolatility,
        const std::vector<Volatility>& vols,
        Real alpha,
        Real beta,
        Real nu,
        Real rho,
        Real gamma,
        bool isAlphaFixed = false,
        bool isBetaFixed = false,
        bool isNuFixed = false,
        bool isRhoFixed = false,
        bool isGammaFixed = false,
        bool vegaWeighted = true,
        ext::shared_ptr<EndCriteria> endCriteria = ext::shared_ptr<EndCriteria>(),
        ext::shared_ptr<OptimizationMethod> method = ext::shared_ptr<OptimizationMethod>(),
        const DayCounter& dc = Actual365Fixed());
    //@}
    //! \name LazyObject interface
    //@{
    void performCalculations() const override;
    void update() override;
    //@}
    //! \name SmileSection interface
    //@{
    Real minStrike() const override;
    Real maxStrike() const override;
    Real atmLevel() const override;
    //@}
    Real varianceImpl(Rate strike) const override;
    Volatility volatilityImpl(Rate strike) const override;
    //! \name Inspectors
    //@{
    Real alpha() const;
    Real beta() const;
    Real nu() const;
    Real rho() const;
    Real gamma() const;
    Real rmsError() const;
    Real maxError() const;
    EndCriteria::Type endCriteria() const;
    //@}

  protected:
    //! Creates the mutable SABRInterpolation
    void createInterpolation() const;
    mutable ext::shared_ptr<ZabrInterpolation<Evaluation> > zabrInterpolation_;

    //! Market data
    const Handle<Quote> forward_;
    const Handle<