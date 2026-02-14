/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003 Ferdinando Ametrano
 Copyright (C) 2006 StatPro Italia srl
 Copyright (C) 2009 Bojan Nikolic

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

/*! \file brownianbridge.hpp
    \brief Browian bridge
*/

// ===========================================================================
// NOTE: The following copyright notice applies to the original code,
//
// Copyright (C) 2002 Peter J�ckel "Monte Carlo Methods in Finance".
// All rights reserved.
//
// Permission to use, copy, modify, and distribute this software is freely
// granted, provided that this notice is preserved.
// ===========================================================================

#ifndef quantlib_brownian_bridge_hpp
#define quantlib_brownian_bridge_hpp

#include <ql/methods/montecarlo/path.hpp>
#include <ql/methods/montecarlo/sample.hpp>

namespace QuantLib {

    //! Builds Wiener process paths using Gaussian variates
    /*! This class generates normalized (i.e., unit-variance) paths as
        sequences of variations. In order to obtain the actual path of
        the underlying, the returned variations must be multiplied by
        the integrated variance (including time) over the
        corresponding time step.

        \ingroup mcarlo
    */
    class BrownianBridge {
      public:
        /*! The constructor generates the time grid so that each step
            is of unit-time length.

            \param steps The number of steps in the path
        */
        BrownianBridge(Size steps);
        /*! The step times are copied from the supplied vector

            \param times A vector containing the times at which the
                         steps occur. This also defines the number of
                         steps that will be generated.

            \note the starting time of the path is assumed to be 0 and
                  must not be included
        */
        BrownianBridge(const std::vector<Time>& times);
        /*! The step times are copied from the TimeGrid object

            \param timeGrid a time grid containing the times at which
                            the steps will occur
        */
        BrownianBridge(const TimeGrid& timeGrid);
        //! \name inspectors
        //@{
        Size size() const { return size_; }
        const std::vector<Time>& times() const { return t_; }
        const std::vector<Size>& bridgeIndex()  const { return bridgeIndex_; }
        const std::vector<Size>& leftIndex()    const { return leftIndex_; }
        const std::vector<Size>& rightIndex()   const { return rightIndex_; }
        const std::vector<Real>& leftWeight()   const { return leftWeight_; }
        const std::vector<Real>& rightWeight()  const { return rightWeight_; }
        const std::vector<Real>& stdDeviation() const { return stdDev_; }
        //@}

        //! Brownian-bridge generator function
        /*! Transforms an input sequence of random variates into a
            sequence of variations in a Brownian bridge path.

            \param begin  The start iterator of the input sequence.
            \param end    The end iterator of the input sequence.
            \param output The start iterator of the output sequence.

            \note To get the canonical Brownian bridge which starts

