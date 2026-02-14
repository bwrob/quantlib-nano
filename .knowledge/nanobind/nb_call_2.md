                  std::is_same_v<Args, args_proxy> ||
                    std::is_same_v<Args, kwargs_proxy>) || ...)) {
        // Complex call with keyword arguments, *args/**kwargs expansion, etc.
        size_t nargs = 0, nkwargs = 0, nargs2 = 0, nkwargs2 = 0;

        // Determine storage requirements for positional and keyword args
        (call_analyze(nargs, nkwargs, (const Args &) args_), ...);

        // Allocate memory on the stack
        PyObject **args =
            (PyObject **) alloca((nargs + nkwargs + 1) * sizeof(PyObject *));

        PyObject *kwnames =
            nkwargs ? PyTuple_New((Py_ssize_t) nkwargs) : nullptr;

        // Fill 'args' and 'kwnames' variables
        (call_init<policy>(args + 1, kwnames, nargs2, nkwargs2, nargs,
                           (forward_t<Args>) args_), ...);

        NB_DO_VECTORCALL();
    } else {
        // Simple version with only positional arguments
        PyObject *args[sizeof...(Args) + 1], *kwnames = nullptr;
        size_t nargs = 0;

        ((args[1 + nargs++] =
              detail::make_caster<Args>::from_cpp(
                  (detail::forward_t<Args>) args_, policy, nullptr)
                  .ptr()),
         ...);

        NB_DO_VECTORCALL();
    }
}

#undef NB_DO_VECTORCALL

#if defined(_MSC_VER)
