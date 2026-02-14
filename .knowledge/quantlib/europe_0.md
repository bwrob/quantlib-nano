/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2004, 2005, 2006 StatPro Italia srl
 Copyright (C) 2016 Quaternion Risk Management Ltd

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

/*! \file europe.hpp
    \brief European currencies

    Data from http://fx.sauder.ubc.ca/currency_table.html
    and http://www.thefinancials.com/vortex/CurrencyFormats.html
*/

#ifndef quantlib_european_currencies_hpp
#define quantlib_european_currencies_hpp

#include <ql/currency.hpp>

#if defined(QL_PATCH_MSVC)
#pragma warning(push)
#pragma warning(disable:4819)
#endif

namespace QuantLib {

    //! Bulgarian lev
    /*! The ISO three-letter code is BGL; the numeric code is 100.
        It is divided in 100 stotinki.

        \ingroup currencies
    */
    class BGLCurrency : public Currency {
      public:
        BGLCurrency();
    };

    //! Bulgarian lev
    /*! The ISO three-letter code is BGN; the numeric code is 975.
        It is divided into 100 stotinki.

        \ingroup currencies
    */
    class BGNCurrency : public Currency {
      public:
        BGNCurrency();
    };

    //! Belarussian ruble
    /*! The ISO three-letter code is BYR; the numeric code is 974.
        It has no subdivisions.

        \ingroup currencies
    */
    class BYRCurrency : public Currency {
      public:
        BYRCurrency();
    };

    //! Swiss franc
    /*! The ISO three-letter code is CHF; the numeric code is 756.
        It is divided into 100 cents.

        \ingroup currencies
    */
    class CHFCurrency : public Currency {
      public:
        CHFCurrency();
    };

    //! Czech koruna
    /*! The ISO three-letter code is CZK; the numeric code is 203.
        It is divided in 100 haleru.

        \ingroup currencies
    */
    class CZKCurrency : public Currency {
      public:
        CZKCurrency();
    };

    //! Danish krone
    /*! The ISO three-letter code is DKK; the numeric code is 208.
        It is divided in 100 øre.

        \ingroup currencies
    */
    class DKKCurrency : public Currency {
      public:
        DKKCurrency();
    };

    //! Estonian kroon
    /*! The ISO three-letter code is EEK; the numeric code is 233.
        It is divided in 100 senti.

        \ingroup currencies
    */
    class EEKCurrency : public Currency {
      public:
        EEKCurrency();
    };

    //! European Euro
    /*! The ISO three-letter code is EUR; the numeric code is 978.
        It is divided into 100 cents.

        \ingroup currencies
    */
    class EURCurrency : public Currency {
      public:
        EURCurrency();
    };

    //! British pound sterling
    /*! The ISO three-letter code is GBP; the numeric code is 826.
        It is divided into 100 pence.

        \ingroup currencies
    */
    class GBPCurrency : public Currency {
      public:
        GBPCurrency();
    };

    //! Georgian lari
    /*! The ISO three-letter code is GEL; the numeric code is 981.
        It is divided into 100 tetri.

        \ingroup currencies
    */
    class GELCurrency : public Currency {
      public:
        GELCurrency();
    };

    //! Hungarian forint
    /*! The ISO three-letter code is HUF; the numeric code is 348.
        It has no subdivisions.

        \ingroup currencies
    */
    class HUFCurrency : public Currency {
      public:
        HU
