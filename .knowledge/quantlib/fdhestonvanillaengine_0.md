/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Andreas Gaida
 Copyright (C) 2008 Ralph Schreyer
 Copyright (C) 2008, 2009, 2014 Klaus Spanderen

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

/*! \file fdhestonvanillaengine.hpp
    \brief Finite-differences Heston vanilla option engine
*/

#ifndef quantlib_fd_heston_vanilla_engine_hpp
#define quantlib_fd_heston_vanilla_engine_hpp

#include <ql/instruments/vanillaoption.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/pricingengines/genericmodelengine.hpp>
#include <ql/methods/finitedifferences/solvers/fdmsolverdesc.hpp>
#include <ql/methods/finitedifferences/solvers/fdmbackwardsolver.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>

namespace QuantLib {

    class FdmQuantoHelper;

    //! Finite-differences Heston vanilla option engine
    /*! \ingroup vanillaengines

        \test the correctness of the returned value is tested by
              reproducing results available in web/literature
              and comparison with Black pricing.
    */
    class FdHestonVanillaEngine
        : public GenericModelEngine<HestonModel,
                                    VanillaOption::arguments,
                                    VanillaOption::results> {
      public:
        explicit
        FdHestonVanillaEngine(const ext::shared_ptr<HestonModel>& model,
                              Size tGrid = 100,
                              Size xGrid = 100,
                              Size vGrid = 50,
                              Size dampingSteps = 0,
                              const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
                              ext::shared_ptr<LocalVolTermStructure> leverageFct = {},
                              Real mixingFactor = 1.0);

        FdHestonVanillaEngine(const ext::shared_ptr<HestonModel>& model,
                              DividendSchedule dividends,
                              Size tGrid = 100,
                              Size xGrid = 100,
                              Size vGrid = 50,
                              Size dampingSteps = 0,
                              const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
                              ext::shared_ptr<LocalVolTermStructure> leverageFct = {},
                              Real mixingFactor = 1.0);

        FdHestonVanillaEngine(const ext::shared_ptr<HestonModel>& model,
                              ext::shared_ptr<FdmQuantoHelper> quantoHelper,
                              Size tGrid = 100,
                              Size xGrid = 100,
                              Size vGrid = 50,
                              Size dampingSteps = 0,
                              const FdmSchemeDesc& schemeDesc = FdmSchemeDesc::Hundsdorfer(),
                              ext::shared_ptr<LocalVolTermStructure> leverageFct = {},
                              Real mixingFactor = 1.0);

        FdHestonVanillaEngine(const ext::shared_ptr<HestonModel>& model,
                              DividendSchedule dividends,
                              ext::shared_ptr<FdmQuantoHelper> quantoHelper,
                              Size tGrid = 100,
                              Size xGrid = 100,
                              Size vGrid = 50,

