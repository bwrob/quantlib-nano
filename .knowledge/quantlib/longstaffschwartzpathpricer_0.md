/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2006 Klaus Spanderen
 Copyright (C) 2015 Peter Caspers
 Copyright (C) 2015 Thema Consulting SA

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

/*! \file longstaffschwartzpathpricer.hpp
    \brief Longstaff-Schwarz path pricer for early exercise options
*/

#ifndef quantlib_longstaff_schwartz_path_pricer_hpp
#define quantlib_longstaff_schwartz_path_pricer_hpp

#include <ql/math/generallinearleastsquares.hpp>
#include <ql/math/statistics/incrementalstatistics.hpp>
#include <ql/methods/montecarlo/earlyexercisepathpricer.hpp>
#include <ql/methods/montecarlo/pathpricer.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <functional>
#include <utility>
#include <memory>

namespace QuantLib {

    //! Longstaff-Schwarz path pricer for early exercise options
    /*! References:

        Francis Longstaff, Eduardo Schwartz, 2001. Valuing American Options
        by Simulation: A Simple Least-Squares Approach, The Review of
        Financial Studies, Volume 14, No. 1, 113-147

        \ingroup mcarlo

        \test the correctness of the returned value is tested by
              reproducing results available in web/literature
    */
    template <class PathType>
    class LongstaffSchwartzPathPricer : public PathPricer<PathType> {
      public:
        typedef typename EarlyExerciseTraits<PathType>::StateType StateType;

        LongstaffSchwartzPathPricer(const TimeGrid& times,
                                    ext::shared_ptr<EarlyExercisePathPricer<PathType> >,
                                    const ext::shared_ptr<YieldTermStructure>& termStructure);

        Real operator()(const PathType& path) const override;
        virtual void calibrate();

        Real exerciseProbability() const;

      protected:
        virtual void post_processing(const Size i,
                                     const std::vector<StateType> &state,
                                     const std::vector<Real> &price,
                                     const std::vector<Real> &exercise) {}
        bool calibrationPhase_ = true;
        const ext::shared_ptr<EarlyExercisePathPricer<PathType> >
            pathPricer_;

        mutable QuantLib::IncrementalStatistics exerciseProbability_;

        std::unique_ptr<Array[]> coeff_;
        std::unique_ptr<DiscountFactor[]> dF_;

        mutable std::vector<PathType> paths_;
        const   std::vector<std::function<Real(StateType)> > v_;

        const Size len_;
    };

    template <class PathType>
    inline LongstaffSchwartzPathPricer<PathType>::LongstaffSchwartzPathPricer(
        const TimeGrid& times,
        ext::shared_ptr<EarlyExercisePathPricer<PathType> > pathPricer,
        const ext::shared_ptr<YieldTermStructure>& termStructure)
    : pathPricer_(std::move(pathPricer)), coeff_(new Array[times.size() - 2]),
      dF_(new DiscountFactor[times.size() - 1]), v_(pathPricer_->basisSystem()),
      len_(times.size()) {

        for (Size i=0; i<times.size()-1; ++i) {
            dF_[i] =   termStructure->discount(times[i+1])
                     / termStructure->discount(times[i]);
        }
    }

    template <class PathType> inline
    Real LongstaffSchwartzPathPricer<PathType>::operator()
        (const PathType& path) const {
        if (calibrationPha
