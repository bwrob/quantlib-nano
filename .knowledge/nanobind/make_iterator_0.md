/*
    nanobind/make_iterator.h: nb::make_[key,value_]iterator()

    This implementation is a port from pybind11 with minimal adjustments.

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

#pragma once

#include <nanobind/nanobind.h>
#include <nanobind/stl/pair.h>

NAMESPACE_BEGIN(NB_NAMESPACE)
NAMESPACE_BEGIN(detail)

/* There are a large number of apparently unused template arguments because
   each combination requires a separate nb::class_ registration. */
template <typename Access, rv_policy Policy, typename Iterator,
          typename Sentinel, typename ValueType, typename... Extra>
struct iterator_state {
    Iterator it;
    Sentinel end;
    bool first_or_done;
};

template <typename T>
struct remove_rvalue_ref { using type = T; };
template <typename T>
struct remove_rvalue_ref<T&&> { using type = T; };

// Note: these helpers take the iterator by non-const reference because some
// iterators in the wild can't be dereferenced when const.
template <typename Iterator> struct iterator_access {
    using result_type = decltype(*std::declval<Iterator &>());
    result_type operator()(Iterator &it) const { return *it; }
};

template <typename Iterator> struct iterator_key_access {
    // Note double parens in decltype((...)) to capture the value category
    // as well. This will be lvalue if the iterator's operator* returned an
    // lvalue reference, and xvalue if the iterator's operator* returned an
    // object (or rvalue reference but that's unlikely). decltype of an xvalue
    // produces T&&, but we want to return a value T from operator() in that
    // case, in order to avoid creating a Python object that references a
    // C++ temporary. Thus, pass the result through remove_rvalue_ref.
    using result_type = typename remove_rvalue_ref<
        decltype(((*std::declval<Iterator &>()).first))>::type;
    result_type operator()(Iterator &it) const { return (*it).first; }
};

template <typename Iterator> struct iterator_value_access {
    using result_type = typename remove_rvalue_ref<
        decltype(((*std::declval<Iterator &>()).second))>::type;
    result_type operator()(Iterator &it) const { return (*it).second; }
};

template <typename Access, rv_policy Policy, typename Iterator,
          typename Sentinel, typename ValueType, typename... Extra>
typed<iterator, ValueType> make_iterator_impl(handle scope, const char *name,
                                              Iterator first, Sentinel last,
                                              Extra &&...extra) {
    using State = iterator_state<Access, Policy, Iterator, Sentinel, ValueType, Extra...>;

    static_assert(
        !detail::is_base_caster_v<detail::make_caster<ValueType>> ||
        detail::is_copy_constructible_v<ValueType> ||
        (Policy != rv_policy::automatic_reference &&
         Policy != rv_policy::copy),
        "make_iterator_impl(): the generated __next__ would copy elements, so the "
        "element type must be copy-constructible");

    {
        static ft_mutex mu;
        ft_lock_guard lock(mu);
        if (!type<State>().is_valid()) {
            class_<State>(scope, name)
                .def("__iter__", [](handle h) { return h; })
                .def("__next__",
                    [](State &s) -> ValueType {
                        if (!s.first_or_done)
                            ++s.it;
                        else
                            s.first_or_done = false;

                        if (s.it == s.end) {
                            s.first_or_done = true;
                            throw stop_iteration();
                        }

                        return Access()(s.it);
                    },
                    std::forward<Extra>(extra)...,
                    Policy);
        }
    }
    return borrow<typed<iterator, ValueType>>(cast(State{
        std::forward<Iterator>(first), std::forward<Sentinel>(last), true 