T::check_(h);
    else if constexpr (detail::is_base_caster_v<detail::make_caster<T>>)
        return detail::nb_type_isinstance(h.ptr(), &typeid(detail::intrinsic_t<T>));
    else
        return detail::make_caster<T>().from_python(h, 0, nullptr);
}

NB_INLINE bool issubclass(handle h1, handle h2) {
    return detail::issubclass(h1.ptr(), h2.ptr());
}

NB_INLINE str repr(handle h) { return steal<str>(detail::obj_repr(h.ptr())); }
NB_INLINE size_t len(handle h) { return detail::obj_len(h.ptr()); }
NB_INLINE size_t len_hint(handle h) { return detail::obj_len_hint(h.ptr()); }
NB_INLINE size_t len(const tuple &t) { return (size_t) NB_TUPLE_GET_SIZE(t.ptr()); }
NB_INLINE size_t len(const list &l) { return (size_t) NB_LIST_GET_SIZE(l.ptr()); }
NB_INLINE size_t len(const dict &d) { return (size_t) NB_DICT_GET_SIZE(d.ptr()); }
NB_INLINE size_t len(const set &d) { return (size_t) NB_SET_GET_SIZE(d.ptr()); }

inline void print(handle value, handle end = handle(), handle file = handle()) {
    detail::print(value.ptr(), end.ptr(), file.ptr());
}

inline void print(const char *str, handle end = handle(), handle file = handle()) {
    print(nanobind::str(str), end, file);
}

inline object none() { return borrow(Py_None); }
inline dict builtins() { return borrow<dict>(PyEval_GetBuiltins()); }

inline iterator iter(handle h) {
    return steal<iterator>(detail::obj_iter(h.ptr()));
}

class slice : public object {
public:
    NB_OBJECT_DEFAULT(slice, object, "slice", PySlice_Check)
    slice(handle start, handle stop, handle step) {
        m_ptr = PySlice_New(start.ptr(), stop.ptr(), step.ptr());
        if (!m_ptr)
            raise_python_error();
    }

    template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>> = 0>
    explicit slice(T stop) : slice(Py_None, int_(stop), Py_None) {}
    template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>> = 0>
    slice(T start, T stop) : slice(int_(start), int_(stop), Py_None) {}
    template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>> = 0>
    slice(T start, T stop, T step) : slice(int_(start), int_(stop), int_(step)) {}

    detail::tuple<Py_ssize_t, Py_ssize_t, Py_ssize_t, size_t> compute(size_t size) const {
        Py_ssize_t start, stop, step;
        size_t slice_length;
        detail::slice_compute(m_ptr, (Py_ssize_t) size, start, stop, step, slice_length);
        return detail::tuple(start, stop, step, slice_length);
    }
};

class memoryview : public object {
    NB_OBJECT(memoryview, object, "memoryview", PyMemoryView_Check)
    explicit memoryview(handle h)
        : object(detail::memoryview_from_obj(h.ptr()), detail::steal_t{}) { }
};

class ellipsis : public object {
    static bool is_ellipsis(PyObject *obj) { return obj == Py_Ellipsis; }

public:
    NB_OBJECT(ellipsis, object, "types.EllipsisType", is_ellipsis)
    ellipsis() : object(Py_Ellipsis, detail::borrow_t()) {}
};

class not_implemented : public object {
    static bool is_not_implemented(PyObject *obj) { return obj == Py_NotImplemented; }

public:
    NB_OBJECT(not_implemented, object, "types.NotImplementedType", is_not_implemented)
    not_implemented() : object(Py_NotImplemented, detail::borrow_t()) {}
};

class callable : public object {
public:
    NB_OBJECT(callable, object, "collections.abc.Callable", PyCallable_Check)
    using object::object;
};

class weakref : public object {
public:
    NB_OBJECT(weakref, object, "weakref.ReferenceType", PyWeakref_Check)

    explicit weakref(handle obj, handle callback = {})
        : object(PyWeakref_NewRef(obj.ptr(), callback.ptr()), detail::steal_t{}) {
        if (!m_ptr)
            raise_python_error();
    }
};

class any : public object {
public:
    using object::object;
    using object::operator=;
    static constexpr auto Name = detail::const_name("typing.Any");
};

template <typename T> class handle_t : public handle {
public:
    static constexpr auto Name = detail::make_caster<T>::Name;

    using handle::handle;
    using 