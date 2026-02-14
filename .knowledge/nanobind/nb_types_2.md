lic detail::api<handle> {
    friend class python_error;
    friend struct detail::str_attr;
    friend struct detail::obj_attr;
    friend struct detail::str_item;
    friend struct detail::obj_item;
    friend struct detail::num_item;
public:
    static constexpr auto Name = detail::const_name("object");

    handle() = default;
    handle(const handle &) = default;
    handle(handle &&) noexcept = default;
    handle &operator=(const handle &) = default;
    handle &operator=(handle &&) noexcept = default;
    NB_INLINE handle(std::nullptr_t, detail::steal_t) : m_ptr(nullptr) { }
    NB_INLINE handle(std::nullptr_t) : m_ptr(nullptr) { }
    NB_INLINE handle(const PyObject *ptr) : m_ptr((PyObject *) ptr) { }
    NB_INLINE handle(const PyTypeObject *ptr) : m_ptr((PyObject *) ptr) { }

    const handle& inc_ref() const & noexcept {
#if defined(NDEBUG)
        Py_XINCREF(m_ptr);
#else
        detail::incref_checked(m_ptr);
#endif
        return *this;
    }

    const handle& dec_ref() const & noexcept {
#if defined(NDEBUG)
        Py_XDECREF(m_ptr);
#else
        detail::decref_checked(m_ptr);
#endif
        return *this;
    }

    NB_INLINE explicit operator bool() const { return m_ptr != nullptr; }
    NB_INLINE PyObject *ptr() const { return m_ptr; }
    NB_INLINE static bool check_(handle) { return true; }

protected:
    PyObject *m_ptr = nullptr;
};

class object : public handle {
public:
    static constexpr auto Name = detail::const_name("object");

    object() = default;
    object(const object &o) : handle(o) { inc_ref(); }
    object(object &&o) noexcept : handle(o) { o.m_ptr = nullptr; }
    ~object() { dec_ref(); }
    object(handle h, detail::borrow_t) : handle(h) { inc_ref(); }
    object(handle h, detail::steal_t) : handle(h) { }

    handle release() {
      handle temp(m_ptr);
      m_ptr = nullptr;
      return temp;
    }

    void reset() {
        dec_ref();
        m_ptr = nullptr;
    }

    object& operator=(const object &o) {
        handle temp(m_ptr);
        o.inc_ref();
        m_ptr = o.m_ptr;
        temp.dec_ref();
        return *this;
    }

    object& operator=(object &&o) noexcept {
        handle temp(m_ptr);
        m_ptr = o.m_ptr;
        o.m_ptr = nullptr;
        temp.dec_ref();
        return *this;
    }

    NB_IMPL_OP_2_IO(operator+=)
    NB_IMPL_OP_2_IO(operator%=)
    NB_IMPL_OP_2_IO(operator-=)
    NB_IMPL_OP_2_IO(operator*=)
    NB_IMPL_OP_2_IO(operator/=)
    NB_IMPL_OP_2_IO(operator|=)
    NB_IMPL_OP_2_IO(operator&=)
    NB_IMPL_OP_2_IO(operator^=)
    NB_IMPL_OP_2_IO(operator<<=)
    NB_IMPL_OP_2_IO(operator>>=)
};

template <typename T> NB_INLINE T borrow(handle h) {
    return { h, detail::borrow_t() };
}

template <typename T = object, typename T2,
          std::enable_if_t<std::is_base_of_v<object, T2> && !std::is_lvalue_reference_v<T2>, int> = 0>
NB_INLINE T borrow(T2 &&o) {
    return { o.release(), detail::steal_t() };
}

template <typename T> NB_INLINE T steal(handle h) {
    return { h, detail::steal_t() };
}

inline bool hasattr(handle h, const char *key) noexcept {
    return PyObject_HasAttrString(h.ptr(), key);
}

inline bool hasattr(handle h, handle key) noexcept {
    return PyObject_HasAttr(h.ptr(), key.ptr());
}

inline object getattr(handle h, const char *key) {
    return steal(detail::getattr(h.ptr(), key));
}

inline object getattr(handle h, handle key) {
    return steal(detail::getattr(h.ptr(), key.ptr()));
}

inline object getattr(handle h, const char *key, handle def) noexcept {
    return steal(detail::getattr(h.ptr(), key, def.ptr()));
}

inline object getattr(handle h, handle key, handle value) noexcept {
    return steal(detail::getattr(h.ptr(), key.ptr(), value.ptr()));
}

inline void setattr(handle h, const char *key, handle value) {
    detail::setattr(h.ptr(), key, value.ptr());
}

inline void setattr(handle h, handle key, handle value) {
    detail::setattr(h.ptr(), key.ptr(), value.ptr());
}

inline void delattr(handle h, const char *k