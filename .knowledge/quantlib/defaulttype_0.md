/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2009 StatPro Italia srl
 Copyright (C) 2009 Jose Aparicio

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

/*! \file defaulttype.hpp
    \brief Classes for default-event description.
*/


#ifndef quantlib_default_type_hpp
#define quantlib_default_type_hpp

#include <ql/time/period.hpp>

namespace QuantLib {

    //! Seniority of a bond.
    /*! They are also ISDA tier/seniorities used for CDS conventional
        spreads.
    */
    enum Seniority {
        SecDom = 0,
        SnrFor,
        SubLT2,
        JrSubT2,
        PrefT1,
        // Unassigned value, allows for default RR quote
        NoSeniority,
        // markit parlance
        SeniorSec     = SecDom,
        SeniorUnSec   = SnrFor,
        SubTier1      = PrefT1,
        SubUpperTier2 = JrSubT2,
        SubLoweTier2  = SubLT2
    };


    //! Atomic (single contractual event) default events.
    /*! Default types defined as enum to allow easy aggregation of
        types. Theres an event algebra logic by default provided by
        DefaultType. If your new type requires more sofisticated test
        you need to derive from it as in FailureToPay
    */
    struct AtomicDefault {
        enum Type {
            // Includes one of the restructuring cases
            Restructuring = 0,
            Bankruptcy,
            FailureToPay,
            RepudiationMoratorium,
            Acceleration,
            Default,
            // synonyms
            ObligationAcceleration = Acceleration,
            ObligationDefault = Default,
            CrossDefault = Default,
            // Other non-isda
            Downgrade,   // Non-ISDA, not in FpML
            MergerEvent  // Non-ISDA, not in FpML
        };
    };


    // these could be merged with the ones above if not because
    //   restructuring types can not be combined together.

    //! Restructuring type
    struct Restructuring {
        enum Type {
            NoRestructuring = 0,
            ModifiedRestructuring,
            ModifiedModifiedRestructuring,
            FullRestructuring,
            AnyRestructuring,
            // Markit notation:
            XR = NoRestructuring,
            MR = ModifiedRestructuring,
            MM = ModifiedModifiedRestructuring,
            CR = FullRestructuring
        };
    };


    //! Atomic credit-event type.
    /*! This class encapsulates the ISDA default contractual types and
        their combinations. Non-atomicity works only at the atomic
        type level, obviating the specific event characteristics which
        it is accounted for only in derived classes.
    */
    class DefaultType {
      public:
        explicit DefaultType(AtomicDefault::Type defType =
                                                    AtomicDefault::Bankruptcy,
                             Restructuring::Type restType = Restructuring::XR);

        virtual ~DefaultType() = default;

        AtomicDefault::Type defaultType() const {
            return defTypes_;
        }
        Restructuring::Type restructuringType() const {return restrType_;}
        bool isRestructuring() const {
            return restrType_ != Restructuring::NoRestructuring;
        }

        // bool isAtomic() const { return defTypes_.size() == 1;}

        /*! Returns true if on