handle::operator=;
    handle_t(const handle &h) : handle(h) { }

    static bool check_(handle h) { return isinstance<T>(h); }
};

struct fallback : public handle {
public:
    static constexpr auto Name = detail::const_name("object");

    using handle::handle;
    using handle::operator=;
    fallback(const handle &h) : handle(h) { }
};

template <typename T> class type_object_t : public type_object {
public:
    static constexpr auto Name = detail::const_name("type[") +
                                 detail::make_caster<T>::Name +
                                 detail::const_name("]");

    using type_object::type_object;
    using type_object::operator=;

    static bool check_(handle h) {
        return PyType_Check(h.ptr()) &&
               PyType_IsSubtype((PyTypeObject *) h.ptr(),
                                (PyTypeObject *) nanobind::type<T>().ptr());
    }
};

template <typename T, typename...> class typed : public T {
public:
    constexpr static bool nb_typed = true;
    using T::T;
    using T::operator=;
    typed(const T& o) : T(o) {}
    typed(T&& o) : T(std::move(o)) {}
};

template <typename T> struct pointer_and_handle {
    T *p;
    handle h;
};

NAMESPACE_BEGIN(detail)
template <typename Derived> NB_INLINE api<Derived>::operator handle() const {
    return derived().ptr();
}

template <typename Derived> NB_INLINE handle api<Derived>::type() const {
    return (PyObject *) Py_TYPE(derived().ptr());
}

template <typename Derived> NB_INLINE handle api<Derived>::inc_ref() const & {
    return operator handle().inc_ref();
}

template <typename Derived> NB_INLINE handle api<Derived>::dec_ref() const & {
    return operator handle().dec_ref();
}

template <typename Derived>
NB_INLINE bool api<Derived>::is(handle value) const {
    return derived().ptr() == value.ptr();
}

template <typename Derived> iterator api<Derived>::begin() const {
    return iter(*this);
}

template <typename Derived> iterator api<Derived>::end() const {
    return iterator::sentinel();
}

struct fast_iterator {
    using value_type = handle;
    using reference = const value_type;
    using difference_type = std::ptrdiff_t;

    fast_iterator() = default;
    fast_iterator(PyObject **value) : value(value) { }

    fast_iterator& operator++() { value++; return *this; }
    fast_iterator operator++(int) { fast_iterator rv = *this; value++; return rv; }
    friend bool operator==(const fast_iterator &a, const fast_iterator &b) { return a.value == b.value; }
    friend bool operator!=(const fast_iterator &a, const fast_iterator &b) { return a.value != b.value; }

    handle operator*() const { return *value; }

    PyObject **value;
};

class dict_iterator {
public:
    NB_NONCOPYABLE(dict_iterator)

    using value_type = std::pair<handle, handle>;
    using reference = const value_type;

    dict_iterator() = default;
    dict_iterator(handle h) : h(h), pos(0) {
#if defined(NB_FREE_THREADED)
        PyCriticalSection_Begin(&cs, h.ptr());
#endif
        increment();
    }

#if defined(NB_FREE_THREADED)
    ~dict_iterator() {
        if (h.ptr())
            PyCriticalSection_End(&cs);
    }
#endif

    dict_iterator& operator++() {
        increment();
        return *this;
    }

    void increment() {
        if (PyDict_Next(h.ptr(), &pos, &key, &value) == 0)
            pos = -1;
    }

    value_type operator*() const { return { key, value }; }

    friend bool operator==(const dict_iterator &a, const dict_iterator &b) { return a.pos == b.pos; }
    friend bool operator!=(const dict_iterator &a, const dict_iterator &b) { return a.pos != b.pos; }

private:
    handle h;
    Py_ssize_t pos = -1;
    PyObject *key = nullptr;
    PyObject *value = nullptr;
#if defined(NB_FREE_THREADED)
    PyCriticalSection cs { };
#endif
};

NB_IMPL_COMP(equal,      Py_EQ)
NB_IMPL_COMP(not_equal,  Py_NE)
NB_IMPL_COMP(operator<,  Py_LT)
NB_IMPL_COMP(operator<=, Py_LE)
NB_IMPL_COMP(operator>,  Py_GT)
NB_IMPL_COMP(operator>=, Py_GE)
NB_IMPL_OP_1(ope
