/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
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

#ifndef quantlib_recursive_loss_model_hpp
#define quantlib_recursive_loss_model_hpp

#include <ql/experimental/credit/constantlosslatentmodel.hpp>
#include <ql/experimental/credit/defaultlossmodel.hpp>
#include <map>
#include <algorithm>

namespace QuantLib {

    /*! Recursive STCDO default loss model for a heterogeneous pool of names.
    The pool names are heterogeneous in their default probabilities, notionals
    and recovery rates. Correlations are given by the latent model.
    The recursive pricing algorithm used here is described in Andersen, Sidenius
    and Basu; "All your hedges in one basket", Risk, November 2003, pages 67-72

        Notice that using copulas other than Gaussian it is only an
        approximation (see remark on p.68).

        \todo Make the loss unit equal to some small fraction depending on the
        portfolio loss weights (notionals and recoveries). As it is now this
        is ok for pricing but not for risk metrics. See the discussion in O'Kane
        18.3.2
        \todo Intengrands should all use the inverted probabilities for
        performance instead of calling the copula inversion with the same vals.
    */
    template<class copulaPolicy>
    class RecursiveLossModel : public DefaultLossModel {
    public:
      explicit RecursiveLossModel(
          const ext::shared_ptr<ConstantLossLatentmodel<copulaPolicy> >& m,
          // nope! use max common divisor. See O'Kane. Or give both options at least.
          Size nbuckets = 1)
      : copula_(m), nBuckets_(nbuckets) {}

    private:
      /*!
      @param pDefDate Vector of unconditional default probabilities for each
      live name (at the current evaluation date). This is passed instead of
      the date for performance reasons (if in the future other magnitudes
      -e.g. lgd- are contingent on the date they shouldd be passed too).
      */
      std::map<Real, Probability> conditionalLossDistrib(const std::vector<Probability>& pDefDate,
                                                         const std::vector<Real>& mktFactor) const;
      Real expectedConditionalLoss(const std::vector<Probability>& pDefDate, //<< never used!!
                                   const std::vector<Real>& mktFactor) const;
      std::vector<Real> conditionalLossProb(const std::vector<Probability>& pDefDate,
                                            // const Date& date,
                                            const std::vector<Real>& mktFactor) const;
      // versions using the P-inverse, deprecate the former
      std::map<Real, Probability> conditionalLossDistribInvP(const std::vector<Real>& pDefDate,
                                                             // const Date& date,
                                                             const std::vector<Real>& mktFactor) const;
      Real expectedConditionalLossInvP(const std::vector<Real>& pDefDate,
                                       // const Date& date,
                                       const std::vector<Real>& mktFactor) const;
    protected:
      void resetModel() override;

    public:
        /*  Expected tranche Loss calculation.
            This is computed from
