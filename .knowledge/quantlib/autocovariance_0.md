/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2010 Liquidnet Holdings, Inc.

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

/*! \file autocovariance.hpp
    \brief autocovariance and convolution calculation
*/

#ifndef quantlib_auto_covariance_hpp
#define quantlib_auto_covariance_hpp

#include <ql/math/fastfouriertransform.hpp>
#include <ql/math/array.hpp>
#include <complex>
#include <vector>
#include <algorithm>
#include <functional>

namespace QuantLib {

    namespace detail {

        // Outputs double FT for a given input:
        // input -> FFT -> norm -> FFT -> out
        template <typename ForwardIterator>
        std::vector<std::complex<Real> > double_ft(ForwardIterator begin,
                                                   ForwardIterator end) {
            std::size_t nData = std::distance(begin, end);
            std::size_t order = FastFourierTransform::min_order(nData) + 1;
            FastFourierTransform fft(order);
            std::vector<std::complex<Real> > ft(fft.output_size());
            fft.transform(begin, end, ft.begin());
            Array tmp(ft.size(), 0.0);
            std::complex<Real> z = std::complex<Real>();
            for (Size i=0; i<ft.size(); ++i) {
                tmp[i] = std::norm(ft[i]);
                ft[i] = z;
            }
            fft.transform(tmp.begin(), tmp.end(), ft.begin());
            return ft;
        }


        // Calculates and subtracts mean from the input data; returns mean
        template <typename InputIterator, typename OutputIterator>
        Real remove_mean(InputIterator begin, InputIterator end,
                         OutputIterator out) {
            Real mean(0.0);
            std::size_t n = 1;
            for (InputIterator it = begin; it != end; ++it, ++n)
                mean = (mean*Real(n-1) + *it)/n;
            std::transform(begin, end, out, [=](Real x) -> Real { return x - mean; });
            return mean;
        }

    }


    //! Convolutions of the input sequence.
    /*! Calculates x[0]*x[n]+x[1]*x[n+1]+x[2]*x[n+2]+...
        for n = 0,1,...,maxLag via FFT.

        \pre The size of the output sequence must be maxLag + 1
    */
    template <typename ForwardIterator, typename OutputIterator>
    void convolutions(ForwardIterator begin, ForwardIterator end,
                      OutputIterator out, std::size_t maxLag) {
        using namespace detail;
        std::size_t nData = std::distance(begin, end);
        QL_REQUIRE(maxLag < nData, "maxLag must be less than data size");
        const std::vector<std::complex<Real> >& ft = double_ft(begin, end);
        Real w = 1.0 / (Real)ft.size();
        for (std::size_t k = 0; k <= maxLag; ++k)
            *out++ = ft[k].real() * w;
    }

    //! Unbiased auto-covariances
    /*! Results are calculated via FFT.

        \pre Input data are supposed to be centered (i.e., zero mean).
        \pre The size of the output sequence must be maxLag + 1
    */
    template <typename ForwardIterator, typename OutputIterator>
    void autocovariances(ForwardIterator begin, ForwardIterator end,
                         OutputIterator out, std::size_t maxLag) {
        using namespace detail;
        std::size_t nData = std::distance(begin, end);
        QL_REQUIRE(maxLag < nData,
                   "number of cov