// ========================================================================

/// Convert a Python object into a Python byte array
NB_CORE PyObject *bytearray_from_obj(PyObject *o);

/// Convert a memory region into a Python byte array
NB_CORE PyObject *bytearray_from_cstr_and_size(const void *c, size_t n);

// ========================================================================

/// Convert a Python object into a Python boolean object
NB_CORE PyObject *bool_from_obj(PyObject *o);

/// Convert a Python object into a Python integer object
NB_CORE PyObject *int_from_obj(PyObject *o);

/// Convert a Python object into a Python floating point object
NB_CORE PyObject *float_from_obj(PyObject *o);

// ========================================================================

/// Convert a Python object into a Python list
NB_CORE PyObject *list_from_obj(PyObject *o);

/// Convert a Python object into a Python tuple
NB_CORE PyObject *tuple_from_obj(PyObject *o);

/// Convert a Python object into a Python set
NB_CORE PyObject *set_from_obj(PyObject *o);

/// Convert a Python object into a Python frozenset
NB_CORE PyObject *frozenset_from_obj(PyObject *o);

/// Convert a Python object into a Python memoryview
NB_CORE PyObject *memoryview_from_obj(PyObject *o);

// ========================================================================

/// Get an object attribute or raise an exception
NB_CORE PyObject *getattr(PyObject *obj, const char *key);
NB_CORE PyObject *getattr(PyObject *obj, PyObject *key);

/// Get an object attribute or return a default value (never raises)
NB_CORE PyObject *getattr(PyObject *obj, const char *key, PyObject *def) noexcept;
NB_CORE PyObject *getattr(PyObject *obj, PyObject *key, PyObject *def) noexcept;

/// Get an object attribute or raise an exception. Skip if 'out' is non-null
NB_CORE void getattr_or_raise(PyObject *obj, const char *key, PyObject **out);
NB_CORE void getattr_or_raise(PyObject *obj, PyObject *key, PyObject **out);

/// Set an object attribute or raise an exception
NB_CORE void setattr(PyObject *obj, const char *key, PyObject *value);
NB_CORE void setattr(PyObject *obj, PyObject *key, PyObject *value);

/// Delete an object attribute or raise an exception
NB_CORE void delattr(PyObject *obj, const char *key);
NB_CORE void delattr(PyObject *obj, PyObject *key);

// ========================================================================

/// Index into an object or raise an exception. Skip if 'out' is non-null
NB_CORE void getitem_or_raise(PyObject *obj, Py_ssize_t, PyObject **out);
NB_CORE void getitem_or_raise(PyObject *obj, const char *key, PyObject **out);
NB_CORE void getitem_or_raise(PyObject *obj, PyObject *key, PyObject **out);

/// Set an item or raise an exception
NB_CORE void setitem(PyObject *obj, Py_ssize_t, PyObject *value);
NB_CORE void setitem(PyObject *obj, const char *key, PyObject *value);
NB_CORE void setitem(PyObject *obj, PyObject *key, PyObject *value);

/// Delete an item or raise an exception
NB_CORE void delitem(PyObject *obj, Py_ssize_t);
NB_CORE void delitem(PyObject *obj, const char *key);
NB_CORE void delitem(PyObject *obj, PyObject *key);

// ========================================================================

/// Determine the length of a Python object
NB_CORE size_t obj_len(PyObject *o);

/// Try to roughly determine the length of a Python object
NB_CORE size_t obj_len_hint(PyObject *o) noexcept;

/// Obtain a string representation of a Python object
NB_CORE PyObject* obj_repr(PyObject *o);

/// Perform a comparison between Python objects and handle errors
NB_CORE bool obj_comp(PyObject *a, PyObject *b, int value);

/// Perform an unary operation on a Python object with error handling
NB_CORE PyObject *obj_op_1(PyObject *a, PyObject* (*op)(PyObject*));

/// Perform an unary operation on a Python object with error handling
NB_CORE PyObject *obj_op_2(PyObject *a, PyObject *b,
                           PyObject *(*op)(PyObject *, PyObject *));

// Perform a
