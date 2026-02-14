/* -*- mode: c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

/*
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl
 Copyright (C) 2003, 2004, 2005, 2006, 2007 StatPro Italia srl
 Copyright (C) 2015 CompatibL

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

/*! \file qldefines.hpp
    \brief Global definitions and compiler switches.
*/

#ifndef quantlib_defines_hpp
#define quantlib_defines_hpp

/* install-hook */

#ifdef _MSC_VER
/* Microsoft-specific, but needs to be defined before
   including <boost/config.hpp> which somehow includes
   <math.h> under VC++10
*/
#define _USE_MATH_DEFINES
#endif

#include <boost/config.hpp>
#include <boost/version.hpp>
#if BOOST_VERSION < 104800
    #error using an old version of Boost, please update.
#endif
#if !defined(BOOST_ENABLE_ASSERT_HANDLER)
    #define BOOST_ENABLE_ASSERT_HANDLER
#endif

/* This allows one to include a given file at this point by
   passing it as a compiler define (e.g., -DQL_INCLUDE_FIRST=foo.hpp).

   The idea is to provide a hook for defining QL_REAL and at the
   same time including any necessary headers for the new type.
*/
#define INCLUDE_FILE(F) INCLUDE_FILE_(F)
#define INCLUDE_FILE_(F) #F
#ifdef QL_INCLUDE_FIRST

#    include INCLUDE_FILE(QL_INCLUDE_FIRST)
#endif
#undef INCLUDE_FILE_
#undef INCLUDE_FILE

/* Eventually these might go into userconfig.hpp.
   For the time being, we hard code them here.
   They can be overridden by passing the #define to the compiler.
*/
#ifndef QL_INTEGER

#    define QL_INTEGER int
#endif

#ifndef QL_BIG_INTEGER

#    define QL_BIG_INTEGER long
#endif

#ifndef QL_REAL