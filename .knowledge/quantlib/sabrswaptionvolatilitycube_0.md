/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006, 2007 Giorgio Facchinetti
 Copyright (C) 2014, 2015 Peter Caspers
 Copyright (C) 2023 Ignacio Anguita

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

/*! \file sabrswaptionvolatilitycube.hpp
    \brief Swaption volatility cube, fit-early-interpolate-later approach
           The provided types are
           SabrSwaptionVolatilityCube using the classic Hagan 2002 Sabr formula
           NoArbSabrSwaptionVolatilityCube using the No Arbitrage Sabr model (Doust)
*/

#ifndef quantlib_sabr_swaption_volatility_cube_hpp
#define quantlib_sabr_swaption_volatility_cube_hpp

#include <ql/math/interpolations/backwardflatlinearinterpolation.hpp>
#include <ql/math/interpolations/bilinearinterpolation.hpp>
#include <ql/math/interpolations/flatextrapolation2d.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/math/interpolations/sabrinterpolation.hpp>
#include <ql/math/matrix.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/volatility/sabrsmilesection.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolcube.hpp>
#include <utility>


#ifndef SWAPTIONVOLCUBE_VEGAWEIGHTED_TOL
    #define SWAPTIONVOLCUBE_VEGAWEIGHTED_TOL 15.0e-4
#endif
#ifndef SWAPTIONVOLCUBE_TOL
    #define SWAPTIONVOLCUBE_TOL 100.0e-4
#endif

namespace QuantLib {

    class Interpolation2D;
    class EndCriteria;
    class OptimizationMethod;

    //! XABR Swaption Volatility Cube
    /*! This class implements the XABR Swaption Volatility Cube
        which is a generic for different SABR, ZABR and
        different smile models that can be used to instantiate concrete cubes.
    */
    template<class Model>
    class XabrSwaptionVolatilityCube : public SwaptionVolatilityCube {
        class Cube { // NOLINT(cppcoreguidelines-special-member-functions)
          public:
            Cube() = default;
            Cube(const std::vector<Date>& optionDates,
                 const std::vector<Period>& swapTenors,
                 const std::vector<Time>& optionTimes,
                 const std::vector<Time>& swapLengths,
                 Size nLayers,
                 bool extrapolation = true,
                 bool backwardFlat = false);
            Cube& operator=(const Cube& o);
            Cube(const Cube&);
            virtual ~Cube() = default;
            void setElement(Size IndexOfLayer,
                            Size IndexOfRow,
                            Size IndexOfColumn,
                            Real x);
            void setPoints(const std::vector<Matrix>& x);
            void setPoint(const Date& optionDate,
                          const Period& swapTenor,
                          Time optionTime,
                          Time swapLength,
                          const std::vector<Real>& point);
            void setLayer(Size i,
                          const Matrix& x);
            void expandLayers(Size i,
                              bool expandOptionTimes,
                              Size j,
                              bool expandSwapLengths);
            const std::vector<Date>& optionDates() const {
                return optionDates_;
            }
            const std::vector<Period>& swapTenors() const {
                return swapTenors_;
            }

