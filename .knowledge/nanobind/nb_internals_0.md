#pragma once

#if defined(__GNUC__)
// Don't warn about missing fields in PyTypeObject declarations

#  pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#elif defined(_MSC_VER)
// Silence warnings that MSVC reports in robin_*.h

#  pragma warning(disable: 4127) // conditional expression is constant

#  pragma warning(disable: 4324) // structure was padded due to alignment specifier

#  pragma warning(disable: 4293) // shift count negative or too big  <-- erroneously raised in a constexpr-disabled block

#  pragma warning(disable: 4310) // cast truncates constant value <-- erroneously raised in a constexpr-disabled block
#endif

#include <nanobind/nanobind.h>
#include <tsl/robin_map.h>
#if defined(NB_FREE_THREADED)
#include <atomic>
#endif
#include <cstring>
#include <string_view>
#include <functional>
#include "hash.h"

#if TSL_RH_VERSION_MAJOR != 1 || TSL_RH_VERSION_MINOR < 3

#  error nanobind depends on tsl::robin_map, in particular version >= 1.3.0, <2.0.0
#endif

#if defined(_MSC_VER)

#  define NB_THREAD_LOCAL __declspec(thread)
#else

#  define NB_THREAD_LOCAL __thread
#endif

#if PY_VERSION_HEX >= 0x030A0000

#  define NB_TPFLAGS_IMMUTABLETYPE Py_TPFLAGS_IMMUTABLETYPE
#else

#  define NB_TPFLAGS_IMMUTABLETYPE 0
#endif

NAMESPACE_BEGIN(NB_NAMESPACE)
NAMESPACE_BEGIN(detail)

#if defined(NB_COMPACT_ASSERTIONS)
[[noreturn]] extern void fail_unspecified() noexcept;

#  define check(cond, ...) if (NB_UNLIKELY(!(cond))) nanobind::detail::fail_unspecified()
#else
