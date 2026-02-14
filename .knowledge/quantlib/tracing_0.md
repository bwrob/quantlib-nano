/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2005 StatPro Italia srl

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

/*! \file tracing.hpp
    \brief tracing facilities
*/

#ifndef quantlib_tracing_hpp
#define quantlib_tracing_hpp

#include <ql/types.hpp>
#include <ql/errors.hpp>
#include <ql/patterns/singleton.hpp>
#include <boost/current_function.hpp>
#include <iosfwd>

namespace QuantLib::detail {

        class Tracing : public Singleton<Tracing> {
            friend class QuantLib::Singleton<Tracing>;
          private:
            Tracing();  // NOLINT(modernize-use-equals-delete)
          public:
            void enable() {
                #if defined(QL_ENABLE_TRACING)
                enabled_ = true;
                #else
                QL_FAIL("tracing support not available");
                #endif
            }
            void disable() { enabled_ = false; }
            void setStream(std::ostream& stream) { out_ = &stream; }
            bool enabled() const { return enabled_; }
            std::ostream& stream() { return *out_; }
            Integer depth() const { return depth_; }
            void down() { depth_++; }
            void up() { depth_--; }
          private:
            std::ostream* out_;
            bool enabled_ = false;
            Integer depth_ = 0;
        };

    }

/*! \addtogroup macros
    @{
*/

/*! \defgroup debugMacros Debugging macros

    For debugging purposes, macros can be used to output information
    about the code being executed.  Instrumenting code as in:
    \code
    namespace Foo {

        int bar(int i) {
            QL_TRACE_ENTER_FUNCTION;
            QL_TRACE_VARIABLE(i);

            if (i == 42) {
                QL_TRACE_LOCATION;
                QL_TRACE("Right answer, but no question");
            } else {
                QL_TRACE_LOCATION;
                QL_TRACE("Wrong answer");
                i *= 2;
            }

            QL_TRACE_VARIABLE(i);
            QL_TRACE_EXIT_FUNCTION;
            return i;
        }

    }
    \endcode
    will output a trace like the following when the code is run:
    \code
    trace[3]: Entering int Foo::bar(int)
    trace[3]: i = 21
    trace[3]: At line 16 in tracing_example.cpp
    trace[3]: Wrong answer
    trace[3]: i = 42
    trace[3]: Exiting int Foo::bar(int)
    \endcode
    (the actual output will depend on the compiler and the file
    names).  A word of warning must be added: adding so much tracing
    to your code might degrade its readability.

    @{
*/

/*! \def QL_TRACE_ENABLE
    \brief enable tracing

    The statement
    \code
    QL_TRACE_ENABLE;
    \endcode
    can be used to enable tracing. Such statement might be
    ignored; refer to QL_TRACE for details.
*/

/*! \def QL_TRACE_DISABLE
    \brief disable tracing

    The statement
    \code
    QL_TRACE_DISABLE;
    \endcode
    can be used to disable tracing. Such statement might be
    ignored; refer to QL_TRACE for details.
*/

/*! \def QL_TRACE_ON
    \brief set tracing stream

    The statement
    \code
    QL_TRACE_ON(stream);
    \endcode
    can be used to set the stream where tracing messages are
    output. Such statement might be ignored; refer to QL_TRACE for
    details.
*/

/*! \def QL_TRACE
    \brief output tracing information

    The statement
 