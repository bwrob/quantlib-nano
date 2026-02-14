/*
    nanobind/nb_func.h: Functionality for binding C++ functions/methods

    Copyright (c) 2022 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

NAMESPACE_BEGIN(NB_NAMESPACE)
NAMESPACE_BEGIN(detail)

template <typename Caster>
bool from_python_remember_conv(Caster &c, PyObject **args, uint8_t *args_flags,
                               cleanup_list *cleanup, size_t index) {
    size_t size_before = cleanup->size();
    if (!c.from_python(args[index], args_flags[index], cleanup))
        return false;

    // If an implicit conversion took place, update the 'args' array so that
    // any keep_alive annotation or postcall hook can be aware of this change
    size_t size_after = cleanup->size();
    if (size_after != size_before)
        args[index] = (*cleanup)[size_after - 1];

    return true;
}

// Return the number of nb::arg and nb::arg_v types in the first I types Ts.
// Invoke with std::make_index_sequence<sizeof...(Ts)>() to provide
// an index pack 'Is' that parallels the types pack Ts.
template <size_t I, typename... Ts, size_t... Is>
constexpr size_t count_args_before_index(std::index_sequence<Is...>) {
    static_assert(sizeof...(Is) == sizeof...(Ts));
    return ((Is < I && std::is_base_of_v<arg, Ts>) + ... + 0);
}

#if defined(NB_FREE_THREADED)
struct ft_args_collector {
    PyObject **args;
    handle h1;
    handle h2;
    size_t index = 0;

    NB_INLINE explicit ft_args_collector(PyObject **a) : args(a) {}
    NB_INLINE void apply(arg_locked *) {
        if (h1.ptr() == nullptr)
            h1 = args[index];
        h2 = args[index];
        ++index;
    }
    NB_INLINE void apply(arg *) { ++index; }
    NB_INLINE void apply(...) {}
};

struct ft_args_guard {
    NB_INLINE void lock(const ft_args_collector& info) {
        PyCriticalSection2_Begin(&cs, info.h1.ptr(), info.h2.ptr());
    }
    ~ft_args_guard() {
        PyCriticalSection2_End(&cs);
    }
    PyCriticalSection2 cs;
};
#endif

struct no_guard {};

template <bool ReturnRef, bool CheckGuard, typename Func, typename Return,
          typename... Args, size_t... Is, typename... Extra>
NB_INLINE PyObject *func_create(Func &&func, Return (*)(Args...),
                                std::index_sequence<Is...> is,
                                const Extra &...extra) {
    using Info = func_extra_info<Extra...>;

    if constexpr (CheckGuard && !std::is_same_v<typename Info::call_guard, void>) {
        return func_create<ReturnRef, false>(
            [func = (forward_t<Func>) func](Args... args) NB_INLINE_LAMBDA -> Return {
                typename Info::call_guard::type g;
                (void) g;
                return func((forward_t<Args>) args...);
            },
            (Return(*)(Args...)) nullptr, is, extra...);
    }

    (void) is;

    // Detect locations of nb::args / nb::kwargs (if they exist).
    // Find the first and last occurrence of each; we'll later make sure these
    // match, in order to guarantee there's only one instance.
    static constexpr size_t
        args_pos_1 = index_1_v<std::is_same_v<intrinsic_t<Args>, args>...>,
        args_pos_n = index_n_v<std::is_same_v<intrinsic_t<Args>, args>...>,
        kwargs_pos_1 = index_1_v<std::is_same_v<intrinsic_t<Args>, kwargs>...>,
        kwargs_pos_n = index_n_v<std::is_same_v<intrinsic_t<Args>, kwargs>...>,
        nargs = sizeof...(Args);

    constexpr bool has_arg_defaults = (detail::has_arg_defaults_v<Args> || ... || false);

    // Determine the number of nb::arg/nb::arg_v annotations
    constexpr size_t nargs_provided =
        (std::is_base_of_v<arg, Extra> + ... + 0);
    constexpr bool is_method_det =
        (std::is_same_v<is_method, Extra> + ... + 0) != 0;
    constexpr bool is_getter_det =
        (std::is_same_v<is_getter, Extra> + ... + 0) != 0;
    constexpr bool has_arg_annotations = has_arg_defaults || (nargs_provided > 0 && !is_getter_det);

    // Determi
