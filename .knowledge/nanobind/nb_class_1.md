 void (*destruct)(void *);
    void (*copy)(void *, const void *);
    void (*move)(void *, void *) noexcept;
    union {
        implicit_t implicit;  // for C++ type bindings
        enum_tbl_t enum_tbl;  // for enumerations
    };
    void (*set_self_py)(void *, PyObject *) noexcept;
    bool (*keep_shared_from_this_alive)(PyObject *) noexcept;
    uint32_t dictoffset;
    uint32_t weaklistoffset;
};

/// Information about a type that is only relevant when it is being created
struct type_init_data : type_data {
    PyObject *scope;
    const std::type_info *base;
    PyTypeObject *base_py;
    const char *doc;
    const PyType_Slot *type_slots;
    size_t supplement;
};

NB_INLINE void type_extra_apply(type_init_data &t, const handle &h) {
    t.flags |= (uint32_t) type_init_flags::has_base_py;
    t.base_py = (PyTypeObject *) h.ptr();
}

NB_INLINE void type_extra_apply(type_init_data &t, const char *doc) {
    t.flags |= (uint32_t) type_init_flags::has_doc;
    t.doc = doc;
}

NB_INLINE void type_extra_apply(type_init_data &t, type_slots c) {
    t.flags |= (uint32_t) type_init_flags::has_type_slots;
    t.type_slots = c.value;
}

template <typename T>
NB_INLINE void type_extra_apply(type_init_data &t, intrusive_ptr<T> ip) {
    t.flags |= (uint32_t) type_flags::intrusive_ptr;
    t.set_self_py = (void (*)(void *, PyObject *) noexcept) ip.set_self_py;
}

NB_INLINE void type_extra_apply(type_init_data &t, is_final) {
    t.flags |= (uint32_t) type_flags::is_final;
}

NB_INLINE void type_extra_apply(type_init_data &t, dynamic_attr) {
    t.flags |= (uint32_t) type_flags::has_dynamic_attr;
}

NB_INLINE void type_extra_apply(type_init_data & t, is_weak_referenceable) {
    t.flags |= (uint32_t) type_flags::is_weak_referenceable;
}

NB_INLINE void type_extra_apply(type_init_data & t, is_generic) {
    t.flags |= (uint32_t) type_flags::is_generic;
}

NB_INLINE void type_extra_apply(type_init_data & t, const sig &s) {
    t.flags |= (uint32_t) type_flags::has_signature;
    t.name = s.value;
}

NB_INLINE void type_extra_apply(type_init_data &, never_destruct) {
    // intentionally empty
}

template <typename T>
NB_INLINE void type_extra_apply(type_init_data &t, supplement<T>) {
    static_assert(std::is_trivially_default_constructible_v<T>,
                  "The supplement must be a POD (plain old data) type");
    static_assert(alignof(T) <= alignof(void *),
                  "The alignment requirement of the supplement is too high.");
    t.flags |= (uint32_t) type_init_flags::has_supplement | (uint32_t) type_flags::is_final;
    t.supplement = sizeof(T);
}

enum class enum_flags : uint32_t {
    /// Is this an arithmetic enumeration?
    is_arithmetic            = (1 << 1),

    /// Is the number type underlying the enumeration signed?
    is_signed                = (1 << 2),

    /// Is the underlying enumeration type Flag?
    is_flag                = (1 << 3)
};

struct enum_init_data {
    const std::type_info *type;
    PyObject *scope;
    const char *name;
    const char *docstr;
    uint32_t flags;
};

NB_INLINE void enum_extra_apply(enum_init_data &e, is_arithmetic) {
    e.flags |= (uint32_t) enum_flags::is_arithmetic;
}

NB_INLINE void enum_extra_apply(enum_init_data &e, is_flag) {
    e.flags |= (uint32_t) enum_flags::is_flag;
}

NB_INLINE void enum_extra_apply(enum_init_data &e, const char *doc) {
    e.docstr = doc;
}

template <typename T>
NB_INLINE void enum_extra_apply(enum_init_data &, T) {
    static_assert(
        std::is_void_v<T>,
        "Invalid enum binding annotation. The implementation of "
        "enums changed nanobind 2.0.0: only nb::is_arithmetic and "
        "docstrings can be passed since this change.");
}

template <typename T> void wrap_copy(void *dst, const void *src) {
    new ((T *) dst) T(*(const T *) src);
}

template <typename T> void wrap_move(void *dst, void *src) noexcept {
    new ((T *) dst) T(std::move(*(T *) src));
}

template <typename T> void wrap_destruct(void *value) noe
