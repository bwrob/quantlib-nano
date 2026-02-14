/*
    nanobind/intrusive/counter.h: Intrusive reference counting sample
    implementation.

    Intrusive reference counting is a simple solution for various lifetime and
    ownership-related issues that can arise in Python bindings of C++ code. The
    implementation here represents one of many ways in which intrusive
    reference counting can be realized and is included for convenience.

    The code in this file is designed to be truly minimal: it depends neither
    on Python, nanobind, nor the STL. This enables its use in small projects
    with a 100% optional Python interface.

    Two section of nanobind's documentation discuss intrusive reference
    counting in general:

     - https://nanobind.readthedocs.io/en/latest/ownership.html
     - https://nanobind.readthedocs.io/en/latest/ownership_adv.html

    Comments below are specific to this sample implementation.

    Copyright (c) 2023 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

#pragma once

#include <cstdint>

// Override this definition to specify DLL export/import declarations
#if !defined(NB_INTRUSIVE_EXPORT)

#  define NB_INTRUSIVE_EXPORT
#endif

#if !defined(Py_PYTHON_H)
/* While the implementation below does not directly depend on Python, the
   PyObject type occurs in a few function interfaces (in a fully opaque
   manner). The lines below forward-declare it. */
extern "C" {
    struct _object;
    typedef _object PyObject;
};
#endif

#if !defined(NAMESPACE_BEGIN)

#  define NAMESPACE_BEGIN(name) namespace name {
#endif

#if !defined(NAMESPACE_END)