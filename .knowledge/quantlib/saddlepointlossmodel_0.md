/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2014 Jose Aparicio

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

#ifndef quantlib_saddle_point_lossmodel_hpp
#define quantlib_saddle_point_lossmodel_hpp

#include <ql/math/solvers1d/brent.hpp>
#include <ql/math/solvers1d/newton.hpp>
#include <ql/experimental/credit/basket.hpp>
#include <ql/experimental/credit/defaultlossmodel.hpp>
#include <ql/experimental/credit/constantlosslatentmodel.hpp>
#include <tuple>

namespace QuantLib {

    /*! \brief Saddle point portfolio credit default loss model.\par
      Default Loss model implementing the Saddle point expansion 
      integrations on several default risk metrics. Codepence is dealt 
      through a latent model making the integrals conditional to the latent 
      model factor. Latent variables are integrated indirectly.\par
    See:\par
    <b>Taking to the saddle</b> by R.Martin, K.Thompson and C.Browne; RISK JUNE 
        2001; p.91\par
    <b>The saddlepoint method and portfolio optionalities</b> R.Martin in Risk 
        December 2006\par
    <b>VAR: who contributes and how much?</b> R.Martin, K.Thompson and 
        C.Browne RISK AUGUST 2001\par
    <b>Shortfall: Who contributes and how much?</b> R. J. Martin, Credit Suisse 
        January 3, 2007 \par
    <b>Don't Fall from the Saddle: the Importance of Higher Moments of Credit 
        Loss Distributions</b> J.Annaert, C.Garcia Joao Batista, J.Lamoot, 
        G.Lanine February 2006, Gent University\par
    <b>Analytical techniques for synthetic CDOs and credit default risk 
        measures</b> A. Antonov, S. Mechkovy, and T. Misirpashaevz; 
        NumeriX May 23, 2005 \par
    <b>Computation of VaR and VaR contribution in the Vasicek portfolio credit 
        loss model: a comparative study</b> X.Huang, C.W.Oosterlee, M.Mesters
        Journal of Credit Risk (75-96) Volume 3/ Number 3, Fall 2007 \par
    <b>Higher-order saddlepoint approximations in the Vasicek portfolio credit 
        loss model</b> X.Huang, C.W.Oosterlee, M.Mesters  Journal of 
        Computational Finance (93-113) Volume 11/Number 1, Fall 2007 \par
    While more expensive, a high order expansion is used here; see the paper by 
    Antonov et al for the terms retained.\par
    For a discussion of an alternative to fix the error at low loss levels 
    (more relevant to pricing than risk metrics) see: \par
    <b>The hybrid saddlepoint method for credit portfolios</b> by A.Owen, 
    A.McLeod and K.Thompson; in Risk, August 2009. This is not implemented here
    though (yet?...)\par
    For the more general context mathematical theory see: <b>Saddlepoint 
    approximations with applications</b> by R.W. Butler, Cambridge series in 
    statistical and probabilistic mathematics. 2007 \par
    \todo Some portfolios show instabilities in the high order expansion terms.
    \todo Methods here are calling and integrating using the unconditional 
        probabilities without inverting them first; quite a lot of calls to 
        the copula inversion can be avoided; this should improve performance.
    \todo Revise the model for stability of the saddle point calculation. The
        search for the point does not convege in extreme cases; e.g. very high
        value of all the factors; factors for each variable not ordered 