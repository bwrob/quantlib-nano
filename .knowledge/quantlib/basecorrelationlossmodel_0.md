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

#ifndef quantlib_base_correl_lossmodel_hpp
#define quantlib_base_correl_lossmodel_hpp


#include <ql/quote.hpp>
#include <ql/quotes/simplequote.hpp>

#include <ql/experimental/credit/basket.hpp>
#include <ql/experimental/credit/defaultlossmodel.hpp>
#include <ql/experimental/credit/basecorrelationstructure.hpp>

// move these to the CPP (and the template spezs)
#include <ql/experimental/credit/binomiallossmodel.hpp>
#include <ql/experimental/credit/gaussianlhplossmodel.hpp>
#include <ql/experimental/credit/inhomogeneouspooldef.hpp>
#include <utility>

namespace QuantLib {

    /*! Base Correlation loss model; interpolation is performed by portfolio 
    (live) amount percentage.\par
    Though the literature on this model is inmense, see for a more than 
    introductory level (precrisis) chapters 19, 20 and 21 of <b>Modelling single
    name and multi-name credit derivatives.</b> Dominic O'Kane, Wiley Finance, 
    2008\par
    For freely available documentation see:\par
    Credit Correlation: A Guide; JP Morgan Credit Derivatives Strategy; 
        12 March 2004 \par
    Introducing Base Correlations; JP Morgan Credit Derivatives Strategy; 
        22 March 2004 \par
    A Relative Value Framework for Credit Correlation; JP Morgan Credit 
        Derivatives Strategy; 27 April 2004 \par
    Valuing and Hedging Synthetic CDO Tranches Using Base Correlations; Bear 
        Stearns; May 17, 2004 \par
    Correlation Primer; Nomura Fixed Income Research, August 6, 2004 \par
    Base Correlation Explained; Lehman Brothers Fixed Income Quantitative 
        Credit Research; 15 November 2004 \par
    'Pricing CDOs with a smile' in Societe Generale Credit Research; 
        February 2005 \par
    For bespoke base correlation see: \par
    Base Correlation Mapping in Lehman Brothers' Quantitative Credit Research 
        Quarterly; Volume 2007-Q1 \par
    You can explore typical postcrisis data by perusing some of the JPMorgan 
    Global Correlation Daily Analytics \par
    Here the crisis model problems of ability to price stressed portfolios 
    or tranches over the maximum loss are the responsibility of the base models.
    Users should select their models according to this; choosing the copula or
    a random loss given default base model (or more exotic ones). \par
    Notice this is different to a bespoke base correlation loss (bespoke here 
    referring to basket composition, not just attachment levels) ; where 
    loss interpolation is on the expected loss value to match the two baskets. 
    Therefore the correlation surface should refer to the same basket intended
    to be priced. But this is left to the user and is not implemented in the 
    correlation surface (yet...)

    \todo Bespoke portfolios BC models are yet to be implemented.

    BaseModel_T must have a constructor with a single quote value
    */
    /* Criticism:
    This model is not as generic as it could be. In principle a default loss 
    model dependent on a single factor correlation parameter is the only 
    restriction on the base loss model(s) type. This class however is tied to a 
    LatentModel single factor. But there is no need for the 
    underlyi