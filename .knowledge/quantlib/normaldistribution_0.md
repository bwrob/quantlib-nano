/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2002, 2003 Ferdinando Ametrano
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2010 Kakhkhor Abdijalilov

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

/*! \file normaldistribution.hpp
    \brief normal, cumulative and inverse cumulative distributions
*/

#ifndef quantlib_normal_distribution_hpp
#define quantlib_normal_distribution_hpp

#include <ql/math/errorfunction.hpp>
#include <ql/errors.hpp>

namespace QuantLib {

    //! Normal distribution function
    /*! Given x, it returns its probability in a Gaussian normal distribution.
        It provides the first derivative too.

        \test the correctness of the returned value is tested by
              checking it against numerical calculations. Cross-checks
              are also performed against the
              CumulativeNormalDistribution and InverseCumulativeNormal
              classes.
    */
    class NormalDistribution {
      public:
        NormalDistribution(Real average = 0.0,
                           Real sigma = 1.0);
        // function
        Real operator()(Real x) const;
        Real derivative(Real x) const;
      private:
        Real average_, sigma_, normalizationFactor_, denominator_,
            derNormalizationFactor_;
    };

    typedef NormalDistribution GaussianDistribution;


    //! Cumulative normal distribution function
    /*! Given x it provides an approximation to the
        integral of the gaussian normal distribution:
        formula here ...

        For this implementation see M. Abramowitz and I. Stegun,
        Handbook of Mathematical Functions,
        Dover Publications, New York (1972)
    */
    class CumulativeNormalDistribution {
      public:
        CumulativeNormalDistribution(Real average = 0.0,
                                     Real sigma   = 1.0);
        // function
        Real operator()(Real x) const;
        Real derivative(Real x) const;
      private:
        Real average_, sigma_;
        NormalDistribution gaussian_;
        ErrorFunction errorFunction_;
    };


    //! Inverse cumulative normal distribution function
    /*! Given x between zero and one as
      the integral value of a gaussian normal distribution
      this class provides the value y such that
      formula here ...

      It use Acklam's approximation:
      by Peter J. Acklam, University of Oslo, Statistics Division.
      URL: http://home.online.no/~pjacklam/notes/invnorm/index.html

      This class can also be used to generate a gaussian normal
      distribution from a uniform distribution.
      This is especially useful when a gaussian normal distribution
      is generated from a low discrepancy uniform distribution:
      in this case the traditional Box-Muller approach and its
      variants would not preserve the sequence's low-discrepancy.

    */
    class InverseCumulativeNormal {
      public:
        InverseCumulativeNormal(Real average = 0.0,
                                Real sigma   = 1.0);
        // function
        Real operator()(Real x) const {
            return average_ + sigma_*standard_value(x);
        }
        // value for average=0, sigma=1
        /* Compared to operator(), this method avoids 2 floating point
           operations (we use average=0 and s