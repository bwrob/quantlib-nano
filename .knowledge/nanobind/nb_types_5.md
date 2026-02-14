 list items() const { return steal<list>(detail::obj_op_1(m_ptr, PyDict_Items)); }
    object get(handle key, handle def) const {
        PyObject *o = PyDict_GetItem(m_ptr, key.ptr());
        if (!o)
            o = def.ptr();
        return borrow(o);
    }
    object get(const char *key, handle def) const {
        PyObject *o = PyDict_GetItemString(m_ptr, key);
        if (!o)
            o = def.ptr();
        return borrow(o);
    }
    template <typename T> bool contains(T&& key) const;
    void clear() { PyDict_Clear(m_ptr); }
    void update(handle h) {
        if (PyDict_Update(m_ptr, h.ptr()))
            raise_python_error();
    }
    bool empty() const { return size() == 0; }
};

class set : public object {
    NB_OBJECT(set, object, "set", PySet_Check)
    set() : object(PySet_New(nullptr), detail::steal_t()) { }
    explicit set(handle h)
        : object(detail::set_from_obj(h.ptr()), detail::steal_t{}) { }
    size_t size() const { return (size_t) NB_SET_GET_SIZE(m_ptr); }
    template <typename T> bool contains(T&& key) const;
    template <typename T> void add(T &&value);
    void clear() {
        if (PySet_Clear(m_ptr))
            raise_python_error();
    }
    template <typename T> bool discard(T &&value);
    bool empty() const { return size() == 0; }
};

class frozenset : public object {
    NB_OBJECT(frozenset, object, "frozenset", PyFrozenSet_Check)
    frozenset() : object(PyFrozenSet_New(nullptr), detail::steal_t()) { }
    explicit frozenset(handle h)
        : object(detail::frozenset_from_obj(h.ptr()), detail::steal_t{}) { }
    size_t size() const { return (size_t) NB_SET_GET_SIZE(m_ptr); }
    template <typename T> bool contains(T&& key) const;
    bool empty() const { return size() == 0; }
};

class sequence : public object {
    NB_OBJECT_DEFAULT(sequence, object, "collections.abc.Sequence", PySequence_Check)
};

class mapping : public object {
    NB_OBJECT_DEFAULT(mapping, object, "collections.abc.Mapping", PyMapping_Check)
    list keys() const { return steal<list>(detail::obj_op_1(m_ptr, PyMapping_Keys)); }
    list values() const { return steal<list>(detail::obj_op_1(m_ptr, PyMapping_Values)); }
    list items() const { return steal<list>(detail::obj_op_1(m_ptr, PyMapping_Items)); }
    template <typename T> bool contains(T&& key) const;
};

class args : public tuple {
    NB_OBJECT_DEFAULT(args, tuple, "tuple", PyTuple_Check)
};

class kwargs : public dict {
    NB_OBJECT_DEFAULT(kwargs, dict, "dict", PyDict_Check)
};

class iterator : public object {
public:
    using difference_type = Py_ssize_t;
    using value_type = handle;
    using reference = const handle;
    using pointer = const handle *;

    NB_OBJECT_DEFAULT(iterator, object, "collections.abc.Iterator", PyIter_Check)

    iterator& operator++() {
        m_value = steal(detail::obj_iter_next(m_ptr));
        return *this;
    }

    iterator operator++(int) {
        iterator rv = *this;
        m_value = steal(detail::obj_iter_next(m_ptr));
        return rv;
    }

    handle operator*() const {
        if (is_valid() && !m_value.is_valid())
            m_value = steal(detail::obj_iter_next(m_ptr));
        return m_value;
    }

    pointer operator->() const { operator*(); return &m_value; }

    static iterator sentinel() { return {}; }

    friend bool operator==(const iterator &a, const iterator &b) { return a->ptr() == b->ptr(); }
    friend bool operator!=(const iterator &a, const iterator &b) { return a->ptr() != b->ptr(); }

private:
    mutable object m_value;
};

class iterable : public object {
public:
    NB_OBJECT_DEFAULT(iterable, object, "collections.abc.Iterable", detail::iterable_check)
};

/// Retrieve the Python type object associated with a C++ class
template <typename T> handle type() noexcept {
    return detail::nb_type_lookup(&typeid(detail::intrinsic_t<T>));
}

template <typename T>
NB_INLINE bool isinstance(handle h) noexcept {
    if constexpr (std::is_base_of_v<handle, T>)
        return
