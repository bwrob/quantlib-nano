/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Klaus Spanderen
 Copyright (C) 2007 StatPro Italia srl
 Copyright (C) 2015, 2016 Peter Caspers
 Copyright (C) 2015 Thema Consulting SA

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

/*! \file mclongstaffschwartzengine.hpp
    \brief Longstaff Schwartz Monte Carlo engine for early exercise options
*/

#ifndef quantlib_mc_longstaff_schwartz_engine_hpp
#define quantlib_mc_longstaff_schwartz_engine_hpp

#include <ql/exercise.hpp>
#include <ql/pricingengines/mcsimulation.hpp>
#include <ql/methods/montecarlo/longstaffschwartzpathpricer.hpp>
#include <ql/optional.hpp>

namespace QuantLib {

    //! Longstaff-Schwarz Monte Carlo engine for early exercise options
    /*! References:

        Francis Longstaff, Eduardo Schwartz, 2001. Valuing American Options
        by Simulation: A Simple Least-Squares Approach, The Review of
        Financial Studies, Volume 14, No. 1, 113-147

        \test the correctness of the returned value is tested by
              reproducing results available in web/literature
    */
    template <class GenericEngine, template <class> class MC,
              class RNG, class S = Statistics, class RNG_Calibration = RNG>
    class MCLongstaffSchwartzEngine : public GenericEngine,
                                      public McSimulation<MC,RNG,S> {
      public:
        typedef typename MC<RNG>::path_type path_type;
        typedef typename McSimulation<MC,RNG,S>::stats_type
            stats_type;
        typedef typename McSimulation<MC,RNG,S>::path_pricer_type
            path_pricer_type;
        typedef typename McSimulation<MC,RNG,S>::path_generator_type
            path_generator_type;
        typedef
            typename McSimulation<MC, RNG_Calibration, S>::path_generator_type
                path_generator_type_calibration;

        /*! If the parameters brownianBridge and antitheticVariate are
          not given they are chosen to be identical to the respective
          parameters for pricing; the seed for calibration is chosen
          to be zero if the pricing seed is zero and otherwise as the
          pricing seed plus some offset to avoid identical paths in
          calibration and pricing; note however that this has no effect
          for low discrepancy RNGs usually, it is therefore recommended
          to use pseudo random generators for the calibration phase always
          (and possibly quasi monte carlo in the subsequent pricing). */
        MCLongstaffSchwartzEngine(ext::shared_ptr<StochasticProcess> process,
                                  Size timeSteps,
                                  Size timeStepsPerYear,
                                  bool brownianBridge,
                                  bool antitheticVariate,
                                  bool controlVariate,
                                  Size requiredSamples,
                                  Real requiredTolerance,
                                  Size maxSamples,
                                  BigNatural seed,
                                  Size nCalibrationSamples = Null<Size>(),
                                  ext::optional<bool> brownianBridgeCalibration = ext::nullopt,
                                  ext::optional<bool> antitheticVariateCalibration = ext::null
