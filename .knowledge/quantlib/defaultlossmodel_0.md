/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Roland Lichters
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

#ifndef quantlib_defaultlossmodel_hpp
#define quantlib_defaultlossmodel_hpp

#include <ql/instruments/claim.hpp>
#include <ql/experimental/credit/defaultprobabilitykey.hpp>
#include <ql/experimental/credit/basket.hpp>

#include <ql/utilities/null_deleter.hpp>

/* Intended to replace LossDistribution in 
    ql/experimental/credit/lossdistribution, not sure its covering all the 
    functionality (see mthod below)
*/

namespace QuantLib {

    /*! Default loss model interface definition.
    Allows communication between the basket and specific algorithms. Intended to
    hold any kind of portfolio joint loss, latent models, top-down,....

    An inconvenience of this design as opposed to the full arguments/results
    is that when pricing several derivatives instruments on the same basket
    not all the pricing engines would point to the same loss model; thus when
    pricing a set of such instruments there might be some switching on the 
    basket loss models, which might require recalculations (of the basket) or 
    not depending on the pricing order.
    */
    class DefaultLossModel : public Observable {// joint-? basket?-defaultLoss
     /* Protection together with frienship to avoid the need of checking the 
     basket-argument pointer integrity. It is the responsibility of the basket 
     now; our only caller.
     */
        friend class Basket;
    protected:
        // argument basket:
        mutable RelinkableHandle<Basket> basket_;

        DefaultLossModel() = default;
        //! \name Statistics
        //@{
        /* Non mandatory implementations, fails if client is not providing what 
        requested. */

        /* Default implementation using the expectedLoss(Date) method. 
          Typically this method is called repeatedly with the same 
          date parameter which makes it innefficient. */
        virtual Real expectedTrancheLoss(const Date& d) const {
            QL_FAIL("expectedTrancheLoss Not implemented for this model.");
        }
        /*! Probability of the tranche losing the same or more than the 
            fractional amount given.

            The passed lossFraction is a fraction of losses over the
            tranche notional (not the portfolio).
        */
        virtual Probability probOverLoss(
            const Date& d, Real lossFraction) const {
            QL_FAIL("probOverLoss Not implemented for this model.");   
        }
        //! Value at Risk given a default loss percentile.
        virtual Real percentile(const Date& d, Real percentile) const {
            QL_FAIL("percentile Not implemented for this model.");   
        }
        //! Expected shortfall given a default loss percentile.
        virtual Real expectedShortfall(const Date& d, Real percentile) const {
            QL_FAIL("eSF Not implemented for this model.");   
        }
        //! Associated VaR fraction to each counterparty.
        virtual std::vector<Real> splitVaRLevel(const Date& d, Real loss) const {
            QL_FAIL("splitVaRLevel Not implemented for this model.");   
        }
        //! Associated ESF fraction to each counterparty.
        virtual std::vector