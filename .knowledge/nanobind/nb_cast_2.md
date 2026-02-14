8)
                    return detail::load_u64(src.ptr(), flags, (uint64_t *) &value);
                else if constexpr (sizeof(T) == 4)
                    return detail::load_u32(src.ptr(), flags, (uint32_t *) &value);
                else if constexpr (sizeof(T) == 2)
                    return detail::load_u16(src.ptr(), flags, (uint16_t *) &value);
                else
                    return detail::load_u8(src.ptr(), flags, (uint8_t *) &value);
            }
        }
    }

    NB_INLINE static handle from_cpp(T src, rv_policy, cleanup_list *) noexcept {
        if constexpr (std::is_floating_point_v<T>) {
            return PyFloat_FromDouble((double) src);
        } else {
            if constexpr (std::is_signed_v<T>) {
                if constexpr (sizeof(T) <= sizeof(long))
                    return PyLong_FromLong((long) src);
                else
                    return PyLong_FromLongLong((long long) src);
            } else {
                if constexpr (sizeof(T) <= sizeof(unsigned long))
                    return PyLong_FromUnsignedLong((unsigned long) src);
                else
                    return PyLong_FromUnsignedLongLong((unsigned long long) src);
            }
        }
    }

    NB_TYPE_CASTER(T, const_name<std::is_integral_v<T>>("int", "float"))
};

template <typename T>
struct type_caster<T, enable_if_t<std::is_enum_v<T>>> {
    NB_INLINE bool from_python(handle src, uint8_t flags, cleanup_list *) noexcept {
        int64_t result;
        bool rv = enum_from_python(&typeid(T), src.ptr(), &result, flags);
        value = (T) result;
        return rv;
    }

    NB_INLINE static handle from_cpp(T src, rv_policy, cleanup_list *) noexcept {
        return enum_from_cpp(&typeid(T), (int64_t) src);
    }

    NB_TYPE_CASTER(T, const_name<T>())
};

template <> struct type_caster<void_type> {
    static constexpr auto Name = const_name("None");
};

template <> struct type_caster<void> {
    template <typename T_> using Cast = void *;
    template <typename T_> static constexpr bool can_cast() { return true; }
    using Value = void*;
    static constexpr auto Name = const_name(NB_TYPING_CAPSULE);
    explicit operator void *() { return value; }
    Value value;

    bool from_python(handle src, uint8_t, cleanup_list *) noexcept {
        if (src.is_none()) {
            value = nullptr;
            return true;
        } else {
            value = PyCapsule_GetPointer(src.ptr(), "nb_handle");
            if (!value) {
                PyErr_Clear();
                return false;
            }
            return true;
        }
    }

    static handle from_cpp(void *ptr, rv_policy, cleanup_list *) noexcept {
        if (ptr)
            return PyCapsule_New(ptr, "nb_handle", nullptr);
        else
            return none().release();
    }
};

template <typename T> struct none_caster {
    bool from_python(handle src, uint8_t, cleanup_list *) noexcept {
        if (src.is_none())
            return true;
        return false;
    }

    static handle from_cpp(T, rv_policy, cleanup_list *) noexcept {
        return none().release();
    }

    NB_TYPE_CASTER(T, const_name("None"))
};

template <> struct type_caster<std::nullptr_t> : none_caster<std::nullptr_t> { };

template <> struct type_caster<bool> {
    bool from_python(handle src, uint8_t, cleanup_list *) noexcept {
        if (src.ptr() == Py_True) {
            value = true;
            return true;
        } else if (src.ptr() == Py_False) {
            value = false;
            return true;
        } else {
            return false;
        }
    }

    static handle from_cpp(bool src, rv_policy, cleanup_list *) noexcept {
        return handle(src ? Py_True : Py_False).inc_ref();
    }

    NB_TYPE_CASTER(bool, const_name("bool"))
};

template <> struct type_caster<char> {
    using Value = const char *;
    Value value;
    Py_ssize_t size;
    static constexpr auto Name = const_name("str");
    template <typename T_>
    usin