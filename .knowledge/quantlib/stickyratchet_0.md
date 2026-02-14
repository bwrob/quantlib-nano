/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2007 Marco Bianchetti
 Copyright (C) 2007 Giorgio Facchinetti

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

/*! \file stickyratchet.hpp
    \brief Payoffs for double nested options of sticky or ratchet type
*/

#ifndef quantlib_stickyratchet_hpp
#define quantlib_stickyratchet_hpp

#include <ql/option.hpp>
#include <ql/payoff.hpp>

namespace QuantLib {
    
    class AcyclicVisitor;
    //! Intermediate class for single/double sticky/ratchet payoffs.
    //  initialValues can be a (forward) rate or a coupon/accrualFactor 
    class DoubleStickyRatchetPayoff : public Payoff {
      public:
        DoubleStickyRatchetPayoff(Real type1, Real type2,
                            Real gearing1, Real gearing2, Real gearing3,
                            Real spread1, Real spread2, Real spread3,
                            Real initialValue1, Real initialValue2, 
                            Real accrualFactor) 
        : type1_(type1), type2_(type2), 
          gearing1_(gearing1), gearing2_(gearing2), gearing3_(gearing3),
          spread1_(spread1), spread2_(spread2), spread3_(spread3),
          initialValue1_(initialValue1), initialValue2_(initialValue2), 
          accrualFactor_(accrualFactor) {}
        //! \name Payoff interface
        //@{
        std::string name() const override;
        Real operator()(Real forward) const override;
        std::string description() const override;
        void accept(AcyclicVisitor&) override;
        //@}
      protected:
        Real type1_ ,type2_;
        Real gearing1_, gearing2_, gearing3_;
        Real spread1_, spread2_, spread3_;
        Real initialValue1_, initialValue2_, accrualFactor_;
    };

    //! Ratchet payoff (single option)
    class RatchetPayoff : public DoubleStickyRatchetPayoff {
      public:
         RatchetPayoff(Real gearing1, Real gearing2,
                       Real spread1, Real spread2,
                       Real initialValue, Real accrualFactor)
        : DoubleStickyRatchetPayoff(-1.0, 0.0,
                            gearing1, 0.0, gearing2,
                            spread1, 0.0, spread2,
                            initialValue, 0.0, 
                            accrualFactor) {}
        //! \name Payoff interface
        //@{
         std::string name() const override { return "Ratchet"; }
         //@}
    };    

    //! Sticky payoff (single option)
    class StickyPayoff : public DoubleStickyRatchetPayoff {
      public:
         StickyPayoff(Real gearing1, Real gearing2,
                       Real spread1, Real spread2,
                       Real initialValue, Real accrualFactor)
        : DoubleStickyRatchetPayoff(+1.0, 0.0,
                            gearing1, 0.0, gearing2,
                            spread1, 0.0, spread2,
                            initialValue, 0.0, 
                            accrualFactor) {}
        //! \name Payoff interface
        //@{
         std::string name() const override { return "Sticky"; }
         //@}
    };

    //! RatchetMax payoff (double option)
    class RatchetMaxPayoff : public DoubleStickyRatchetPayoff {
      public:
         RatchetMaxPayoff(Real gearing1, Real gearing2, Real gearing3,
                          Real spread1, Real spread2, Real spread3,
           