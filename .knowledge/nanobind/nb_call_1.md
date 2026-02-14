#  pragma warning(disable: 6255) // _alloca indicates failure by raising a stack overflow exception
#endif

class kwargs_proxy : public handle {
public:
    explicit kwargs_proxy(handle h) : handle(h) { }
};

class args_proxy : public handle {
public:
    explicit args_proxy(handle h) : handle(h) { }
    kwargs_proxy operator*() const { return kwargs_proxy(*this); }
};

template <typename Derived>
args_proxy api<Derived>::operator*() const {
    return args_proxy(derived().ptr());
}

/// Implementation detail of api<T>::operator() (call operator)
template <typename T>
NB_INLINE void call_analyze(size_t &nargs, size_t &nkwargs, const T &value) {
    using D = std::decay_t<T>;
    static_assert(!std::is_base_of_v<arg_locked, D>,
                  "nb::arg().lock() may be used only when defining functions, "
                  "not when calling them");

    if constexpr (std::is_same_v<D, arg_v>)
        nkwargs++;
    else if constexpr (std::is_same_v<D, args_proxy>)
        nargs += len(value);
    else if constexpr (std::is_same_v<D, kwargs_proxy>)
        nkwargs += len(value);
    else
        nargs += 1;

    (void) nargs; (void) nkwargs; (void) value;
}

/// Implementation detail of api<T>::operator() (call operator)
template <rv_policy policy, typename T>
NB_INLINE void call_init(PyObject **args, PyObject *kwnames, size_t &nargs,
                         size_t &nkwargs, const size_t kwargs_offset,
                         T &&value) {
    using D = std::decay_t<T>;

    if constexpr (std::is_same_v<D, arg_v>) {
        args[kwargs_offset + nkwargs] = value.value.release().ptr();
        NB_TUPLE_SET_ITEM(kwnames, nkwargs++,
                         PyUnicode_InternFromString(value.name_));
    } else if constexpr (std::is_same_v<D, args_proxy>) {
        for (size_t i = 0, l = len(value); i < l; ++i)
            args[nargs++] = borrow(value[i]).release().ptr();
    } else if constexpr (std::is_same_v<D, kwargs_proxy>) {
        PyObject *key, *entry;
        Py_ssize_t pos = 0;
#if defined(NB_FREE_THREADED)
        ft_object_guard guard(value);
#endif
        while (PyDict_Next(value.ptr(), &pos, &key, &entry)) {
            Py_INCREF(key); Py_INCREF(entry);
            args[kwargs_offset + nkwargs] = entry;
            NB_TUPLE_SET_ITEM(kwnames, nkwargs++, key);
        }
    } else {
        args[nargs++] =
            make_caster<T>::from_cpp((forward_t<T>) value, policy, nullptr).ptr();
    }
    (void) args; (void) kwnames; (void) nargs;
    (void) nkwargs; (void) kwargs_offset;
}

#define NB_DO_VECTORCALL()                                                     \
    PyObject *base, **args_p;                                                  \
    if constexpr (method_call) {                                               \
        base = derived().key().release().ptr();                                \
        args[0] = derived().base().inc_ref().ptr();                            \
        args_p = args;                                                         \
        nargs++;                                                               \
    } else {                                                                   \
        base = derived().inc_ref().ptr();                                      \
        args[0] = nullptr;                                                     \
        args_p = args + 1;                                                     \
    }                                                                          \
    nargs |= PY_VECTORCALL_ARGUMENTS_OFFSET;                                   \
    return steal(obj_vectorcall(base, args_p, nargs, kwnames, method_call))

template <typename Derived>
template <rv_policy policy, typename... Args>
object api<Derived>::operator()(Args &&...args_) const {
    static constexpr bool method_call =
        std::is_same_v<Derived, accessor<obj_attr>> ||
        std::is_same_v<Derived, accessor<str_attr>>;

    if constexpr (((std::is_same_v<Args, arg_v> ||
  