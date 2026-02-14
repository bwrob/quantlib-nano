y_check(PyObject *o) noexcept;

// ========================================================================

/// Print to stdout using Python
NB_CORE void print(PyObject *file, PyObject *str, PyObject *end);

// ========================================================================

typedef void (*exception_translator)(const std::exception_ptr &, void *);

NB_CORE void register_exception_translator(exception_translator translator,
                                           void *payload);

NB_CORE PyObject *exception_new(PyObject *mod, const char *name,
                                PyObject *base);

// ========================================================================

NB_CORE bool load_i8 (PyObject *o, uint8_t flags, int8_t *out) noexcept;
NB_CORE bool load_u8 (PyObject *o, uint8_t flags, uint8_t *out) noexcept;
NB_CORE bool load_i16(PyObject *o, uint8_t flags, int16_t *out) noexcept;
NB_CORE bool load_u16(PyObject *o, uint8_t flags, uint16_t *out) noexcept;
NB_CORE bool load_i32(PyObject *o, uint8_t flags, int32_t *out) noexcept;
NB_CORE bool load_u32(PyObject *o, uint8_t flags, uint32_t *out) noexcept;
NB_CORE bool load_i64(PyObject *o, uint8_t flags, int64_t *out) noexcept;
NB_CORE bool load_u64(PyObject *o, uint8_t flags, uint64_t *out) noexcept;
NB_CORE bool load_f32(PyObject *o, uint8_t flags, float *out) noexcept;
NB_CORE bool load_f64(PyObject *o, uint8_t flags, double *out) noexcept;

// ========================================================================

/// Increase the reference count of 'o', and check that the GIL is held
NB_CORE void incref_checked(PyObject *o) noexcept;

/// Decrease the reference count of 'o', and check that the GIL is held
NB_CORE void decref_checked(PyObject *o) noexcept;

// ========================================================================

NB_CORE bool leak_warnings() noexcept;
NB_CORE bool implicit_cast_warnings() noexcept;
NB_CORE void set_leak_warnings(bool value) noexcept;
NB_CORE void set_implicit_cast_warnings(bool value) noexcept;

// ========================================================================

NB_CORE bool iterable_check(PyObject *o) noexcept;

// ========================================================================

NB_CORE void slice_compute(PyObject *slice, Py_ssize_t size,
                           Py_ssize_t &start, Py_ssize_t &stop,
                           Py_ssize_t &step, size_t &slice_length);

// ========================================================================

NB_CORE bool issubclass(PyObject *a, PyObject *b);

// ========================================================================

NB_CORE PyObject *repr_list(PyObject *o);
NB_CORE PyObject *repr_map(PyObject *o);

NB_CORE bool is_alive() noexcept;

#if NB_TYPE_GET_SLOT_IMPL
NB_CORE void *type_get_slot(PyTypeObject *t, int slot_id);
#endif

NB_CORE PyObject *dict_get_item_ref_or_fail(PyObject *d, PyObject *k);

NB_CORE const char *abi_tag();

NAMESPACE_END(detail)

using detail::raise;
using detail::raise_type_error;
using detail::raise_python_error;

NAMESPACE_END(NB_NAMESPACE)