PyObject *obj, handle key, PyObject **cache) {
        detail::getitem_or_raise(obj, key.ptr(), cache);
    }

    NB_INLINE static void set(PyObject *obj, handle key, PyObject *v) {
        setitem(obj, key.ptr(), v);
    }

    NB_INLINE static void del(PyObject *obj, handle key) {
        delitem(obj, key.ptr());
    }
};

struct num_item {
    static constexpr bool cache_dec_ref = true;
    using key_type = Py_ssize_t;

    NB_INLINE static void get(PyObject *obj, Py_ssize_t index, PyObject **cache) {
        detail::getitem_or_raise(obj, index, cache);
    }

    NB_INLINE static void set(PyObject *obj, Py_ssize_t index, PyObject *v) {
        setitem(obj, index, v);
    }

    NB_INLINE static void del(PyObject *obj, Py_ssize_t index) {
        delitem(obj, index);
    }
};

struct num_item_list {
    #if defined(Py_GIL_DISABLED)
          static constexpr bool cache_dec_ref = true;
    #else
          static constexpr bool cache_dec_ref = false;
    #endif

    using key_type = Py_ssize_t;

    NB_INLINE static void get(PyObject *obj, Py_ssize_t index, PyObject **cache) {
        #if defined(Py_GIL_DISABLED)
            *cache = PyList_GetItemRef(obj, index);
        #else
            *cache = NB_LIST_GET_ITEM(obj, index);
        #endif
    }

    NB_INLINE static void set(PyObject *obj, Py_ssize_t index, PyObject *v) {
#if defined(Py_LIMITED_API) || defined(NB_FREE_THREADED)
        Py_INCREF(v);
        PyList_SetItem(obj, index, v);
#else
        PyObject *old = NB_LIST_GET_ITEM(obj, index);
        Py_INCREF(v);
        NB_LIST_SET_ITEM(obj, index, v);
        Py_DECREF(old);
#endif
    }

    NB_INLINE static void del(PyObject *obj, Py_ssize_t index) {
        delitem(obj, index);
    }
};

struct num_item_tuple {
    static constexpr bool cache_dec_ref = false;
    using key_type = Py_ssize_t;

    NB_INLINE static void get(PyObject *obj, Py_ssize_t index, PyObject **cache) {
        *cache = NB_TUPLE_GET_ITEM(obj, index);
    }

    template <typename...Ts> static void set(Ts...) {
        static_assert(false_v<Ts...>, "tuples are immutable!");
    }
};

template <typename D> accessor<obj_attr> api<D>::attr(handle key) const {
    return { derived(), borrow(key) };
}

template <typename D> accessor<str_attr> api<D>::attr(const char *key) const {
    return { derived(), key };
}

template <typename D> accessor<str_attr> api<D>::doc() const {
    return { derived(), "__doc__" };
}

template <typename D> accessor<obj_item> api<D>::operator[](handle key) const {
    return { derived(), borrow(key) };
}

template <typename D> accessor<str_item> api<D>::operator[](const char *key) const {
    return { derived(), key };
}

template <typename D>
template <typename T, enable_if_t<std::is_arithmetic_v<T>>>
accessor<num_item> api<D>::operator[](T index) const {
    return { derived(), (Py_ssize_t) index };
}

NB_IMPL_ACCESSOR_OP_I(operator+=, PyNumber_InPlaceAdd)
NB_IMPL_ACCESSOR_OP_I(operator%=, PyNumber_InPlaceRemainder)
NB_IMPL_ACCESSOR_OP_I(operator-=, PyNumber_InPlaceSubtract)
NB_IMPL_ACCESSOR_OP_I(operator*=, PyNumber_InPlaceMultiply)
NB_IMPL_ACCESSOR_OP_I(operator/=, PyNumber_InPlaceTrueDivide)
NB_IMPL_ACCESSOR_OP_I(operator|=, PyNumber_InPlaceOr)
NB_IMPL_ACCESSOR_OP_I(operator&=, PyNumber_InPlaceAnd)
NB_IMPL_ACCESSOR_OP_I(operator^=, PyNumber_InPlaceXor)
NB_IMPL_ACCESSOR_OP_I(operator<<=,PyNumber_InPlaceLshift)
NB_IMPL_ACCESSOR_OP_I(operator>>=,PyNumber_InPlaceRshift)

NAMESPACE_END(detail)

template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>>>
detail::accessor<detail::num_item_list> list::operator[](T index) const {
    return { derived(), (Py_ssize_t) index };
}

template <typename T, detail::enable_if_t<std::is_arithmetic_v<T>>>
detail::accessor<detail::num_item_tuple> tuple::operator[](T index) const {
    return { derived(), (Py_ssize_t) index };
}

template <typename... Args> str str::format(Args&&... args) const {
    return steal<str>(
        derived().attr("format")((detail::forward_t<Args>)
