/*
    nanobind/nb_cast.h: Type caster interface and essential type casters

    Copyright (c) 2022 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

#define NB_TYPE_CASTER(Value_, descr)                                          \
    using Value = Value_;                                                      \
    static constexpr auto Name = descr;                                        \
    template <typename T_> using Cast = movable_cast_t<T_>;                    \
    template <typename T_> static constexpr bool can_cast() { return true; }   \
    template <typename T_,                                                     \
              enable_if_t<std::is_same_v<std::remove_cv_t<T_>, Value>> = 0>    \
    static handle from_cpp(T_ *p, rv_policy policy, cleanup_list *list) {      \
        if (!p)                                                                \
            return none().release();                                           \
        return from_cpp(*p, policy, list);                                     \
    }                                                                          \
    explicit operator Value*() { return &value; }                              \
    explicit operator Value&() { return (Value &) value; }                     \
    explicit operator Value&&() { return (Value &&) value; }                   \
    Value value;

#define NB_MAKE_OPAQUE(...)                                                    \
    namespace nanobind::detail {                                               \
    template <> class type_caster<__VA_ARGS__>                                 \
        : public type_caster_base<__VA_ARGS__> { }; }

NAMESPACE_BEGIN(NB_NAMESPACE)
NAMESPACE_BEGIN(detail)

/**
 * Type casters expose a member 'Cast<T>' which users of a type caster must
 * query to determine what the caster actually can (and prefers) to produce.
 * The convenience alias ``cast_t<T>`` defined below performs this query for a
 * given type ``T``.
 *
 * Often ``cast_t<T>`` is simply equal to ``T`` or ``T&``. More significant
 * deviations are also possible, which could be due to one of the following
 * two reasons:
 *
 * 1. Efficiency: most STL type casters create a local copy (``value`` member)
 *    of the value being cast. The caller should move this value to its
 *    intended destination instead of making further copies along the way.
 *    Consequently, ``cast_t<std::vector<T>>`` yields ``cast_t<std::vector<T>>
 *    &&`` to enable such behavior.
 *
 * 2. STL pairs may contain references, and such pairs aren't
 *    default-constructible. The STL pair caster therefore cannot create a local
 *    copy and must construct the pair on the fly, which in turns means that it
 *    cannot return references. Therefore, ``cast_t<const std::pair<T1, T2>&>``
 *    yields ``std::pair<T1, T2>``.
 */

/// Ask a type caster what flavors of a type it can actually produce -- may be different from 'T'
template <typename T> using cast_t = typename make_caster<T>::template Cast<T>;

/// This is a default choice for the 'Cast' type alias described above. It
/// prefers to return rvalue references to allow the caller to move the object.
template <typename T>
using movable_cast_t =
    std::conditional_t<is_pointer_v<T>, intrinsic_t<T> *,
                       std::conditional_t<std::is_lvalue_reference_v<T>,
                                          intrinsic_t<T> &, intrinsic_t<T> &&>>;

/// This version is more careful about what the caller actually requested and
/// only moves when this was explicitly requested. It is the default for the
/// base type caster (i.e., types bound via ``nanobind::class_<..>``)
template <typename T>
using precise_cast_t =
    std::conditional_t<is_pointer_v<T>, intrinsic_t<T> *,
                       std::conditional_t<std::is_rvalue_reference_v<T>,
                                          intrinsic_t<T>
