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

/*! \file basket.hpp
    \brief basket of issuers and related notionals
*/

#ifndef quantlib_basket_hpp
#define quantlib_basket_hpp

#include <ql/instruments/claim.hpp>
#include <ql/termstructures/defaulttermstructure.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/experimental/credit/defaultprobabilitykey.hpp>
#include <ql/experimental/credit/issuer.hpp>
#include <ql/experimental/credit/recoveryratemodel.hpp>
#include <ql/experimental/credit/pool.hpp>
#include <ql/experimental/credit/loss.hpp>

namespace QuantLib {

    class DefaultLossModel;

    /*! Credit Basket.\par
        A basket is a collection of credit names, represented by a
        unique identifier (a text string), associated notional
        amounts, a pool and tranche information. The pool is a map of
        "names" to issuers.  The Basket structure is motivated by CDO
        squared instruments containing various underlying inner CDOs
        which can be represented by respective baskets including their
        tranche structure.  The role of the Pool is providing a unique
        list of relevant issuers while names may appear multiple times
        across different baskets (overlap).
     */
    class Basket : public LazyObject {
      public:
        Basket() = default;
        /*! Constructs a basket of simple collection of constant notional 
          positions subject to default risk only.
          
          The refDate parameter is the basket inception date, that is,
          the date at which defaultable events are relevant. (There
          are no constraints on forward baskets but models assigned
          should be consistent.)
        */
        Basket(const Date& refDate,
               const std::vector<std::string>& names,
               std::vector<Real> notionals,
               ext::shared_ptr<Pool> pool,
               Real attachmentRatio = 0.0,
               Real detachmentRatio = 1.0,
               ext::shared_ptr<Claim> claim = ext::shared_ptr<Claim>(new FaceValueClaim()));
        void update() override {
            computeBasket();
            LazyObject::update();
        }
        void computeBasket() const {
            Date today = Settings::instance().evaluationDate();
            /* update cache values at the calculation date (work as arguments 
              to the Loss Models)
            \to do: IMPORTANT: notice that defaults added to Issuers dont get
            notify as the codes stnds today. Issuers need to be observables.
            */
            //this one must remain on top since there are dependencies
            evalDateLiveKeys_      = remainingDefaultKeys(today);
            evalDateSettledLoss_   = settledLoss(today);
            evalDateRemainingNot_  = remainingNotional(today);
            evalDateLiveNotionals_ = remainingNotionals(today);
            evalDateLiveNames_     = remainingNames(today);
            evalDateAttachAmount_  = remainingAttachmentAmount(today);
            evalDateDetachAmmount_ = 
                remainingDetachmentAmount(today);
            evalDateLiveList_ = liveList(today);
        }
        //! Basket inception number of counterpar