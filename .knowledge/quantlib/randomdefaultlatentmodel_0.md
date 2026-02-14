/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Roland Lichters
 Copyright (C) 2009, 2014 Jose Aparicio

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

#ifndef quantlib_randomdefault_latent_model_hpp
#define quantlib_randomdefault_latent_model_hpp

#include <ql/experimental/credit/basket.hpp>
#include <ql/experimental/credit/constantlosslatentmodel.hpp>
#include <ql/experimental/credit/defaultlossmodel.hpp>
#include <ql/experimental/math/gaussiancopulapolicy.hpp>
#include <ql/experimental/math/latentmodel.hpp>
#include <ql/experimental/math/tcopulapolicy.hpp>
#include <ql/math/beta.hpp>
#include <ql/math/randomnumbers/mt19937uniformrng.hpp>
#include <ql/math/randomnumbers/sobolrsg.hpp>
#include <ql/math/solvers1d/brent.hpp>
#include <ql/math/statistics/histogram.hpp>
#include <ql/math/statistics/riskstatistics.hpp>
#include <tuple>
#include <utility>

/* Intended to replace
    ql\experimental\credit\randomdefaultmodel.Xpp
*/

namespace QuantLib {

    /*! Simulation event trait class template forward declaration.
    Each latent model will be modelling different entities according to the
    meaning of the model function which depends on the random \$ Y_i\$
    variables. Still the generation of the factors and variables it is common to
    any model. Only within a given transformation function the model and event
    generated becomes concrete.

    However here these simulations are already made specific to a default event.
    Yet other variables contingent to default can be modelled (recovery,
    market...) So we are placed in a less generic stage where default is
    modelled possibly jointly with other unespecified magnitudes.

    Another role of this trait class is to compact in memory the simulation
    data. The statistic post processing needs to have the results stored in
    memory and simulations can not be consumed at generation time, typically
    because some statistics are conditional on others (e.g. ESF) or/and
    parametric (percentile, etc...)

    Simulation events do not derive from each other, and they are specialized
    for each type; duck typing applies for variable names (see the statistic
    methods)
    */
    // replaces class Loss
    template <class simEventOwner> struct simEvent;


    /*! Base class for latent model monte carlo simulation. Independent of the
    copula type and the generator.
    Generates the factors and variable samples and determines event threshold
    but it is not responsible for actual event specification; thats the derived
    classes responsibility according to what they model.
    Derived classes need mainly to implement nextSample (Worker::nextSample in
    the multithreaded version) to compute the simulation event generated, if
    any, from the latent variables sample. They also have the accompanying
    event trait to specify.
    */
    /* CRTP used for performance to avoid virtual table resolution in the Monte
    Carlo. Not only in sample generation but access; quite an amount of time can
    go into statistics computation, for a portfolio of tens of thousands
    positions that part of the problem will be starting to overtake the
    simulation costs.

    \todo: someone with sound experience on cache misses look into this, the
    statistics will be getting memory in and o
