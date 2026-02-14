nd::call_guard<Cs...>;
};

template <size_t Nurse, size_t Patient, typename... Ts>
struct func_extra_info<nanobind::keep_alive<Nurse, Patient>, Ts...> : func_extra_info<Ts...> {
    static constexpr bool pre_post_hooks = true;
};

template <typename Policy, typename... Ts>
struct func_extra_info<call_policy<Policy>, Ts...> : func_extra_info<Ts...> {
    static constexpr bool pre_post_hooks = true;
};

template <typename... Ts>
struct func_extra_info<arg_locked, Ts...> : func_extra_info<Ts...> {
    static constexpr size_t nargs_locked = 1 + func_extra_info<Ts...>::nargs_locked;
};

template <typename... Ts>
struct func_extra_info<lock_self, Ts...> : func_extra_info<Ts...> {
    static constexpr size_t nargs_locked = 1 + func_extra_info<Ts...>::nargs_locked;
};

NB_INLINE void process_precall(PyObject **, size_t, detail::cleanup_list *, void *) { }

template <size_t NArgs, typename Policy>
NB_INLINE void
process_precall(PyObject **args, std::integral_constant<size_t, NArgs> nargs,
                detail::cleanup_list *cleanup, call_policy<Policy> *) {
    Policy::precall(args, nargs, cleanup);
}

NB_INLINE void process_postcall(PyObject **, size_t, PyObject *, void *) { }

template <size_t NArgs, size_t Nurse, size_t Patient>
NB_INLINE void
process_postcall(PyObject **args, std::integral_constant<size_t, NArgs>,
                 PyObject *result, nanobind::keep_alive<Nurse, Patient> *) {
    static_assert(Nurse != Patient,
                  "keep_alive with the same argument as both nurse and patient "
                  "doesn't make sense");
    static_assert(Nurse <= NArgs && Patient <= NArgs,
                  "keep_alive template parameters must be in the range "
                  "[0, number of C++ function arguments]");
    keep_alive(Nurse   == 0 ? result : args[Nurse - 1],
               Patient == 0 ? result : args[Patient - 1]);
}

template <size_t NArgs, typename Policy>
NB_INLINE void
process_postcall(PyObject **args, std::integral_constant<size_t, NArgs> nargs,
                 PyObject *&result, call_policy<Policy> *) {
    // result_guard avoids leaking a reference to the return object
    // if postcall throws an exception
    object result_guard = steal(result);
    Policy::postcall(args, nargs, result);
    result_guard.release();
}

NAMESPACE_END(detail)
NAMESPACE_END(NB_NAMESPACE)
