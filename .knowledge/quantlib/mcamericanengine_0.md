/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Klaus Spanderen
 Copyright (C) 2007 StatPro Italia srl
 Copyright (C) 2016 Peter Caspers
 Copyright (C) 2022 Jonghee Lee

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

/*! \file mcamericanengine.hpp
    \brief American Monte Carlo engine
*/

#ifndef quantlib_mc_american_engine_hpp
#define quantlib_mc_american_engine_hpp

#include <ql/qldefines.hpp>
#include <ql/payoff.hpp>
#include <ql/exercise.hpp>
#include <ql/optional.hpp>
#include <ql/methods/montecarlo/lsmbasissystem.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/pricingengines/mclongstaffschwartzengine.hpp>
#include <ql/pricingengines/vanilla/mceuropeanengine.hpp>
#include <ql/pricingengines/vanilla/analyticeuropeanengine.hpp>

namespace QuantLib {

    //! American Monte Carlo engine
    /*! References:

        \ingroup vanillaengines

        \test the correctness of the returned value is tested by
              reproducing results available in web/literature
    */
    template <class RNG = PseudoRandom, class S = Statistics,
              class RNG_Calibration = RNG>
    class MCAmericanEngine
        : public MCLongstaffSchwartzEngine<VanillaOption::engine,
                                           SingleVariate,RNG,S,RNG_Calibration> {
      public:
        MCAmericanEngine(const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
                         Size timeSteps,
                         Size timeStepsPerYear,
                         bool antitheticVariate,
                         bool controlVariate,
                         Size requiredSamples,
                         Real requiredTolerance,
                         Size maxSamples,
                         BigNatural seed,
                         Size polynomialOrder,
                         LsmBasisSystem::PolynomialType polynomialType,
                         Size nCalibrationSamples = Null<Size>(),
                         const ext::optional<bool>& antitheticVariateCalibration = ext::nullopt,
                         BigNatural seedCalibration = Null<Size>());

        void calculate() const override;

      protected:
        ext::shared_ptr<LongstaffSchwartzPathPricer<Path> > lsmPathPricer() const override;

        Real controlVariateValue() const override;
        ext::shared_ptr<PricingEngine> controlPricingEngine() const override;
        ext::shared_ptr<PathPricer<Path> > controlPathPricer() const override;

      private:
        const Size polynomialOrder_;
        const LsmBasisSystem::PolynomialType polynomialType_;
    };

    class AmericanPathPricer : public EarlyExercisePathPricer<Path>  {
      public:
        AmericanPathPricer(ext::shared_ptr<Payoff> payoff,
                           Size polynomialOrder,
                           LsmBasisSystem::PolynomialType polynomialType);

        Real state(const Path& path, Size t) const override;
        Real operator()(const Path& path, Size t) const override;

        std::vector<std::function<Real(Real)> > basisSystem() const override;

      protected:
        Real payoff(Real state) const;

        Real scalingValue_ = 1.0;
        const ext::shared_ptr<Payoff> payoff_;
        std::vector<std::function<Real(Real)> > v_;
    };


    //! Monte Carlo American engine facto