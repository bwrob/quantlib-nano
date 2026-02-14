/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2004, 2005, 2008 Klaus Spanderen
 Copyright (C) 2007 StatPro Italia srl

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

/*! \file analytichestonengine.hpp
    \brief analytic Heston-model engine
*/

#ifndef quantlib_analytic_heston_engine_hpp
#define quantlib_analytic_heston_engine_hpp

#include <ql/utilities/null.hpp>
#include <ql/math/integrals/integral.hpp>
#include <ql/math/integrals/gaussianquadratures.hpp>
#include <ql/pricingengines/genericmodelengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/instruments/vanillaoption.hpp>
#include <functional>
#include <complex>

namespace QuantLib {

    //! analytic Heston-model engine based on Fourier transform

    /*! Integration detail:
        Two algebraically equivalent formulations of the complex
        logarithm of the Heston model exist. Gatherals [2005]
        (also Duffie, Pan and Singleton [2000], and Schoutens,
        Simons and Tistaert[2004]) version does not cause
        discoutinuities whereas the original version (e.g. Heston [1993])
        needs some sort of "branch correction" to work properly.
        Gatheral's version does also work with adaptive integration
        routines and should be preferred over the original Heston version.
    */

    /*! References:

        Heston, Steven L., 1993. A Closed-Form Solution for Options
        with Stochastic Volatility with Applications to Bond and
        Currency Options.  The review of Financial Studies, Volume 6,
        Issue 2, 327-343.

        A. Sepp, Pricing European-Style Options under Jump Diffusion
        Processes with Stochastic Volatility: Applications of Fourier
        Transform (<http://math.ut.ee/~spartak/papers/stochjumpvols.pdf>)

        R. Lord and C. Kahl, Why the rotation count algorithm works,
        http://papers.ssrn.com/sol3/papers.cfm?abstract_id=921335

        H. Albrecher, P. Mayer, W.Schoutens and J. Tistaert,
        The Little Heston Trap, http://www.schoutens.be/HestonTrap.pdf

        J. Gatheral, The Volatility Surface: A Practitioner's Guide,
        Wiley Finance

        F. Le Floc'h, Fourier Integration and Stochastic Volatility
        Calibration,
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2362968

        L. Andersen, and V. Piterbarg, 2010,
        Interest Rate Modeling, Volume I: Foundations and Vanilla Models,
        Atlantic Financial Press London.

        L. Andersen and M. Lake, 2018
        Robust High-Precision Option Pricing by Fourier Transforms:
        Contour Deformations and Double-Exponential Quadrature,
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3231626

        \ingroup vanillaengines

        \test the correctness of the returned value is tested by
              reproducing results available in web/literature
              and comparison with Black pricing.
    */
    class AnalyticHestonEngine
        : public GenericModelEngine<HestonModel,
                                    VanillaOption::arguments,
                                    VanillaOption::results> {
      public:
        class Integration;
        class OptimalAlpha;
        class AP_Helper;

        enum ComplexLogFormula {
            // Gatheral form of characteristic function w/o control variate

