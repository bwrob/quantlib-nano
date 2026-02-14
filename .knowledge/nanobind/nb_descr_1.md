urn {}; }
constexpr descr<0> concat_maybe() { return {}; }

template <size_t N, typename... Ts>
constexpr descr<N, Ts...> concat(const descr<N, Ts...> &descr) { return descr; }

template <size_t N, typename... Ts>
constexpr descr<N, Ts...> concat_maybe(const descr<N, Ts...> &descr) { return descr; }

template <size_t N, typename... Ts, typename... Args>
constexpr auto concat(const descr<N, Ts...> &d, const Args &...args)
    -> decltype(std::declval<descr<N + 2, Ts...>>() + concat(args...)) {
    return d + const_name(", ") + concat(args...);
}

template <typename... Args>
constexpr auto concat_maybe(const descr<0> &, const descr<0> &, const Args &...args)
    -> decltype(concat_maybe(args...)) { return concat_maybe(args...); }

template <size_t N, typename... Ts, typename... Args>
constexpr auto concat_maybe(const descr<0> &, const descr<N, Ts...> &arg, const Args &...args)
    -> decltype(concat_maybe(arg, args...)) { return concat_maybe(arg, args...); }

template <size_t N, typename... Ts, typename... Args>
constexpr auto concat_maybe(const descr<N, Ts...> &arg, const descr<0> &, const Args &...args)
    -> decltype(concat_maybe(arg, args...)) { return concat_maybe(arg, args...); }

template <size_t N, size_t N2, typename... Ts, typename... Ts2, typename... Args,
          enable_if_t<N != 0 && N2 != 0> = 0>
constexpr auto concat_maybe(const descr<N, Ts...> &arg0, const descr<N2, Ts2...> &arg1, const Args &...args)
    -> decltype(concat(arg0, concat_maybe(arg1, args...))) {
    return concat(arg0, concat_maybe(arg1, args...));
}

template <size_t N, typename... Ts>
constexpr descr<N + 2, Ts...> type_descr(const descr<N, Ts...> &descr) {
    return const_name("{") + descr + const_name("}");
}

NAMESPACE_END(detail)
NAMESPACE_END(NB_NAMESPACE)
