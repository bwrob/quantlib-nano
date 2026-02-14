/*
    nanobind/nb_types.h: nb::dict/str/list/..: C++ wrappers for Python types

    Copyright (c) 2022 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

NAMESPACE_BEGIN(NB_NAMESPACE)

/// Macro defining functions/constructors for nanobind::handle subclasses
#define NB_OBJECT(Type, Parent, Str, Check)                                    \
public:                                                                        \
    static constexpr auto Name = ::nanobind::detail::const_name(Str);          \
    NB_INLINE Type(handle h, ::nanobind::detail::borrow_t)                     \
        : Parent(h, ::nanobind::detail::borrow_t{}) { }                        \
    NB_INLINE Type(handle h, ::nanobind::detail::steal_t)                      \
        : Parent(h, ::nanobind::detail::steal_t{}) { }                         \
    NB_INLINE static bool check_(handle h) {                                   \
        return Check(h.ptr());                                                 \
    }

/// Like NB_OBJECT but allow null-initialization
#define NB_OBJECT_DEFAULT(Type, Parent, Str, Check)                            \
    NB_OBJECT(Type, Parent, Str, Check)                                        \
    NB_INLINE Type() : Parent() {}

/// Helper macro to create detail::api comparison functions
#define NB_DECL_COMP(name)                                                     \
    template <typename T2> NB_INLINE bool name(const api<T2> &o) const;

#define NB_IMPL_COMP(name, op)                                                 \
    template <typename T1> template <typename T2>                              \
    NB_INLINE bool api<T1>::name(const api<T2> &o) const {                     \
        return detail::obj_comp(derived().ptr(), o.derived().ptr(), op);       \
    }

/// Helper macros to create detail::api unary operators
#define NB_DECL_OP_1(name)                                                     \
    NB_INLINE object name() const;

#define NB_IMPL_OP_1(name, op)                                                 \
    template <typename T> NB_INLINE object api<T>::name() const {              \
        return steal(detail::obj_op_1(derived().ptr(), op));                   \
    }

/// Helper macros to create detail::api binary operators
#define NB_DECL_OP_2(name)                                                     \
    template <typename T2> NB_INLINE object name(const api<T2> &o) const;

#define NB_IMPL_OP_2(name, op)                                                 \
    template <typename T1> template <typename T2>                              \
    NB_INLINE object api<T1>::name(const api<T2> &o) const {                   \
        return steal(                                                          \
            detail::obj_op_2(derived().ptr(), o.derived().ptr(), op));         \
    }

#define NB_DECL_OP_2_I(name)                                                   \
    template <typename T2> NB_INLINE object name(const api<T2> &o);

#define NB_IMPL_OP_2_I(name, op)                                               \
    template <typename T1> template <typename T2>                              \
    NB_INLINE object api<T1>::name(const api<T2> &o) {                         \
        return steal(                                                          \
            detail::obj_op_2(derived().ptr(), o.derived().ptr(), op));         \
    }

#define NB_IMPL_OP_2_IO(name)                                                  \
    template <typename T> NB_INLINE decltype(auto) name(const api<T> &o) {     \
        return operator=(handle::name(o));                                     \
    }

// A few forward declarations
class object;
class handle;
class iterator;

template <typename T = object> NB_INLINE T borrow(handle h);
template <typename T = object> NB_INLINE T steal(handle h);

NAMESPACE_BEGIN(detail)

template <typename T, typename SFINA