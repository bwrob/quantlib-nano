tes", PyBytes_Check)

    explicit bytes(handle h)
        : object(detail::bytes_from_obj(h.ptr()), detail::steal_t{}) { }

    explicit bytes(const char *s)
        : object(detail::bytes_from_cstr(s), detail::steal_t{}) { }

    explicit bytes(const void *s, size_t n)
        : object(detail::bytes_from_cstr_and_size(s, n), detail::steal_t{}) { }

    const char *c_str() const { return PyBytes_AsString(m_ptr); }

    const void *data() const { return (const void *) PyBytes_AsString(m_ptr); }

    size_t size() const { return (size_t) PyBytes_Size(m_ptr); }
};

NAMESPACE_BEGIN(literals)
inline str operator""_s(const char *s, size_t n) {
    return str(s, n);
}
NAMESPACE_END(literals)

class bytearray : public object {
    NB_OBJECT(bytearray, object, "bytearray", PyByteArray_Check)

    bytearray()
        : object(PyObject_CallNoArgs((PyObject *)&PyByteArray_Type), detail::steal_t{}) { }

    explicit bytearray(handle h)
        : object(detail::bytearray_from_obj(h.ptr()), detail::steal_t{}) { }

    explicit bytearray(const void *s, size_t n)
        : object(detail::bytearray_from_cstr_and_size(s, n), detail::steal_t{}) { }

    const char *c_str() const { return PyByteArray_AsString(m_ptr); }

    const void *data() const { return PyByteArray_AsString(m_ptr); }
    void *data() { return PyByteArray_AsString(m_ptr); }

    size_t size() const { return (size_t) PyByteArray_Size(m_ptr); }

    void resize(size_t n) {
        if (PyByteArray_Resize(m_ptr, (Py_ssize_t) n) != 0)
            detail::raise_python_error();
    }
};

class tuple : public object {
    NB_OBJECT(tuple, object, "tuple", PyTuple_Check)
    tuple() : object(PyTuple_New(0), detail::steal_t()) { }
    explicit tuple(handle h)
        : object(detail::tuple_from_obj(h.ptr()), detail::steal_t{}) { }
    size_t size() const { return (size_t) NB_TUPLE_GET_SIZE(m_ptr); }
    template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>> = 1>
    detail::accessor<detail::num_item_tuple> operator[](T key) const;

#if !defined(Py_LIMITED_API) && !defined(PYPY_VERSION)
    detail::fast_iterator begin() const;
    detail::fast_iterator end() const;
#endif
    bool empty() const { return size() == 0; }
};

class type_object : public object {
    NB_OBJECT_DEFAULT(type_object, object, "type", PyType_Check)
};

class list : public object {
    NB_OBJECT(list, object, "list", PyList_Check)
    list() : object(PyList_New(0), detail::steal_t()) { }
    explicit list(handle h)
        : object(detail::list_from_obj(h.ptr()), detail::steal_t{}) { }
    size_t size() const { return (size_t) NB_LIST_GET_SIZE(m_ptr); }

    template <typename T> void append(T &&value);
    template <typename T> void insert(Py_ssize_t index, T &&value);

    template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>> = 1>
    detail::accessor<detail::num_item_list> operator[](T key) const;

    void clear() {
        if (PyList_SetSlice(m_ptr, 0, PY_SSIZE_T_MAX, nullptr))
            raise_python_error();
    }

    void extend(handle h) {
        if (PyList_SetSlice(m_ptr, PY_SSIZE_T_MAX, PY_SSIZE_T_MAX, h.ptr()))
            raise_python_error();
    }

    void sort() {
        if (PyList_Sort(m_ptr))
            raise_python_error();
    }

    void reverse() {
        if (PyList_Reverse(m_ptr))
            raise_python_error();
    }

#if !defined(Py_LIMITED_API) && !defined(PYPY_VERSION)
    detail::fast_iterator begin() const;
    detail::fast_iterator end() const;
#endif
    bool empty() const { return size() == 0; }
};

class dict : public object {
    NB_OBJECT(dict, object, "dict", PyDict_Check)
    dict() : object(PyDict_New(), detail::steal_t()) { }
    size_t size() const { return (size_t) NB_DICT_GET_SIZE(m_ptr); }
    detail::dict_iterator begin() const;
    detail::dict_iterator end() const;
    list keys() const { return steal<list>(detail::obj_op_1(m_ptr, PyDict_Keys)); }
    list values() const { return steal<list>(detail::obj_op_1(m_ptr, PyDict_Values)); }

