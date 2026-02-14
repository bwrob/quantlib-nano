/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2004 Decillion Pty(Ltd)
 Copyright (C) 2004, 2005, 2006, 2007 StatPro Italia srl

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

/*! \file currency.hpp
    \brief Currency specification
*/

#ifndef quantlib_currency_hpp
#define quantlib_currency_hpp

#include <ql/math/rounding.hpp>
#include <ql/errors.hpp>
#include <iosfwd>
#include <set>

namespace QuantLib {

    //! %Currency specification
    class Currency {
      public:
        //! \name Constructors
        //@{
        //! default constructor
        /*! Instances built via this constructor have undefined
            behavior. Such instances can only act as placeholders
            and must be reassigned to a valid currency before being
            used.
        */
        Currency() = default;
        Currency(const std::string& name,
                 const std::string& code,
                 Integer numericCode,
                 const std::string& symbol,
                 const std::string& fractionSymbol,
                 Integer fractionsPerUnit,
                 const Rounding& rounding,
                 const Currency& triangulationCurrency = Currency(),
                 const std::set<std::string>& minorUnitCodes = {});
        //@}
        //! \name Inspectors
        //@{
        //! currency name, e.g, "U.S. Dollar"
        const std::string& name() const;
        //! ISO 4217 three-letter code, e.g, "USD"
        const std::string& code() const;
        //! ISO 4217 numeric code, e.g, "840"
        Integer numericCode() const;
        //! symbol, e.g, "$"
        const std::string& symbol() const;
        //! fraction symbol, e.g, "¢"
        const std::string& fractionSymbol() const;
        //! number of fractionary parts in a unit, e.g, 100
        Integer fractionsPerUnit() const;
        //! rounding convention
        const Rounding& rounding() const;
        //@}
        //! \name Other information
        //@{
        //! is this a usable instance?
        bool empty() const;
        //! currency used for triangulated exchange when required
        const Currency& triangulationCurrency() const;
        //! minor unit codes, e.g. GBp, GBX for GBP
        const std::set<std::string>& minorUnitCodes() const;
        //@}
      protected:
        struct Data;
        ext::shared_ptr<Data> data_;
     private:
        void checkNonEmpty() const;
    };

    struct Currency::Data {
        std::string name, code;
        Integer numeric;
        std::string symbol, fractionSymbol;
        Integer fractionsPerUnit;
        Rounding rounding;
        Currency triangulated;
        std::set<std::string> minorUnitCodes;

        Data(std::string name,
             std::string code,
             Integer numericCode,
             std::string symbol,
             std::string fractionSymbol,
             Integer fractionsPerUnit,
             const Rounding& rounding,
             Currency triangulationCurrency = Currency(),
             std::set<std::string> minorUnitCodes = {});
    };


    /*! \relates Currency */
    bool operator==(const Currency&,
                    const Currency&);

    /*! \relates Currency */
    bool operator!=(const Currency&,
                    const Currency&);

    /*! \relates Currency */
    std::ostrea