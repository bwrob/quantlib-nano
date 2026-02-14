vector function call
NB_CORE PyObject *obj_vectorcall(PyObject *base, PyObject *const *args,
                                 size_t nargsf, PyObject *kwnames,
                                 bool method_call);

/// Create an iterator from 'o', raise an exception in case of errors
NB_CORE PyObject *obj_iter(PyObject *o);

/// Advance the iterator 'o', raise an exception in case of errors
NB_CORE PyObject *obj_iter_next(PyObject *o);

// ========================================================================

// Conversion validity check done by nb::make_tuple
NB_CORE void tuple_check(PyObject *tuple, size_t nargs);

// ========================================================================

// Append a single argument to a function call
NB_CORE void call_append_arg(PyObject *args, size_t &nargs, PyObject *value);

// Append a variable-length sequence of arguments to a function call
NB_CORE void call_append_args(PyObject *args, size_t &nargs, PyObject *value);

// Append a single keyword argument to a function call
NB_CORE void call_append_kwarg(PyObject *kwargs, const char *name, PyObject *value);

// Append a variable-length dictionary of keyword arguments to a function call
NB_CORE void call_append_kwargs(PyObject *kwargs, PyObject *value);

// ========================================================================

// If the given sequence has the size 'size', return a pointer to its contents.
// May produce a temporary.
NB_CORE PyObject **seq_get_with_size(PyObject *seq, size_t size,
                                     PyObject **temp) noexcept;

// Like the above, but return the size instead of checking it.
NB_CORE PyObject **seq_get(PyObject *seq, size_t *size,
                           PyObject **temp) noexcept;

// ========================================================================

/// Create a new capsule object with a name
NB_CORE PyObject *capsule_new(const void *ptr, const char *name,
                              void (*cleanup)(void *) noexcept) noexcept;

// ========================================================================

// Forward declaration for type in nb_attr.h
struct func_data_prelim_base;

/// Create a Python function object for the given function record
NB_CORE PyObject *nb_func_new(const func_data_prelim_base *f) noexcept;

// ========================================================================

/// Create a Python type object for the given type record
struct type_init_data;
NB_CORE PyObject *nb_type_new(const type_init_data *c) noexcept;

/// Extract a pointer to a C++ type underlying a Python object, if possible
NB_CORE bool nb_type_get(const std::type_info *t, PyObject *o, uint8_t flags,
                         cleanup_list *cleanup, void **out) noexcept;

/// Cast a C++ type instance into a Python object
NB_CORE PyObject *nb_type_put(const std::type_info *cpp_type, void *value,
                              rv_policy rvp, cleanup_list *cleanup,
                              bool *is_new = nullptr) noexcept;

// Special version of nb_type_put for polymorphic classes
NB_CORE PyObject *nb_type_put_p(const std::type_info *cpp_type,
                                const std::type_info *cpp_type_p, void *value,
                                rv_policy rvp, cleanup_list *cleanup,
                                bool *is_new = nullptr) noexcept;

// Special version of 'nb_type_put' for unique pointers and ownership transfer
NB_CORE PyObject *nb_type_put_unique(const std::type_info *cpp_type,
                                     void *value, cleanup_list *cleanup,
                                     bool cpp_delete) noexcept;

// Special version of 'nb_type_put_unique' for polymorphic classes
NB_CORE PyObject *nb_type_put_unique_p(const std::type_info *cpp_type,
                                       const std::type_info *cpp_type_p,
                                       void *value, cleanup_list *cleanup,
                                       bool cpp_delete) noexcept;

/// Try
