g Cast = std::conditional_t<is_pointer_v<T_>, const char *, char>;

    bool from_python(handle src, uint8_t, cleanup_list *) noexcept {
        value = PyUnicode_AsUTF8AndSize(src.ptr(), &size);
        if (!value) {
            PyErr_Clear();
            return false;
        }
        return true;
    }

    static handle from_cpp(const char *value, rv_policy,
                           cleanup_list *) noexcept {
        if (value == nullptr) {
            PyObject* result = Py_None;
            Py_INCREF(result);
            return result;
        }
        return PyUnicode_FromString(value);
    }

    static handle from_cpp(char value, rv_policy, cleanup_list *) noexcept {
        return PyUnicode_FromStringAndSize(&value, 1);
    }

    template <typename T_>
    NB_INLINE bool can_cast() const noexcept {
        return std::is_pointer_v<T_> || (value && size == 1);
    }

    explicit operator const char *() { return value; }

    explicit operator char() {
        if (can_cast<char>())
            return value[0];
        else
            throw next_overload();
    }
};

template <typename T> struct type_caster<pointer_and_handle<T>> {
    using Caster = make_caster<T>;
    using T2 = pointer_and_handle<T>;
    NB_TYPE_CASTER(T2, Caster::Name)

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {
        Caster c;
        if (!c.from_python(src, flags_for_local_caster<T*>(flags), cleanup) ||
            !c.template can_cast<T*>())
            return false;
        value.h = src;
        value.p = c.operator T*();
        return true;
    }
};

template <> struct type_caster<fallback> {
    NB_TYPE_CASTER(fallback, const_name("object"))
    bool from_python(handle src, uint8_t flags, cleanup_list *) noexcept {
        if (!(flags & (uint8_t) cast_flags::convert))
            return false;
        value = src;
        return true;
    }
};

template <typename T> struct typed_base_name {
      static constexpr auto Name = type_caster<T>::Name;
};

// Base case: typed<T, Ts...> renders as T[Ts...]
template <typename T, typename... Ts> struct typed_name {
    static constexpr auto Name =
            typed_base_name<intrinsic_t<T>>::Name + const_name("[") +
            concat(const_name<std::is_same_v<Ts, ellipsis>>(const_name("..."),
                    make_caster<Ts>::Name)...) + const_name("]");
};

// typed<object, T> or typed<handle, T> renders as T, rather than as
// the nonsensical object[T]
template <typename T> struct typed_name<object, T> {
    static constexpr auto Name = make_caster<T>::Name;
};
template <typename T> struct typed_name<handle, T> {
    static constexpr auto Name = make_caster<T>::Name;
};

// typed<callable, R(Args...)> renders as Callable[[Args...], R]
template <typename R, typename... Args>
struct typed_name<callable, R(Args...)> {
    using Ret = std::conditional_t<std::is_void_v<R>, void_type, R>;
    static constexpr auto Name =
            const_name("collections.abc.Callable[[") +
            concat(make_caster<Args>::Name...) + const_name("], ") +
            make_caster<Ret>::Name + const_name("]");
};
// typed<callable, R(...)> renders as Callable[..., R]
template <typename R>
struct typed_name<callable, R(...)> {
    using Ret = std::conditional_t<std::is_void_v<R>, void_type, R>;
    static constexpr auto Name =
            const_name("collections.abc.Callable[..., ") +
            make_caster<Ret>::Name + const_name("]");
};

template <typename T, typename... Ts> struct type_caster<typed<T, Ts...>> {
    using Caster = make_caster<T>;
    using Typed = typed<T, Ts...>;

    NB_TYPE_CASTER(Typed, (typed_name<T, Ts...>::Name))

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {
        Caster caster;
        if (!caster.from_python(src, flags_for_local_caster<T>(flags), cleanup) ||
            !caster.template can_cast<T>())
            return false;
        value = caster.operator cast_t<T>();
        return true;
    }

   