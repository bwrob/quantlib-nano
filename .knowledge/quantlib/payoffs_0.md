/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003, 2006 Ferdinando Ametrano
 Copyright (C) 2006 Warren Chou
 Copyright (C) 2006, 2008 StatPro Italia srl
 Copyright (C) 2006 Chiara Fornarola

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

/*! \file payoffs.hpp
    \brief Payoffs for various options
*/

#ifndef quantlib_payoffs_hpp
#define quantlib_payoffs_hpp

#include <ql/option.hpp>
#include <ql/payoff.hpp>

namespace QuantLib {

    //! Dummy %payoff class
    class NullPayoff : public Payoff {
      public:
        //! \name Payoff interface
        //@{
        std::string name() const override;
        std::string description() const override;
        Real operator()(Real price) const override;
        void accept(AcyclicVisitor&) override;
        //@}
    };


    //! Intermediate class for put/call payoffs
    class TypePayoff : public Payoff {
      public:
        Option::Type optionType() const { return type_; };
        //! \name Payoff interface
        //@{
        std::string description() const override;
        //@}
      protected:
        explicit TypePayoff(Option::Type type) : type_(type) {}
        Option::Type type_;
    };

    ////! Intermediate class for payoffs based on a fixed strike
    //class StrikedPayoff : public Payoff {
    //  public:
    //    StrikedPayoff(Real strike) : strike_(strike) {}
    //    Real strike() const { return strike_; };
    //    //! \name Payoff interface
    //    //@{
    //    std::string description() const;
    //    //@}
    //  protected:
    //    Real strike_;
    //};

    //! %Payoff based on a floating strike
    class FloatingTypePayoff : public TypePayoff {
      public:
        FloatingTypePayoff(Option::Type type) : TypePayoff(type) {}
        //! \name Payoff interface
        //@{
        std::string name() const override { return "FloatingType"; }
        Real operator()(Real price, Real strike) const;
        Real operator()(Real price) const override;
        void accept(AcyclicVisitor&) override;
        //@}
    };

    //! Intermediate class for payoffs based on a fixed strike
    class StrikedTypePayoff : public TypePayoff
                              //, public StrikedPayoff
    {
      public:
        //! \name Payoff interface
        //@{
        std::string description() const override;
        //@}
        Real strike() const { return strike_; };
      protected:
        StrikedTypePayoff(Option::Type type,
                          Real strike)
        : TypePayoff(type), strike_(strike) {}
        Real strike_;
    };

    //! Plain-vanilla payoff
    class PlainVanillaPayoff : public StrikedTypePayoff {
      public:
        PlainVanillaPayoff(Option::Type type,
                           Real strike)
        : StrikedTypePayoff(type, strike) {}
        //! \name Payoff interface
        //@{
        std::string name() const override { return "Vanilla"; }
        Real operator()(Real price) const override;
        void accept(AcyclicVisitor&) override;
        //@}
    };

    //! %Payoff with strike expressed as percentage
    class PercentageStrikePayoff : public StrikedTypePayoff {
      public:
        PercentageStrikePayoff(Option::Type type,
                               Real moneyness)
        : StrikedTypePayoff(type, moneyness) {}
        //! \n