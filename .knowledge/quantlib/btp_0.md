/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2010, 2011 Ferdinando Ametrano

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

/*! \file btp.hpp
    \brief Italian BTP (Buoni Poliennali del Tesoro) fixed rate bond
*/

#ifndef quantlib_btp_hpp
#define quantlib_btp_hpp

#include <ql/instruments/bonds/fixedratebond.hpp>
#include <ql/instruments/bonds/floatingratebond.hpp>
#include <ql/indexes/ibor/euribor.hpp>
#include <ql/instruments/vanillaswap.hpp>

#include <numeric>

namespace QuantLib {

    /*! Italian CCTEU (Certificato di credito del tesoro)
        Euribor6M indexed floating rate bond

        \ingroup instruments

    */
    class CCTEU : public FloatingRateBond {
      public:
        CCTEU(const Date& maturityDate,
              Spread spread,
              const Handle<YieldTermStructure>& fwdCurve =
                                    Handle<YieldTermStructure>(),
              const Date& startDate = Date(),
              const Date& issueDate = Date());
        //! \name Bond interface
        //@{
        //! accrued amount at a given date
        /*! The default bond settlement is used if no date is given. */
        Real accruedAmount(Date d = Date()) const override;
        //@}
    };

    //! Italian BTP (Buono Poliennali del Tesoro) fixed rate bond
    /*! \ingroup instruments

    */
    class BTP : public FixedRateBond {
      public:
        BTP(const Date& maturityDate,
            Rate fixedRate,
            const Date& startDate = Date(),
            const Date& issueDate = Date());
        /*! constructor needed for legacy non-par redemption BTPs.
            As of today the only remaining one is IT123456789012
            that will redeem 99.999 on xx-may-2037 */
        BTP(const Date& maturityDate,
            Rate fixedRate,
            Real redemption,
            const Date& startDate = Date(),
            const Date& issueDate = Date());
        //! \name Bond interface
        //@{
        //! accrued amount at a given date
        /*! The default bond settlement is used if no date is given. */
        Real accruedAmount(Date d = Date()) const override;
        //@}
        //! BTP yield given a (clean) price and settlement date
        /*! The default BTP conventions are used: Actual/Actual (ISMA),
            Compounded, Annual.
            The default bond settlement is used if no date is given. */
        Rate yield(Real cleanPrice,
                   Date settlementDate = Date(),
                   Real accuracy = 1.0e-8,
                   Size maxEvaluations = 100) const;
    };

    class RendistatoBasket : public Observer,
                             public Observable {
      public:
        RendistatoBasket(const std::vector<ext::shared_ptr<BTP> >& btps,
                         const std::vector<Real>& outstandings,
                         std::vector<Handle<Quote> > cleanPriceQuotes);
        //! \name Inspectors
        //@{
        Size size() const { return n_;}
        const std::vector<ext::shared_ptr<BTP> >& btps() const;
        const std::vector<Handle<Quote> >& cleanPriceQuotes() const;
        const std::vector<Real>& outstandings() const { return outstandings_;}
        const std::vector<Real>& weights() const { return weights_;}
        Real outstanding() const { return outstanding_;}
