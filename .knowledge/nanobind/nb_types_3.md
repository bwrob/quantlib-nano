ey) {
    detail::delattr(h.ptr(), key);
}

inline void delattr(handle h, handle key) {
    detail::delattr(h.ptr(), key.ptr());
}

class module_ : public object {
public:
    NB_OBJECT(module_, object, "types.ModuleType", PyModule_CheckExact)

    template <typename Func, typename... Extra>
    module_ &def(const char *name_, Func &&f, const Extra &...extra);

    static NB_INLINE module_ import_(const char *name) {
        return steal<module_>(detail::module_import(name));
    }

    static NB_INLINE module_ import_(handle name) {
        return steal<module_>(detail::module_import(name.ptr()));
    }

    NB_INLINE module_ def_submodule(const char *name,
                                    const char *doc = nullptr) {
        return steal<module_>(detail::module_new_submodule(m_ptr, name, doc));
    }
};

class capsule : public object {
    NB_OBJECT_DEFAULT(capsule, object, NB_TYPING_CAPSULE, PyCapsule_CheckExact)

    capsule(const void *ptr, void (*cleanup)(void *) noexcept = nullptr) {
        m_ptr = detail::capsule_new(ptr, nullptr, cleanup);
    }

    capsule(const void *ptr, const char *name,
            void (*cleanup)(void *) noexcept = nullptr) {
        m_ptr = detail::capsule_new(ptr, name, cleanup);
    }

    const char *name() const { return PyCapsule_GetName(m_ptr); }

    void *data() const { return PyCapsule_GetPointer(m_ptr, name()); }
    void *data(const char *name) const {
        void *p = PyCapsule_GetPointer(m_ptr, name);
        if (!p && PyErr_Occurred())
            raise_python_error();
        return p;
    }
};

class bool_ : public object {
    NB_OBJECT_DEFAULT(bool_, object, "bool", PyBool_Check)

    explicit bool_(handle h)
        : object(detail::bool_from_obj(h.ptr()), detail::borrow_t{}) { }

    explicit bool_(bool value)
        : object(value ? Py_True : Py_False, detail::borrow_t{}) { }

    explicit operator bool() const {
        return m_ptr == Py_True;
    }
};

class int_ : public object {
    NB_OBJECT_DEFAULT(int_, object, "int", PyLong_Check)

    explicit int_(handle h)
        : object(detail::int_from_obj(h.ptr()), detail::steal_t{}) { }

    template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>> = 0>
    explicit int_(T value) {
        if constexpr (std::is_floating_point_v<T>)
            m_ptr = PyLong_FromDouble((double) value);
        else
            m_ptr = detail::type_caster<T>::from_cpp(value, rv_policy::copy, nullptr).ptr();

        if (!m_ptr)
            raise_python_error();
    }

    template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>> = 0>
    explicit operator T() const {
        detail::type_caster<T> tc;
        if (!tc.from_python(m_ptr, 0, nullptr))
            throw std::out_of_range("Conversion of nanobind::int_ failed");
        return tc.value;
    }
};

class float_ : public object {
    NB_OBJECT_DEFAULT(float_, object, "float", PyFloat_Check)

    explicit float_(handle h)
        : object(detail::float_from_obj(h.ptr()), detail::steal_t{}) { }

    explicit float_(double value)
        : object(PyFloat_FromDouble(value), detail::steal_t{}) {
        if (!m_ptr)
            raise_python_error();
    }

#if !defined(Py_LIMITED_API)
    explicit operator double() const { return PyFloat_AS_DOUBLE(m_ptr); }
#else
    explicit operator double() const { return PyFloat_AsDouble(m_ptr); }
#endif
};

class str : public object {
    NB_OBJECT_DEFAULT(str, object, "str", PyUnicode_Check)

    explicit str(handle h)
        : object(detail::str_from_obj(h.ptr()), detail::steal_t{}) { }

    explicit str(const char *s)
        : object(detail::str_from_cstr(s), detail::steal_t{}) { }

    explicit str(const char *s, size_t n)
        : object(detail::str_from_cstr_and_size(s, n), detail::steal_t{}) { }

    template <typename... Args> str format(Args&&... args) const;

    const char *c_str() const { return PyUnicode_AsUTF8AndSize(m_ptr, nullptr); }
};

class bytes : public object {
    NB_OBJECT_DEFAULT(bytes, object, "by
