/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2014 Jose Aparicio

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

#ifndef convolved_student_t_hpp
#define convolved_student_t_hpp

#include <ql/types.hpp>
#include <vector>
#include <numeric>
#include <functional>

namespace QuantLib {

    /*! \brief Cumulative (generalized) BehrensFisher distribution.

    Exact analitical computation of the cumulative probability distribution of
    the linear combination of an arbitrary number (not just two) of T random
    variables of odd integer order. Adapted from the algorithm in:\par
        V. Witkovsky, Journal of Statistical Planning and Inference 94
        (2001) 1-13\par
    see also:\par
        On the distribution of a linear combination of t-distributed
        variables; Glenn Alan Walker, Ph.D.thesis University of Florida 1977\par
        'Convolutions of the T Distribution'; S. Nadarajah, D. K. Dey in
        Computers and Mathematics with Applications 49 (2005) 715-721\par
    The last reference provides direct expressions for some of the densities
    when the linear combination of only two Ts is just an addition. It can be
    used for testing the results here.\par
    Another available test on this algorithm stems from the realization that a
    linear convex (\f$ \sum a_i=1\f$) combination of Ts of order one is stable
    in the distribution sense (but this result is often of no practical use
    because of its non-finite variance).\par
    This implementation is for two or more T variables in the linear
    combination albeit these must be of odd order. The case of exactly two T of
    odd order is known to be a finite mixture of Ts but that result is not used
    here. On this line see 'Linearization coefficients of Bessel polynomials'
    C.Berg, C.Vignat; February 2008; arXiv:math/0506458

        \todo Implement the series expansion solution for the addition of
        two Ts of even order described in: 'On the density of the sum of two
        independent Student t-random vectors' C.Berg, C.Vignat; June 2009;
        eprint arXiv:0906.3037
    */
    class CumulativeBehrensFisher { // ODD orders only by now, rename?
    public:
        /*!
            @param degreesFreedom Degrees of freedom of the Ts convolved. The
                algorithm is limited to odd orders only.
            @param factors Factors in the linear combination of the Ts.
        */
        CumulativeBehrensFisher(
            const std::vector<Integer>& degreesFreedom = std::vector<Integer>(),
            const std::vector<Real>& factors = std::vector<Real>());

        //! Degrees of freedom of the Ts involved in the convolution.
        const std::vector<Integer>& degreeFreedom() const {
            return degreesFreedom_;
        }
        //! Factors in the linear combination.
        const std::vector<Real>& factors() const {
            return factors_;
        }
    private:
        /*! \brief Student t characteristic polynomials.

        Generates the polynomial coefficients defining the characteristic
        function of a T distribution \f$T_\nu\f$ of odd order; \f$\nu=2n+1\f$.
        In general the characteristic function is given by:
        \f[
        \phi_{\nu}(t) = \varphi_{n}(t) \exp{-\nu^{1/2}|t|} ;\,where\,\nu = 2n+1
        \f]
        where \