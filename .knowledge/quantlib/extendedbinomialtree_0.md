/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2001, 2002, 2003 Sadruddin Rejeb
 Copyright (C) 2003 Ferdinando Ametrano
 Copyright (C) 2005 StatPro Italia srl
 Copyright (C) 2008 John Maiden

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

/*! \file extendedbinomialtree.hpp
    \brief Time-dependent binomial tree class
*/

#ifndef quantlib_extended_binomial_tree_hpp
#define quantlib_extended_binomial_tree_hpp

#include <ql/methods/lattices/tree.hpp>
#include <ql/instruments/dividendschedule.hpp>
#include <ql/stochasticprocess.hpp>

namespace QuantLib {

    //! Binomial tree base class
    /*! \ingroup lattices */
    template <class T>
    class ExtendedBinomialTree : public Tree<T> {
      public:
        enum Branches { branches = 2 };
        ExtendedBinomialTree(
                        const ext::shared_ptr<StochasticProcess1D>& process,
                        Time end,
                        Size steps)
        : Tree<T>(steps+1), x0_(process->x0()), dt_(end/steps),
          treeProcess_(process) {}
        Size size(Size i) const {
            return i+1;
        }
        Size descendant(Size, Size index, Size branch) const {
            return index + branch;
        }
      protected:
        //time dependent drift per step
        Real driftStep(Time driftTime) const {
            return this->treeProcess_->drift(driftTime, x0_) * dt_;
        }

        Real x0_;
        Time dt_;


        ext::shared_ptr<StochasticProcess1D> treeProcess_;
    };


    //! Base class for equal probabilities binomial tree
    /*! \ingroup lattices */
    template <class T>
    class ExtendedEqualProbabilitiesBinomialTree
        : public ExtendedBinomialTree<T> {
      public:
        ExtendedEqualProbabilitiesBinomialTree(
                        const ext::shared_ptr<StochasticProcess1D>& process,
                        Time end,
                        Size steps)
        : ExtendedBinomialTree<T>(process, end, steps) {}
        virtual ~ExtendedEqualProbabilitiesBinomialTree() = default;

        Real underlying(Size i, Size index) const {
            Time stepTime = i*this->dt_;
            BigInteger j = 2*BigInteger(index) - BigInteger(i);
            // exploiting the forward value tree centering
            return this->x0_*std::exp(i*this->driftStep(stepTime) + j*this->upStep(stepTime));
        }

        Real probability(Size, Size, Size) const { return 0.5; }
      protected:
        //the tree dependent up move term at time stepTime
        virtual Real upStep(Time stepTime) const = 0;
        Real up_;
    };


    //! Base class for equal jumps binomial tree
    /*! \ingroup lattices */
    template <class T>
    class ExtendedEqualJumpsBinomialTree : public ExtendedBinomialTree<T> {
      public:
        ExtendedEqualJumpsBinomialTree(
                        const ext::shared_ptr<StochasticProcess1D>& process,
                        Time end,
                        Size steps)
        : ExtendedBinomialTree<T>(process, end, steps) {}
        virtual ~ExtendedEqualJumpsBinomialTree() = default;

        Real underlying(Size i, Size index) const {
            Time stepTime = i*this->dt_;
            BigInteger j = 2*BigInteger(index) - BigInteger(i);
            // exploiting equal jump and the x0_ tree centering
            return
