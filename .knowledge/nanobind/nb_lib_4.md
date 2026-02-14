ct *getter,
                                     PyObject *setter) noexcept;

// ========================================================================

NB_CORE PyObject *get_override(void *ptr, const std::type_info *type,
                               const char *name, bool pure);

// ========================================================================

// Ensure that 'patient' cannot be GCed while 'nurse' is alive
NB_CORE void keep_alive(PyObject *nurse, PyObject *patient);

// Keep 'payload' alive until 'nurse' is GCed
NB_CORE void keep_alive(PyObject *nurse, void *payload,
                        void (*deleter)(void *) noexcept) noexcept;


// ========================================================================

/// Indicate to nanobind that an implicit constructor can convert 'src' -> 'dst'
NB_CORE void implicitly_convertible(const std::type_info *src,
                                    const std::type_info *dst) noexcept;

/// Register a callback to check if implicit conversion to 'dst' is possible
NB_CORE void implicitly_convertible(bool (*predicate)(PyTypeObject *,
                                                      PyObject *,
                                                      cleanup_list *),
                                    const std::type_info *dst) noexcept;

// ========================================================================

struct enum_init_data;

/// Create a new enumeration type
NB_CORE PyObject *enum_create(enum_init_data *) noexcept;

/// Append an entry to an enumeration
NB_CORE void enum_append(PyObject *tp, const char *name,
                         int64_t value, const char *doc) noexcept;

// Query an enumeration's Python object -> integer value map
NB_CORE bool enum_from_python(const std::type_info *, PyObject *, int64_t *,
                              uint8_t flags) noexcept;

// Query an enumeration's integer value -> Python object map
NB_CORE PyObject *enum_from_cpp(const std::type_info *, int64_t) noexcept;

/// Export enum entries to the parent scope
NB_CORE void enum_export(PyObject *tp);

// ========================================================================

/// Try to import a Python extension module, raises an exception upon failure
NB_CORE PyObject *module_import(const char *name);

/// Try to import a Python extension module, raises an exception upon failure
NB_CORE PyObject *module_import(PyObject *name);

/// Create a submodule of an existing module
NB_CORE PyObject *module_new_submodule(PyObject *base, const char *name,
                                       const char *doc) noexcept;


// ========================================================================

// Try to import a reference-counted ndarray object via DLPack
NB_CORE ndarray_handle *ndarray_import(PyObject *o,
                                       const ndarray_config *c,
                                       bool convert,
                                       cleanup_list *cleanup) noexcept;

// Describe a local ndarray object using a DLPack capsule
NB_CORE ndarray_handle *ndarray_create(void *data, size_t ndim,
                                       const size_t *shape, PyObject *owner,
                                       const int64_t *strides,
                                       dlpack::dtype dtype, bool ro,
                                       int device, int device_id,
                                       char order);

/// Increase the reference count of the given ndarray object; returns a pointer
/// to the underlying DLTensor
NB_CORE dlpack::dltensor *ndarray_inc_ref(ndarray_handle *) noexcept;

/// Decrease the reference count of the given ndarray object
NB_CORE void ndarray_dec_ref(ndarray_handle *) noexcept;

/// Wrap a ndarray_handle* into a PyCapsule
NB_CORE PyObject *ndarray_export(ndarray_handle *, int framework,
                                 rv_policy policy, cleanup_list *cleanup) noexcept;

/// Check if an object represents an ndarray
NB_CORE bool ndarra
