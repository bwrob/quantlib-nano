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

/*! \file zabrsmilesection.hpp
    \brief zabr smile section
*/

#ifndef quantlib_zabr_smile_section_hpp
#define quantlib_zabr_smile_section_hpp

#include <ql/experimental/volatility/zabr.hpp>
#include <ql/pricingengines/blackformula.hpp>
#include <ql/termstructures/volatility/smilesection.hpp>
#include <ql/termstructures/volatility/smilesectionutils.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <utility>
#include <vector>

using std::exp;

namespace QuantLib {

// Evaluation Tags

struct ZabrShortMaturityLognormal {};
struct ZabrShortMaturityNormal {};
struct ZabrLocalVolatility {};
struct ZabrFullFd {};

template <typename Evaluation> class ZabrSmileSection : public SmileSection {
  public:
    ZabrSmileSection(Time timeToExpiry,
                     Rate forward,
                     std::vector<Real> zabrParameters,
                     const std::vector<Real>& moneyness = std::vector<Real>(),
                     Size fdRefinement = 5);
    ZabrSmileSection(const Date& d,
                     Rate forward,
                     std::vector<Real> zabrParameters,
                     const DayCounter& dc = Actual365Fixed(),
                     const std::vector<Real>& moneyness = std::vector<Real>(),
                     Size fdRefinement = 5);

    Real minStrike() const override { return 0.0; }
    Real maxStrike() const override { return QL_MAX_REAL; }
    Real atmLevel() const override { return model_->forward(); }
    Real
    optionPrice(Rate strike, Option::Type type = Option::Call, Real discount = 1.0) const override {
        return optionPrice(strike, type, discount, Evaluation());
    }

    ext::shared_ptr<ZabrModel> model() { return model_; }

  protected:
    Volatility volatilityImpl(Rate strike) const override {
        return volatilityImpl(strike, Evaluation());
    }

  private:
    void init(const std::vector<Real> &moneyness) {
        init(moneyness, Evaluation());
        init2(Evaluation());
        init3(Evaluation());
    }
    void init(const std::vector<Real> &moneyness, ZabrShortMaturityLognormal);
    void init(const std::vector<Real> &moneyness, ZabrShortMaturityNormal);
    void init(const std::vector<Real> &moneyness, ZabrLocalVolatility);
    void init(const std::vector<Real> &moneyness, ZabrFullFd);
    void init2(ZabrShortMaturityLognormal);
    void init2(ZabrShortMaturityNormal);
    void init2(ZabrLocalVolatility);
    void init2(ZabrFullFd);
    void init3(ZabrShortMaturityLognormal);
    void init3(ZabrShortMaturityNormal);
    void init3(ZabrLocalVolatility);
    void init3(ZabrFullFd);
    Real optionPrice(Rate strike, Option::Type type, Real discount,
                     ZabrShortMaturityLognormal) const;
    Real optionPrice(Rate strike, Option::Type type, Real discount,
                     ZabrShortMaturityNormal) const;
    Real optionPrice(Rate strike, Option::Type type, Real discount,
                     ZabrLocalVolatility) const;
    Real optionPrice(Rate strike, Option::Type type, Real discount,
                     ZabrFullFd) const;
    Volatility volatilityImpl(Rate strike, ZabrShortMaturityLognormal) const;
    Volatility volatilityImpl(Rate strike, ZabrShort