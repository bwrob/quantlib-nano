&&, intrinsic_t<T> &>>;

/// Many type casters delegate to another caster using the pattern:
/// ~~~ .cc
/// bool from_python(handle src, uint8_t flags, cleanup_list *cl) noexcept {
///     SomeCaster c;
///     if (!c.from_python(src, flags, cl)) return false;
///     /* do something with */ c.operator T();
///     return true;
/// }
/// ~~~
/// This function adjusts the flags to avoid issues where the resulting T object
/// refers into storage that will dangle after SomeCaster is destroyed, and
/// causes a static assertion failure if that's not sufficient. Use it like:
/// ~~~ .cc
///     if (!c.from_python(src, flags_for_local_caster<T>(flags), cl))
///         return false;
/// ~~~
/// where the template argument T is the type you plan to extract.
template <typename T>
NB_INLINE uint8_t flags_for_local_caster(uint8_t flags) noexcept {
    using Caster = make_caster<T>;
    constexpr bool is_ref = std::is_pointer_v<T> || std::is_reference_v<T>;
    if constexpr (is_base_caster_v<Caster>) {
        if constexpr (is_ref) {
            /* References/pointers to a type produced by implicit conversions
               refer to storage owned by the cleanup_list. In a nb::cast() call,
               that storage will be released before the reference can be used;
               to prevent dangling, don't allow implicit conversions there. */
            if (flags & ((uint8_t) cast_flags::manual))
                flags &= ~((uint8_t) cast_flags::convert);
        }
    } else {
        /* Any pointer produced by a non-base caster will generally point
           into storage owned by the caster, which won't live long enough.
           Exception: the 'char' caster produces a result that points to
           storage owned by the incoming Python 'str' object, so it's OK. */
        static_assert(!is_ref || std::is_same_v<T, const char*> ||
                      (std::is_pointer_v<T> && std::is_constructible_v<T*, Caster>),
                      "nanobind generally cannot produce objects that "
                      "contain interior pointers T* (or references T&) if "
                      "the pointee T is not handled by nanobind's regular "
                      "class binding mechanism. For example, you can write "
                      "a function that accepts int*, or std::vector<int>, "
                      "but not std::vector<int*>.");
    }
    return flags;
}

template <typename T>
struct type_caster<T, enable_if_t<std::is_arithmetic_v<T> && !is_std_char_v<T>>> {
    NB_INLINE bool from_python(handle src, uint8_t flags, cleanup_list *) noexcept {
        if constexpr (std::is_floating_point_v<T>) {
            if constexpr (std::is_same_v<T, double>) {
                return detail::load_f64(src.ptr(), flags, &value);
            } else if constexpr (std::is_same_v<T, float>) {
                return detail::load_f32(src.ptr(), flags, &value);
            } else {
                double d;
                if (!detail::load_f64(src.ptr(), flags, &d))
                    return false;
                T result = (T) d;
                if ((flags & (uint8_t) cast_flags::convert)
                        || (double) result == d
                        || (result != result && d != d)) {
                    value = result;
                    return true;
                }
                return false;
            }
        } else {
            if constexpr (std::is_signed_v<T>) {
                if constexpr (sizeof(T) == 8)
                    return detail::load_i64(src.ptr(), flags, (int64_t *) &value);
                else if constexpr (sizeof(T) == 4)
                    return detail::load_i32(src.ptr(), flags, (int32_t *) &value);
                else if constexpr (sizeof(T) == 2)
                    return detail::load_i16(src.ptr(), flags, (int16_t *) &value);
                else
                    return detail::load_i8(src.ptr(), flags, (int8_t *) &value);
            } else {
                if constexpr (sizeof(T) == 