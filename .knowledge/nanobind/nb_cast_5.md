  // so we prohibit it by default, with two exceptions that we know are safe:
    //
    // - If we're casting to a bound object type, the returned pointer points
    //   into storage owned by that object, not the type caster. Note this is
    //   only safe if we don't allow implicit conversions, because the pointer
    //   produced after an implicit conversion points into storage owned by
    //   a temporary object in the cleanup list, and we have to release those
    //   temporaries before we return.
    //
    // - If we're casting to const char*, the caster was provided by nanobind,
    //   and we know it will only accept Python 'str' objects, producing
    //   a pointer to storage owned by that object.

    constexpr bool is_ref = std::is_reference_v<T> || std::is_pointer_v<T>;
    static_assert(
        !is_ref ||
            is_base_caster_v<Caster> ||
            std::is_same_v<const char *, T>,
        "nanobind::cast(): cannot return a reference to a temporary.");

    Caster caster;
    bool rv;
    if constexpr (Convert && !is_ref) {
        // Release the values in the cleanup list only after we
        // initialize the return object, since the initialization
        // might access those temporaries.
        struct raii_cleanup {
            cleanup_list list{nullptr};
            ~raii_cleanup() { list.release(); }
        } cleanup;
        rv = caster.from_python(h.ptr(),
                                ((uint8_t) cast_flags::convert) |
                                ((uint8_t) cast_flags::manual),
                                &cleanup.list);
        if (!rv)
            detail::raise_python_or_cast_error();
        return caster.operator cast_t<T>();
    } else {
        rv = caster.from_python(h.ptr(), (uint8_t) cast_flags::manual, nullptr);
        if (!rv)
            detail::raise_python_or_cast_error();
        return caster.operator cast_t<T>();
    }
}

template <bool Convert, typename T>
bool try_cast_impl(handle h, T &out) noexcept {
    using Caster = detail::make_caster<T>;

    // See comments in cast_impl above
    constexpr bool is_ref = std::is_reference_v<T> || std::is_pointer_v<T>;
    static_assert(
        !is_ref ||
            is_base_caster_v<Caster> ||
            std::is_same_v<const char *, T>,
        "nanobind::try_cast(): cannot return a reference to a temporary.");

    Caster caster;
    bool rv;
    if constexpr (Convert && !is_ref) {
        cleanup_list cleanup(nullptr);
        rv = caster.from_python(h.ptr(),
                                ((uint8_t) cast_flags::convert) |
                                ((uint8_t) cast_flags::manual),
                                &cleanup) &&
             caster.template can_cast<T>();
        if (rv) {
            out = caster.operator cast_t<T>();
        }
        cleanup.release(); // 'from_python' is 'noexcept', so this always runs
    } else {
        rv = caster.from_python(h.ptr(), (uint8_t) cast_flags::manual, nullptr) &&
             caster.template can_cast<T>();
        if (rv) {
            out = caster.operator cast_t<T>();
        }
    }

    return rv;
}

NAMESPACE_END(detail)

template <typename T, typename Derived>
NB_INLINE T cast(const detail::api<Derived> &value, bool convert = true) {
    if constexpr (std::is_same_v<T, void>) {
        (void) value; (void) convert;
        return;
    } else {
        if (convert)
            return detail::cast_impl<true, T>(value);
        else
            return detail::cast_impl<false, T>(value);
    }
}

template <typename T, typename Derived>
NB_INLINE bool try_cast(const detail::api<Derived> &value, T &out, bool convert = true) noexcept {
    if (convert)
        return detail::try_cast_impl<true, T>(value, out);
    else
        return detail::try_cast_impl<false, T>(value, out);
}

template <typename T>
object cast(T &&value, rv_policy policy = rv_policy::automatic_reference) {
    handle h = detail::make_caster<T>::from_cpp((detail::forward_t<T>) value,
    