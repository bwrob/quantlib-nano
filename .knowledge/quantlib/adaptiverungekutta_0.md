/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2012 Peter Caspers

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

/*! \file adaptiverungekutta.hpp
    \brief Runge-Kutta ODE integration

    Runge Kutta method with adaptive stepsize as described in
    Numerical Recipes in C, Chapter 16.2
*/

#ifndef quantlib_adaptive_runge_kutta_hpp
#define quantlib_adaptive_runge_kutta_hpp

#include <ql/types.hpp>
#include <ql/errors.hpp>
#include <functional>
#include <vector>
#include <cmath>
#include <complex>

namespace QuantLib {

    template <class T = Real>
    class AdaptiveRungeKutta {
      public:
        typedef std::function<std::vector<T>(const Real, const std::vector<T>&)> OdeFct;
        typedef std::function<T(const Real, const T)> OdeFct1d;

        /*! The class is constructed with the following inputs:
            - eps       prescribed error for the solution
            - h1        start step size
            - hmin      smallest step size allowed
        */

        AdaptiveRungeKutta(const Real eps = 1.0e-6, const Real h1 = 1.0e-4, const Real hmin = 0.0)
        : eps_(eps), h1_(h1), hmin_(hmin), b31(3.0 / 40.0), b32(9.0 / 40.0), b51(-11.0 / 54.0),
          b53(-70.0 / 27.0), b54(35.0 / 27.0), b61(1631.0 / 55296.0), b62(175.0 / 512.0),
          b63(575.0 / 13824.0), b64(44275.0 / 110592.0), b65(253.0 / 4096.0), c1(37.0 / 378.0),
          c3(250.0 / 621.0), c4(125.0 / 594.0), c6(512.0 / 1771.0), dc1(c1 - 2825.0 / 27648.0),
          dc3(c3 - 18575.0 / 48384.0), dc4(c4 - 13525.0 / 55296.0), dc5(-277.0 / 14336.0),
          dc6(c6 - 0.25) {}

        /*! Integrate the ode from \f$ x1 \f$ to \f$ x2 \f$ with
            initial value condition \f$ f(x1)=y1 \f$.

            The ode is given by a function \f$ F: R \times K^n
            \rightarrow K^n \f$ as \f$ f'(x) = F(x,f(x)) \f$, $K=R,
            C$ */
        std::vector<T> operator()(const OdeFct& ode, const std::vector<T>& y1, Real x1, Real x2);
        T operator()(const OdeFct1d& ode, T y1, Real x1, Real x2);

      private:
        void rkqs(std::vector<T>& y,
                  const std::vector<T>& dydx,
                  Real& x,
                  Real htry,
                  Real eps,
                  const std::vector<Real>& yScale,
                  Real& hdid,
                  Real& hnext,
                  const OdeFct& derivs);
        void rkck(const std::vector<T>& y,
                  const std::vector<T>& dydx,
                  Real x,
                  Real h,
                  std::vector<T>& yout,
                  std::vector<T>& yerr,
                  const OdeFct& derivs);

        const std::vector<T> yStart_;
        const Real eps_, h1_, hmin_;
        const Real a2 = 0.2, a3 = 0.3, a4 = 0.6, a5 = 1.0, a6 = 0.875, b21 = 0.2, b31, b32,
                   b41 = 0.3, b42 = -0.9, b43 = 1.2, b51, b52 = 2.5, b53, b54, b61, b62, b63, b64,
                   b65, c1, c3, c4, c6, dc1, dc3, dc4, dc5, dc6;
        const double ADAPTIVERK_MAXSTP = 10000, ADAPTIVERK_TINY = 1.0E-30, ADAPTIVERK_SAFETY = 0.9,
                     ADAPTIVERK_PGROW = -0.2, ADAPTIVERK_PSHRINK = -0.25,
                     ADAPTIVERK_ERRCON = 1.89E-4;
    };



    template<class T>
    std::vector<T> AdaptiveRungeKutta<T>::operator()(const OdeFct& ode,
                                       