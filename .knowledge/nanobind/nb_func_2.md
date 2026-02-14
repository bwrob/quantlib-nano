unc;
    };

    // The following temporary record will describe the function in detail
    func_data_prelim<has_arg_defaults ? (nargs - is_method_det) : nargs_provided> f;

    // Initialize argument flags. The first branch turns std::optional<> types
    // into implicit nb::none() annotations (skipping 'self' for methods).
    if constexpr (has_arg_defaults) {
        ((void)(Is < is_method_det ||
                (f.args[Is - is_method_det] = { nullptr, nullptr, nullptr, nullptr,
                    has_arg_defaults_v<Args> ? (uint8_t) cast_flags::accepts_none
                                             : (uint8_t) 0 }, true)), ...);
    } else if constexpr (nargs_provided > 0) {
        for (size_t i = 0; i < nargs_provided; ++i)
            f.args[i].flag = 0;
    }

    f.flags = (args_pos_1   < nargs ? (uint32_t) func_flags::has_var_args   : 0) |
              (kwargs_pos_1 < nargs ? (uint32_t) func_flags::has_var_kwargs : 0) |
              (ReturnRef            ? (uint32_t) func_flags::return_ref     : 0) |
              (has_arg_annotations  ? (uint32_t) func_flags::has_args       : 0);

    /* Store captured function inside 'func_data_prelim' if there is space. Issues
       with aliasing are resolved via separate compilation of libnanobind. */
    if constexpr (sizeof(capture) <= sizeof(f.capture)) {
        capture *cap = (capture *) f.capture;
        new (cap) capture{ (forward_t<Func>) func };

        if constexpr (!std::is_trivially_destructible_v<capture>) {
            f.flags |= (uint32_t) func_flags::has_free;
            f.free_capture = [](void *p) {
                ((capture *) p)->~capture();
            };
        }
    } else {
        void **cap = (void **) f.capture;
        cap[0] = new capture{ (forward_t<Func>) func };

        f.flags |= (uint32_t) func_flags::has_free;
        f.free_capture = [](void *p) {
            delete (capture *) ((void **) p)[0];
        };
    }

    f.impl = [](void *p, PyObject **args, uint8_t *args_flags, rv_policy policy,
                cleanup_list *cleanup) NB_INLINE_LAMBDA -> PyObject * {
        (void) p; (void) args; (void) args_flags; (void) policy; (void) cleanup;

        const capture *cap;
        if constexpr (sizeof(capture) <= sizeof(f.capture))
            cap = (capture *) p;
        else
            cap = (capture *) ((void **) p)[0];

        tuple<make_caster<Args>...> in;
        (void) in;

#if defined(NB_FREE_THREADED)
        std::conditional_t<Info::nargs_locked != 0, ft_args_guard, no_guard> guard;
        if constexpr (Info::nargs_locked) {
            ft_args_collector collector{args};
            if constexpr (is_method_det) {
                if constexpr (lock_self_det)
                    collector.apply((arg_locked *) nullptr);
                else
                    collector.apply((arg *) nullptr);
            }
            (collector.apply((Extra *) nullptr), ...);
            guard.lock(collector);
        }
#endif

        if constexpr (Info::pre_post_hooks) {
            std::integral_constant<size_t, nargs> nargs_c;
            (process_precall(args, nargs_c, cleanup, (Extra *) nullptr), ...);
            if ((!from_python_remember_conv(in.template get<Is>(), args,
                                            args_flags, cleanup, Is) || ...))
                return NB_NEXT_OVERLOAD;
        } else {
            if ((!in.template get<Is>().from_python(args[Is], args_flags[Is],
                                                    cleanup) || ...))
                return NB_NEXT_OVERLOAD;
        }

        PyObject *result;
        if constexpr (std::is_void_v<Return>) {
#if defined(_WIN32) && !defined(__CUDACC__) // temporary workaround for an internal compiler error in MSVC
            cap->func(static_cast<cast_t<Args>>(in.template get<Is>())...);
#else
            cap->func(in.template get<Is>().operator cast_t<Args>()...);
#endif
            result = Py_None;
            Py_INCREF(result);
        } else {
#if defined(_WI
