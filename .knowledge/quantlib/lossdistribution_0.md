/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2008 Roland Lichters

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

/*! \file lossdistribution.hpp
    \brief Loss distributions and probability of n defaults
*/

#ifndef quantlib_loss_distribution_hpp
#define quantlib_loss_distribution_hpp

#include <ql/math/distributions/binomialdistribution.hpp>
#include <ql/experimental/credit/distribution.hpp>
#include <ql/experimental/credit/onefactorcopula.hpp>

namespace QuantLib {

    //! Probability formulas and algorithms
    class LossDist {
    public:
      LossDist() = default;
      virtual ~LossDist() = default;

      virtual Distribution operator()(const std::vector<Real>& volumes,
                                      const std::vector<Real>& probabilities) const = 0;
      virtual Size buckets() const = 0;
      virtual Real maximum() const = 0;

      /*! Binomial probability of n defaults using prob[0]
       */
      static Real binomialProbabilityOfNEvents(int n, std::vector<Real>& p);

      /*! Binomial probability of at least n defaults using prob[0]
       */
      static Real binomialProbabilityOfAtLeastNEvents(int n, std::vector<Real>& p);
      /*! Probability of exactly n default events
        Xiaofong Ma, "Numerical Methods for the Valuation of Synthetic
        Collateralized Debt Obligations", PhD Thesis,
        Graduate Department of Computer Science, University of Toronto, 2007
        http://www.cs.toronto.edu/pub/reports/na/ma-07-phd.pdf (formula 2.1)
      */
      static std::vector<Real> probabilityOfNEvents(std::vector<Real>& p);

      static Real probabilityOfNEvents(int n, std::vector<Real>& p);

      /*! Probability of at least n defaults
       */
      static Real probabilityOfAtLeastNEvents(int n, std::vector<Real>& p);
    };

    //! Probability of N events
    class ProbabilityOfNEvents {
    public:
        explicit ProbabilityOfNEvents (int n) : n_(n) {}
        Real operator()(std::vector<Real> p) const;
    private:
        Size n_;
    };

    //! Probability of at least N events
    class ProbabilityOfAtLeastNEvents {
    public:
        explicit ProbabilityOfAtLeastNEvents (int n) : n_(n) {}
        Real operator()(std::vector<Real> p) const;
    private:
        Size n_;
    };

    //! Probability of at least N events
    class BinomialProbabilityOfAtLeastNEvents {
    public:
        explicit BinomialProbabilityOfAtLeastNEvents(int n) : n_(n) {}
        Real operator()(std::vector<Real> p) const;

      private:
        int n_;
    };

    //! Binomial loss distribution
    class LossDistBinomial : public LossDist {
    public:
        LossDistBinomial (Size nBuckets, Real maximum)
            : nBuckets_(nBuckets), maximum_(maximum) {}
        Distribution operator()(Size n, Real volume, Real probability) const;
        Distribution operator()(const std::vector<Real>& volumes,
                                const std::vector<Real>& probabilities) const override;
        Size buckets() const override { return nBuckets_; }
        Real maximum() const override { return maximum_; }
        Real volume() const { return volume_; }
        Size size () const { return n_; }
        std::vector<Real> probability() const { return probability_; }
        std::vector<Real> excessProbability() const { return
