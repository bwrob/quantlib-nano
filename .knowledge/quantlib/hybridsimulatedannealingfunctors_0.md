/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
Copyright (C) 2015 Andres Hernandez

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

/*! \file hybridsimulatedannealingfunctors.hpp
\brief Functors for use on HybridSimulatedAnnealing
*/

#ifndef HYBRIDSIMULATEDANNEALINGFUNCTORS_H
#define HYBRIDSIMULATEDANNEALINGFUNCTORS_H

#include <ql/math/array.hpp>
#include <ql/math/randomnumbers/seedgenerator.hpp>
#include <ql/math/optimization/problem.hpp>

#include <algorithm>
#include <cmath>
#include <random>
#include <utility>
#include <vector>

namespace QuantLib
{
    //! Lognormal Sampler
    /*!    Sample from lognormal distribution. This means that the parameter space
    must have support on the positve side of the real line only.
    */
    class SamplerLogNormal
    {
    public:
        explicit SamplerLogNormal(unsigned long seed = SeedGenerator::instance().get()) :
            generator_(seed), distribution_(0.0, 1.0) {};

        void operator()(Array &newPoint, const Array &currentPoint, const Array &temp) {
            QL_REQUIRE(newPoint.size() == currentPoint.size(), "Incompatible input");
            QL_REQUIRE(newPoint.size() == temp.size(), "Incompatible input");
            for (Size i = 0; i < currentPoint.size(); i++)
                newPoint[i] = currentPoint[i] * exp(sqrt(temp[i]) * distribution_(generator_));
        };
    private:
        std::mt19937 generator_;
        std::normal_distribution<Real> distribution_;
    };

    //! Gaussian Sampler
    /*!    Sample from normal distribution. This means that the parameter space
    must have support on the whole real line.
    */
    class SamplerGaussian
    {
    public:
        explicit SamplerGaussian(unsigned long seed = SeedGenerator::instance().get()) :
            generator_(seed), distribution_(0.0, 1.0) {};

        void operator()(Array &newPoint, const Array &currentPoint, const Array &temp) {
            QL_REQUIRE(newPoint.size() == currentPoint.size(), "Incompatible input");
            QL_REQUIRE(newPoint.size() == temp.size(), "Incompatible input");
            for (Size i = 0; i < currentPoint.size(); i++)
                newPoint[i] = currentPoint[i] + std::sqrt(temp[i]) * distribution_(generator_);
        };
    private:
        std::mt19937 generator_;
        std::normal_distribution<Real> distribution_;
    };
    
    //! Gaussian Ring Sampler
    /*! Sample from normal distribution, but constrained to lie within
     * .boundaries. If the value ends up beyond the boundary, the value
     * is circled back from the other side.
    */
    class SamplerRingGaussian
    {
    public:
      SamplerRingGaussian(Array lower,
                          Array upper,
                          unsigned long seed = SeedGenerator::instance().get())
      : generator_(seed), distribution_(0.0, 1.0),
        lower_(std::move(lower)), upper_(std::move(upper)){};

        void operator()(Array &newPoint, const Array &currentPoint, const Array &temp) {
            QL_REQUIRE(newPoint.size() == currentPoint.size(), "Incompatible input");
            QL_REQUIRE(newPoint.size() == temp.size(), "Incompatible input");
            for (Size i = 0; i < currentPoint.size(); i++){
                newPoint[i] = currentPoint[i] + std::sqrt(temp[i]) * distribution_(generator_);
                while(newPoint[i] < l