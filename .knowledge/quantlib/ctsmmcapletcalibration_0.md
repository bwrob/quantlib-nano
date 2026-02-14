/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Ferdinando Ametrano
 Copyright (C) 2007 Mark Joshi

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

#ifndef quantlib_ctsmm_caplet_calibration_hpp
#define quantlib_ctsmm_caplet_calibration_hpp

#include <ql/models/marketmodels/curvestate.hpp>
#include <ql/models/marketmodels/evolutiondescription.hpp>
#include <ql/models/marketmodels/piecewiseconstantcorrelation.hpp>
#include <ql/shared_ptr.hpp>
#include <vector>

namespace QuantLib {

    class PiecewiseConstantVariance;
    class Matrix;

    class CTSMMCapletCalibration {
      public:
        virtual ~CTSMMCapletCalibration() = default;
        CTSMMCapletCalibration(
            EvolutionDescription evolution,
            ext::shared_ptr<PiecewiseConstantCorrelation> corr,
            std::vector<ext::shared_ptr<PiecewiseConstantVariance> > displacedSwapVariances,
            std::vector<Volatility> mktCapletVols, // displaced??
            ext::shared_ptr<CurveState> cs,
            Spread displacement); // ??
        // modifiers
        bool calibrate(Natural numberOfFactors,

                       Natural maxIterations,
                       Real tolerance,

                       Natural innerMaxIterations = 100,
                       Real innerTolerance = 1e-8);
        // inspectors
        Natural failures() const;
        Real deformationSize() const;

        Real capletRmsError() const;
        Real capletMaxError() const;
        Real swaptionRmsError() const;
        Real swaptionMaxError() const;

        const std::vector<Matrix>& swapPseudoRoots() const;
        const Matrix& swapPseudoRoot(Size i) const;

        const std::vector<Volatility>& mktCapletVols() const;
        const std::vector<Volatility>& mdlCapletVols() const;
        const std::vector<Volatility>& mktSwaptionVols() const;
        const std::vector<Volatility>& mdlSwaptionVols() const;
        const std::vector<Volatility>& timeDependentCalibratedSwaptionVols(Size i) const;
        const std::vector<Volatility>& timeDependentUnCalibratedSwaptionVols(Size i) const;


        static void performChecks(
            const EvolutionDescription& evolution,
            const PiecewiseConstantCorrelation& corr,
            const std::vector<ext::shared_ptr<
                        PiecewiseConstantVariance> >&
                                    displacedSwapVariances,
            const std::vector<Volatility>& mktCapletVols,
            const CurveState& cs);

        const ext::shared_ptr<CurveState>& curveState() const;
        std::vector<Spread> displacements() const;
      protected:
        virtual Natural calibrationImpl_(Natural numberOfFactors,

                                         Natural innerMaxIterations,
                                         Real innerTolerance) = 0;
        // input
        EvolutionDescription evolution_;
        ext::shared_ptr<PiecewiseConstantCorrelation> corr_;
        std::vector<ext::shared_ptr<PiecewiseConstantVariance> >
                                                displacedSwapVariances_;

        std::vector<Volatility> mktCapletVols_, mdlCapletVols_;
        std::vector<Volatility> mktSwaptionVols_, mdlSwaptionVols_;
        std::vector<std::vector<Volatility> > timeDependentCalibratedSwaptionVols_;

