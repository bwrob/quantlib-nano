/*
    nanobind/stl/chrono.h: conversion between std::chrono and python's datetime

    Copyright (c) 2023 Hudson River Trading LLC <opensource@hudson-trading.com>

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/
#pragma once

#include <nanobind/nanobind.h>

// Functions for working with objects in the Python 'datetime' module,
// used by the std::chrono type caster in <nanobind/stl/chrono.h>.
// This is pretty straightforward except on Limited API builds.
// Note that while PyPy does provide <datetime.h>, it implements
// the macro-like calls there (PyDateTime_DATE_GET_HOUR, etc) as full
// function calls that can fail. We use the limited-API logic on PyPy
// in order to be able to handle errors better.

#if !defined(Py_LIMITED_API) && !defined(PYPY_VERSION)

#  include <datetime.h>
#endif

#if defined(__GNUC__)
// warning: warning: declaration of '...' with attribute 'noinline' follows inline declaration

#  pragma GCC diagnostic push