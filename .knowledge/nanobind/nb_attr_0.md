/*
    nanobind/nb_attr.h: Annotations for function and class declarations

    Copyright (c) 2022 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

NAMESPACE_BEGIN(NB_NAMESPACE)

struct scope {
    PyObject *value;
    NB_INLINE scope(handle value) : value(value.ptr()) {}
};

struct name {
    const char *value;
    NB_INLINE name(const char *value) : value(value) {}
};

struct arg_v;
struct arg_locked;
struct arg_locked_v;

// Basic function argument descriptor (no default value, not locked)
struct arg {
    NB_INLINE constexpr explicit arg(const char *name = nullptr) : name_(name), signature_(nullptr) { }

    // operator= can be used to provide a default value
    template <typename T> NB_INLINE arg_v operator=(T &&value) const;

    // Mutators that don't change default value or locked state
    NB_INLINE arg &noconvert(bool value = true) {
        convert_ = !value;
        return *this;
    }
    NB_INLINE arg &none(bool value = true) {
        none_ = value;
        return *this;
    }
    NB_INLINE arg &sig(const char *value) {
        signature_ = value;
        return *this;
    }

    // After lock(), this argument is locked
    NB_INLINE arg_locked lock();

    const char *name_, *signature_;
    uint8_t convert_{ true };
    bool none_{ false };
};

// Function argument descriptor with default value (not locked)
struct arg_v : arg {
    object value;
    NB_INLINE arg_v(const arg &base, object &&value)
        : arg(base), value(std::move(value)) {}

  private:
    // Inherited mutators would slice off the default, and are not generally needed
    using arg::noconvert;
    using arg::none;
    using arg::sig;
    using arg::lock;
};

// Function argument descriptor that is locked (no default value)
struct arg_locked : arg {
    NB_INLINE constexpr explicit arg_locked(const char *name = nullptr) : arg(name) { }
    NB_INLINE constexpr explicit arg_locked(const arg &base) : arg(base) { }

    // operator= can be used to provide a default value
    template <typename T> NB_INLINE arg_locked_v operator=(T &&value) const;

    // Mutators must be respecified in order to not slice off the locked status
    NB_INLINE arg_locked &noconvert(bool value = true) {
        convert_ = !value;
        return *this;
    }
    NB_INLINE arg_locked &none(bool value = true) {
        none_ = value;
        return *this;
    }
    NB_INLINE arg_locked &sig(const char *value) {
        signature_ = value;
        return *this;
    }

    // Redundant extra lock() is allowed
    NB_INLINE arg_locked &lock() { return *this; }
};

// Function argument descriptor that is potentially locked and has a default value
struct arg_locked_v : arg_locked {
    object value;
    NB_INLINE arg_locked_v(const arg_locked &base, object &&value)
        : arg_locked(base), value(std::move(value)) {}

  private:
    // Inherited mutators would slice off the default, and are not generally needed
    using arg_locked::noconvert;
    using arg_locked::none;
    using arg_locked::sig;
    using arg_locked::lock;
};

NB_INLINE arg_locked arg::lock() { return arg_locked{*this}; }

template <typename... Ts> struct call_guard {
    using type = detail::tuple<Ts...>;
};

struct dynamic_attr {};
struct is_weak_referenceable {};
struct is_method {};
struct is_implicit {};
struct is_operator {};
struct is_arithmetic {};
struct is_flag {};
struct is_final {};
struct is_generic {};
struct kw_only {};
struct lock_self {};
struct never_destruct {};

template <size_t /* Nurse */, size_t /* Patient */> struct keep_alive {};
template <typename T> struct supplement {};
template <typename T> struct intrusive_ptr {
    intrusive_ptr(void (*set_self_py)(T *, PyObject *) noexcept)
        : set_self_py(set_self_py) { }
    void (*set_self_py)(T *, PyObject *) noexcept;
};

struct type_slots {
    type_slots (const PyType_Slot *value) : value(value) { }
    const PyType_Slot *value;
}