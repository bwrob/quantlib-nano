ne the number of potentially-locked function arguments
    constexpr bool lock_self_det =
        (std::is_same_v<lock_self, Extra> + ... + 0) != 0;
    static_assert(Info::nargs_locked <= 2,
        "At most two function arguments can be locked");
    static_assert(!(lock_self_det && !is_method_det),
        "The nb::lock_self() annotation only applies to methods");

    // Detect location of nb::kw_only annotation, if supplied. As with args/kwargs
    // we find the first and last location and later verify they match each other.
    // Note this is an index in Extra... while args/kwargs_pos_* are indices in
    // Args... .
    constexpr size_t
        kwonly_pos_1 = index_1_v<std::is_same_v<kw_only, Extra>...>,
        kwonly_pos_n = index_n_v<std::is_same_v<kw_only, Extra>...>;

    // Arguments after nb::args are implicitly keyword-only even if there is no
    // nb::kw_only annotation
    constexpr bool explicit_kw_only = kwonly_pos_1 != sizeof...(Extra);
    constexpr bool implicit_kw_only = args_pos_1 + 1 < kwargs_pos_1;

    // A few compile-time consistency checks
    static_assert(args_pos_1 == args_pos_n && kwargs_pos_1 == kwargs_pos_n,
        "Repeated use of nb::kwargs or nb::args in the function signature!");
    static_assert(!has_arg_annotations || has_arg_defaults || nargs_provided + is_method_det == nargs,
        "The number of nb::arg annotations must match the argument count!");
    static_assert(kwargs_pos_1 == nargs || kwargs_pos_1 + 1 == nargs,
        "nb::kwargs must be the last element of the function signature!");
    static_assert(args_pos_1 == nargs || args_pos_1 < kwargs_pos_1,
        "nb::args must precede nb::kwargs if both are present!");
    static_assert(has_arg_annotations || (!implicit_kw_only && !explicit_kw_only),
        "Keyword-only arguments must have names!");

    // Find the index in Args... of the first keyword-only parameter. Since
    // the 'self' parameter doesn't get a nb::arg annotation, we must adjust
    // by 1 for methods. Note that nargs_before_kw_only is only used if
    // a kw_only annotation exists (i.e., if explicit_kw_only is true);
    // the conditional is just to save the compiler some effort otherwise.
    constexpr size_t nargs_before_kw_only =
        explicit_kw_only
            ? is_method_det + count_args_before_index<kwonly_pos_1, Extra...>(
                  std::make_index_sequence<sizeof...(Extra)>())
            : nargs;

    (void) kwonly_pos_n;

    if constexpr (explicit_kw_only) {
        static_assert(kwonly_pos_1 == kwonly_pos_n,
            "Repeated use of nb::kw_only annotation!");

        // If both kw_only and *args are specified, kw_only must be
        // immediately after the nb::arg for *args.
        static_assert(args_pos_1 == nargs || nargs_before_kw_only == args_pos_1 + 1,
            "Arguments after nb::args are implicitly keyword-only; any "
            "nb::kw_only() annotation must be positioned to reflect that!");

        // If both kw_only and **kwargs are specified, kw_only must be
        // before the nb::arg for **kwargs.
        static_assert(nargs_before_kw_only < kwargs_pos_1,
            "Variadic nb::kwargs are implicitly keyword-only; any "
            "nb::kw_only() annotation must be positioned to reflect that!");
    }

    // Collect function signature information for the docstring
    using cast_out = make_caster<
        std::conditional_t<std::is_void_v<Return>, void_type, Return>>;

    // Compile-time function signature
    static constexpr auto descr =
        const_name("(") +
        concat(type_descr(
            make_caster<remove_opt_mono_t<intrinsic_t<Args>>>::Name)...) +
        const_name(") -> ") + cast_out::Name;

    // std::type_info for all function arguments
    const std::type_info* descr_types[descr.type_count() + 1];
    descr.put_types(descr_types);

    // Auxiliary data structure to capture the provided function/closure
    struct capture {
        std::remove_reference_t<Func> f
