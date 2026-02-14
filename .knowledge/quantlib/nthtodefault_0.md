/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Roland Lichters

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

/*! \file nthtodefault.hpp
    \brief N-th to default swap
*/

#ifndef quantlib_nth_to_default_hpp
#define quantlib_nth_to_default_hpp

#include <ql/instrument.hpp>
#include <ql/cashflow.hpp>
#include <ql/default.hpp>
#include <ql/termstructures/defaulttermstructure.hpp>
#include <ql/experimental/credit/onefactorcopula.hpp>
#include <ql/time/schedule.hpp>

namespace QuantLib {

    class YieldTermStructure;
    class Claim;
    class Basket;

    //--------------------------------------------------------------------------
    //! N-th to default swap
    /*! A NTD instrument exchanges protection against the nth default
        in a basket of underlying credits for premium payments based
        on the protected notional amount.

        The pricing is analogous to the pricing of a CDS instrument
        which represents protection against default of a single
        underlying credit.  The only difference is the calculation of
        the probability of default.  In the CDS case, it is the
        probabilty of single name default; in the NTD case the
        probability of at least N defaults in the portfolio of
        underlying credits.

        This probability is computed using the algorithm in
        John Hull and Alan White, "Valuation of a CDO and nth to
        default CDS without Monte Carlo simulation", Journal of
        Derivatives 12, 2, 2004.

        The algorithm allows for varying probability of default across
        the basket. Otherwise, for identical probabilities of default,
        the probability of n defaults is given by the binomial
        distribution.

        Default correlation is modeled using a one-factor Gaussian copula
        approach.

        The class is tested against data in Hull-White (see reference
        above.)
    */
    class NthToDefault : public Instrument {
      public:
        class arguments;
        class results;
        class engine;

        //! This product is 'digital'; the basket might be tranched but this is
        //  not relevant to it.
        NthToDefault(const ext::shared_ptr<Basket>& basket,
                Size n,
                Protection::Side side,
                Schedule premiumSchedule,
                Rate upfrontRate,
                Rate premiumRate,
                const DayCounter& dayCounter,
                Real nominal,
                bool settlePremiumAccrual);

        bool isExpired() const override;

        // inspectors
        Rate premium() const { return premiumRate_; }
        Real nominal() const { return nominal_; }
        DayCounter dayCounter() const { return dayCounter_; }
        Protection::Side side() const { return side_; }
        Size rank() const { return n_; }
        Size basketSize() const;

        const Date& maturity() const {return premiumSchedule_.endDate();}//???

        const ext::shared_ptr<Basket>& basket() const {return basket_;}

        // results
        Rate fairPremium() const;
        Real premiumLegNPV() const;
        Real protectionLegNPV() const;
        Real errorEstimate() const;

        void setupArguments(PricingEngine::arguments*) const override;
        void fetchResults(const PricingEngine::res
