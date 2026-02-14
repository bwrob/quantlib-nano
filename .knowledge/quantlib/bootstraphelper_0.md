/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2005, 2006, 2007, 2008 StatPro Italia srl
 Copyright (C) 2007, 2009, 2015 Ferdinando Ametrano
 Copyright (C) 2015 Paolo Mazzocchi

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

/*! \file bootstraphelper.hpp
    \brief base helper class used for bootstrapping
*/

#ifndef quantlib_bootstrap_helper_hpp
#define quantlib_bootstrap_helper_hpp

#include <ql/handle.hpp>
#include <ql/patterns/observable.hpp>
#include <ql/patterns/visitor.hpp>
#include <ql/quote.hpp>
#include <ql/quotes/simplequote.hpp>
#include <ql/settings.hpp>
#include <ql/time/date.hpp>
#include <utility>

namespace QuantLib {

    struct Pillar {
        //! Alternatives ways of determining the pillar date
        enum Choice {
            MaturityDate,     //! instruments maturity date
            LastRelevantDate, //! last date relevant for instrument pricing
            CustomDate        //! custom choice
        };
    };

    std::ostream& operator<<(std::ostream& out, Pillar::Choice type);

    //! Base helper class for bootstrapping
    /*! This class provides an abstraction for the instruments used to
        bootstrap a term structure.

        It is advised that a bootstrap helper for an instrument
        contains an instance of the actual instrument class to ensure
        consistancy between the algorithms used during bootstrapping
        and later instrument pricing. This is not yet fully enforced
        in the available bootstrap helpers.
    */
    template <class TS>
    class BootstrapHelper : public Observer, public Observable {
      public:
        explicit BootstrapHelper(const std::variant<Spread, Handle<Quote>>& quote);
        ~BootstrapHelper() override = default;
        //! \name BootstrapHelper interface
        //@{
        const Handle<Quote>& quote() const { return quote_; }
        virtual Real impliedQuote() const = 0;
        Real quoteError() const { return quote_->value() - impliedQuote(); }
        //! sets the term structure to be used for pricing
        /*! \warning Being a pointer and not a shared_ptr, the term
                     structure is not guaranteed to remain allocated
                     for the whole life of the rate helper. It is
                     responsibility of the programmer to ensure that
                     the pointer remains valid. It is advised that
                     this method is called only inside the term
                     structure being bootstrapped, setting the pointer
                     to <b>this</b>, i.e., the term structure itself.
        */
        virtual void setTermStructure(TS*);

        //! earliest relevant date
        /*! The earliest date at which data are needed by the
            helper in order to provide a quote.
        */
        virtual Date earliestDate() const;

        //! instrument's maturity date
        virtual Date maturityDate() const;

        //! latest relevant date
        /*! The latest date at which data are needed by the helper
            in order to provide a quote. It does not necessarily
            equal the maturity of the underlying instrument.
        */
        virtual Date latestRelevantDate() const;

        //! pillar date
        virtual Date pillarDate() const;

        //! latest date
        /*! equal
