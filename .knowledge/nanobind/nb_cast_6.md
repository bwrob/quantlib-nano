                                            policy, nullptr);
    if (!h.is_valid())
        detail::raise_python_or_cast_error();

    return steal(h);
}

template <typename T>
object cast(T &&value, rv_policy policy, handle parent) {
    detail::cleanup_list cleanup(parent.ptr());
    handle h = detail::make_caster<T>::from_cpp((detail::forward_t<T>) value,
                                                policy, &cleanup);

    cleanup.release();

    if (!h.is_valid())
        detail::raise_python_or_cast_error();

    return steal(h);
}

template <typename T> object find(const T &value) noexcept {
    return steal(detail::make_caster<T>::from_cpp(value, rv_policy::none, nullptr));
}

template <rv_policy policy = rv_policy::automatic, typename... Args>
tuple make_tuple(Args &&...args) {
    tuple result = steal<tuple>(PyTuple_New((Py_ssize_t) sizeof...(Args)));

    size_t nargs = 0;
    PyObject *o = result.ptr();

    (NB_TUPLE_SET_ITEM(o, nargs++,
                       detail::make_caster<Args>::from_cpp(
                           (detail::forward_t<Args>) args, policy, nullptr)
                           .ptr()),
     ...);

    detail::tuple_check(o, sizeof...(Args));

    return result;
}

template <typename T> arg_v arg::operator=(T &&value) const {
    return arg_v(*this, cast((detail::forward_t<T>) value));
}
template <typename T> arg_locked_v arg_locked::operator=(T &&value) const {
    return arg_locked_v(*this, cast((detail::forward_t<T>) value));
}

template <typename Impl> template <typename T>
detail::accessor<Impl>& detail::accessor<Impl>::operator=(T &&value) {
    object result = cast((detail::forward_t<T>) value);
    Impl::set(m_base, m_key, result.ptr());
    return *this;
}

template <typename T> void list::append(T &&value) {
    object o = nanobind::cast((detail::forward_t<T>) value);
    if (PyList_Append(m_ptr, o.ptr()))
        raise_python_error();
}

template <typename T> void list::insert(Py_ssize_t index, T &&value) {
    object o = nanobind::cast((detail::forward_t<T>) value);
    if (PyList_Insert(m_ptr, index, o.ptr()))
        raise_python_error();
}

template <typename T> bool dict::contains(T&& key) const {
    object o = nanobind::cast((detail::forward_t<T>) key);
    int rv = PyDict_Contains(m_ptr, o.ptr());
    if (rv == -1)
        raise_python_error();
    return rv == 1;
}

template <typename T> bool set::contains(T&& key) const {
    object o = nanobind::cast((detail::forward_t<T>) key);
    int rv = PySet_Contains(m_ptr, o.ptr());
    if (rv == -1)
        raise_python_error();
    return rv == 1;
}

template <typename T> void set::add(T&& key) {
    object o = nanobind::cast((detail::forward_t<T>) key);
    int rv = PySet_Add(m_ptr, o.ptr());
    if (rv == -1)
        raise_python_error();
}

template <typename T> bool set::discard(T &&value) {
    object o = nanobind::cast((detail::forward_t<T>) value);
    int rv = PySet_Discard(m_ptr, o.ptr());
    if (rv < 0)
        raise_python_error();
    return rv == 1;
}

template <typename T> bool frozenset::contains(T&& key) const {
    object o = nanobind::cast((detail::forward_t<T>) key);
    int rv = PySet_Contains(m_ptr, o.ptr());
    if (rv == -1)
        raise_python_error();
    return rv == 1;
}

template <typename T> bool mapping::contains(T&& key) const {
    object o = nanobind::cast((detail::forward_t<T>) key);
    int rv = PyMapping_HasKey(m_ptr, o.ptr());
    if (rv == -1)
        raise_python_error();
    return rv == 1;
}

NAMESPACE_END(NB_NAMESPACE)