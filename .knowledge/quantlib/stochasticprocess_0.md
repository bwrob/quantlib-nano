/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2003 Ferdinando Ametrano
 Copyright (C) 2001, 2002, 2003 Sadruddin Rejeb
 Copyright (C) 2004, 2005 StatPro Italia srl

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

/*! \file stochasticprocess.hpp
    \brief stochastic processes
*/

#ifndef quantlib_stochastic_process_hpp
#define quantlib_stochastic_process_hpp

#include <ql/time/date.hpp>
#include <ql/patterns/observable.hpp>
#include <ql/math/matrix.hpp>

namespace QuantLib {

    //! multi-dimensional stochastic process class.
    /*! This class describes a stochastic process governed by
        \f[
        d\mathrm{x}_t = \mu(t, x_t)\mathrm{d}t
                      + \sigma(t, \mathrm{x}_t) \cdot d\mathrm{W}_t.
        \f]
    */
    class StochasticProcess : public Observer, public Observable {
      public:
        //! discretization of a stochastic process over a given time interval
        class discretization {
          public:
            virtual ~discretization() = default;
            virtual Array drift(const StochasticProcess&,
                                Time t0,
                                const Array& x0,
                                Time dt) const = 0;
            virtual Matrix diffusion(const StochasticProcess&,
                                     Time t0,
                                     const Array& x0,
                                     Time dt) const = 0;
            virtual Matrix covariance(const StochasticProcess&,
                                      Time t0,
                                      const Array& x0,
                                      Time dt) const = 0;
        };
        ~StochasticProcess() override = default;
        //! \name Stochastic process interface
        //@{
        //! returns the number of dimensions of the stochastic process
        virtual Size size() const = 0;
        //! returns the number of independent factors of the process
        virtual Size factors() const;
        //! returns the initial values of the state variables
        virtual Array initialValues() const = 0;
        /*! \brief returns the drift part of the equation, i.e.,
                   \f$ \mu(t, \mathrm{x}_t) \f$
        */
        virtual Array drift(Time t,
                            const Array& x) const = 0;
        /*! \brief returns the diffusion part of the equation, i.e.
                   \f$ \sigma(t, \mathrm{x}_t) \f$
        */
        virtual Matrix diffusion(Time t,
                                 const Array& x) const = 0;
        /*! returns the expectation
            \f$ E(\mathrm{x}_{t_0 + \Delta t}
                | \mathrm{x}_{t_0} = \mathrm{x}_0) \f$
            of the process after a time interval \f$ \Delta t \f$
            according to the given discretization. This method can be
            overridden in derived classes which want to hard-code a
            particular discretization.
        */
        virtual Array expectation(Time t0,
                                  const Array& x0,
                                  Time dt) const;
        /*! returns the standard deviation
            \f$ S(\mathrm{x}_{t_0 + \Delta t}
                | \mathrm{x}_{t_0} = \mathrm{x}_0) \f$
            of the process after a time interval \f$ \Delta t \f$
            according to th