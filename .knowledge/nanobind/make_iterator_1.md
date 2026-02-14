}));
}

NAMESPACE_END(detail)

/// Makes a python iterator from a first and past-the-end C++ InputIterator.
template <rv_policy Policy = rv_policy::automatic_reference,
          typename Iterator,
          typename Sentinel,
          typename ValueType = typename detail::iterator_access<Iterator>::result_type,
          typename... Extra,
          typename = decltype(std::declval<Iterator>() == std::declval<Sentinel>())>
auto make_iterator(handle scope, const char *name, Iterator first, Sentinel last, Extra &&...extra) {
    return detail::make_iterator_impl<detail::iterator_access<Iterator>, Policy,
                                      Iterator, Sentinel, ValueType, Extra...>(
        scope, name, std::forward<Iterator>(first),
        std::forward<Sentinel>(last), std::forward<Extra>(extra)...);
}

/// Makes an iterator over the keys (`.first`) of a iterator over pairs from a
/// first and past-the-end InputIterator.
template <rv_policy Policy = rv_policy::automatic_reference, typename Iterator,
          typename Sentinel,
          typename KeyType =
              typename detail::iterator_key_access<Iterator>::result_type,
          typename... Extra>
auto make_key_iterator(handle scope, const char *name, Iterator first,
                       Sentinel last, Extra &&...extra) {
    return detail::make_iterator_impl<detail::iterator_key_access<Iterator>,
                                      Policy, Iterator, Sentinel, KeyType,
                                      Extra...>(
        scope, name, std::forward<Iterator>(first),
        std::forward<Sentinel>(last), std::forward<Extra>(extra)...);
}

/// Makes an iterator over the values (`.second`) of a iterator over pairs from a
/// first and past-the-end InputIterator.
template <rv_policy Policy = rv_policy::automatic_reference,
          typename Iterator,
          typename Sentinel,
          typename ValueType = typename detail::iterator_value_access<Iterator>::result_type,
          typename... Extra>
auto make_value_iterator(handle scope, const char *name, Iterator first, Sentinel last, Extra &&...extra) {
    return detail::make_iterator_impl<detail::iterator_value_access<Iterator>,
                                      Policy, Iterator, Sentinel, ValueType,
                                      Extra...>(
        scope, name, std::forward<Iterator>(first),
        std::forward<Sentinel>(last), std::forward<Extra>(extra)...);
}

/// Makes an iterator over values of a container supporting `std::begin()`/`std::end()`
template <rv_policy Policy = rv_policy::automatic_reference,
          typename Type,
          typename... Extra,
          typename = decltype(std::begin(std::declval<Type&>()))>
auto make_iterator(handle scope, const char *name, Type &value, Extra &&...extra) {
    return make_iterator<Policy>(scope, name, std::begin(value),
                                 std::end(value),
                                 std::forward<Extra>(extra)...);
}

NAMESPACE_END(NB_NAMESPACE)
