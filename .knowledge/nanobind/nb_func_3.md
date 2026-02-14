N32) && !defined(__CUDACC__) // temporary workaround for an internal compiler error in MSVC
            result = cast_out::from_cpp(
                       cap->func(static_cast<cast_t<Args>>(in.template get<Is>())...),
                       policy, cleanup).ptr();
#else
            result = cast_out::from_cpp(
                       cap->func((in.template get<Is>())
                                     .operator cast_t<Args>()...),
                       policy, cleanup).ptr();
#endif
        }

        if constexpr (Info::pre_post_hooks) {
            std::integral_constant<size_t, nargs> nargs_c;
            (process_postcall(args, nargs_c, result, (Extra *) nullptr), ...);
        }

        return result;
    };

    f.descr = descr.text;
    f.descr_types = descr_types;
    f.nargs = nargs;

    // Set nargs_pos to the number of C++ function parameters (Args...) that
    // can be filled from Python positional arguments in a one-to-one fashion.
    // This ends at:
    // - the location of the variadic *args parameter, if present; otherwise
    // - the location of the first keyword-only parameter, if any; otherwise
    // - the location of the variadic **kwargs parameter, if present; otherwise
    // - the end of the parameter list
    // It's correct to give *args priority over kw_only because we verified
    // above that kw_only comes afterward if both are present. It's correct
    // to give kw_only priority over **kwargs because we verified above that
    // kw_only comes before if both are present.
    f.nargs_pos =   args_pos_1 < nargs ? args_pos_1 :
                      explicit_kw_only ? nargs_before_kw_only :
                  kwargs_pos_1 < nargs ? kwargs_pos_1 : nargs;

    // Fill remaining fields of 'f'
    size_t arg_index = 0;
    (func_extra_apply(f, extra, arg_index), ...);

    (void) arg_index;

    return nb_func_new(&f);
}

NAMESPACE_END(detail)

// The initial template parameter to cpp_function/cpp_function_def is
// used by class_ to ensure that member pointers are treated as members
// of the class being defined; other users can safely leave it at its
// default of void.

template <typename = void, typename Return, typename... Args, typename... Extra>
NB_INLINE object cpp_function(Return (*f)(Args...), const Extra&... extra) {
    return steal(detail::func_create<true, true>(
        f, f, std::make_index_sequence<sizeof...(Args)>(), extra...));
}

template <typename = void, typename Return, typename... Args, typename... Extra>
NB_INLINE void cpp_function_def(Return (*f)(Args...), const Extra&... extra) {
    detail::func_create<false, true>(
        f, f, std::make_index_sequence<sizeof...(Args)>(), extra...);
}

/// Construct a cpp_function from a lambda function (pot. with internal state)
template <
    typename = void, typename Func, typename... Extra,
    detail::enable_if_t<detail::is_lambda_v<std::remove_reference_t<Func>>> = 0>
NB_INLINE object cpp_function(Func &&f, const Extra &...extra) {
    using am = detail::analyze_method<decltype(&std::remove_reference_t<Func>::operator())>;
    return steal(detail::func_create<true, true>(
        (detail::forward_t<Func>) f, (typename am::func *) nullptr,
        std::make_index_sequence<am::argc>(), extra...));
}

template <
    typename = void, typename Func, typename... Extra,
    detail::enable_if_t<detail::is_lambda_v<std::remove_reference_t<Func>>> = 0>
NB_INLINE void cpp_function_def(Func &&f, const Extra &...extra) {
    using am = detail::analyze_method<decltype(&std::remove_reference_t<Func>::operator())>;
    detail::func_create<false, true>(
        (detail::forward_t<Func>) f, (typename am::func *) nullptr,
        std::make_index_sequence<am::argc>(), extra...);
}

/// Construct a cpp_function from a class method (non-const)
template <typename Target = void,
          typename Return, typename Class, typename... Args, typename... Extra>
NB_INLINE object cpp_function(Return (Class::*f)(Args...), const Extra &...extra) {
    using