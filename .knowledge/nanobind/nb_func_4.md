 T = std::conditional_t<std::is_void_v<Target>, Class, Target>;
    return steal(detail::func_create<true, true>(
        [f](T *c, Args... args) NB_INLINE_LAMBDA -> Return {
            return (c->*f)((detail::forward_t<Args>) args...);
        },
        (Return(*)(T *, Args...)) nullptr,
        std::make_index_sequence<sizeof...(Args) + 1>(), extra...));
}

template <typename Target = void,
          typename Return, typename Class, typename... Args, typename... Extra>
NB_INLINE void cpp_function_def(Return (Class::*f)(Args...), const Extra &...extra) {
    using T = std::conditional_t<std::is_void_v<Target>, Class, Target>;
    detail::func_create<false, true>(
        [f](T *c, Args... args) NB_INLINE_LAMBDA -> Return {
            return (c->*f)((detail::forward_t<Args>) args...);
        },
        (Return(*)(T *, Args...)) nullptr,
        std::make_index_sequence<sizeof...(Args) + 1>(), extra...);
}

/// Construct a cpp_function from a class method (const)
template <typename Target = void,
          typename Return, typename Class, typename... Args, typename... Extra>
NB_INLINE object cpp_function(Return (Class::*f)(Args...) const, const Extra &...extra) {
    using T = std::conditional_t<std::is_void_v<Target>, Class, Target>;
    return steal(detail::func_create<true, true>(
        [f](const T *c, Args... args) NB_INLINE_LAMBDA -> Return {
            return (c->*f)((detail::forward_t<Args>) args...);
        },
        (Return(*)(const T *, Args...)) nullptr,
        std::make_index_sequence<sizeof...(Args) + 1>(), extra...));
}

template <typename Target = void,
          typename Return, typename Class, typename... Args, typename... Extra>
NB_INLINE void cpp_function_def(Return (Class::*f)(Args...) const, const Extra &...extra) {
    using T = std::conditional_t<std::is_void_v<Target>, Class, Target>;
    detail::func_create<false, true>(
        [f](const T *c, Args... args) NB_INLINE_LAMBDA -> Return {
            return (c->*f)((detail::forward_t<Args>) args...);
        },
        (Return(*)(const T *, Args...)) nullptr,
        std::make_index_sequence<sizeof...(Args) + 1>(), extra...);
}

template <typename Func, typename... Extra>
module_ &module_::def(const char *name_, Func &&f, const Extra &...extra) {
    cpp_function_def((detail::forward_t<Func>) f, scope(*this),
                     name(name_), extra...);
    return *this;
}

NAMESPACE_END(NB_NAMESPACE)