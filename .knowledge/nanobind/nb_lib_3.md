 to relinquish ownership from Python object to a unique_ptr;
/// return true if successful, false if not. (Failure is only
/// possible if `cpp_delete` is true.)
NB_CORE bool nb_type_relinquish_ownership(PyObject *o, bool cpp_delete) noexcept;

/// Reverse the effects of nb_type_relinquish_ownership().
NB_CORE void nb_type_restore_ownership(PyObject *o, bool cpp_delete) noexcept;

/// Get a pointer to a user-defined 'extra' value associated with the nb_type t.
NB_CORE void *nb_type_supplement(PyObject *t) noexcept;

/// Check if the given python object represents a nanobind type
NB_CORE bool nb_type_check(PyObject *t) noexcept;

/// Return the size of the type wrapped by the given nanobind type object
NB_CORE size_t nb_type_size(PyObject *t) noexcept;

/// Return the alignment of the type wrapped by the given nanobind type object
NB_CORE size_t nb_type_align(PyObject *t) noexcept;

/// Return a unicode string representing the long-form name of the given type
NB_CORE PyObject *nb_type_name(PyObject *t) noexcept;

/// Return a unicode string representing the long-form name of object's type
NB_CORE PyObject *nb_inst_name(PyObject *o) noexcept;

/// Return the C++ type_info wrapped by the given nanobind type object
NB_CORE const std::type_info *nb_type_info(PyObject *t) noexcept;

/// Get a pointer to the instance data of a nanobind instance (nb_inst)
NB_CORE void *nb_inst_ptr(PyObject *o) noexcept;

/// Check if a Python type object wraps an instance of a specific C++ type
NB_CORE bool nb_type_isinstance(PyObject *obj, const std::type_info *t) noexcept;

/// Search for the Python type object associated with a C++ type
NB_CORE PyObject *nb_type_lookup(const std::type_info *t) noexcept;

/// Allocate an instance of type 't'
NB_CORE PyObject *nb_inst_alloc(PyTypeObject *t);

/// Allocate an zero-initialized instance of type 't'
NB_CORE PyObject *nb_inst_alloc_zero(PyTypeObject *t);

/// Allocate an instance of type 't' referencing the existing 'ptr'
NB_CORE PyObject *nb_inst_reference(PyTypeObject *t, void *ptr,
                                    PyObject *parent);

/// Allocate an instance of type 't' taking ownership of the existing 'ptr'
NB_CORE PyObject *nb_inst_take_ownership(PyTypeObject *t, void *ptr);

/// Call the destructor of the given python object
NB_CORE void nb_inst_destruct(PyObject *o) noexcept;

/// Zero-initialize a POD type and mark it as ready + to be destructed upon GC
NB_CORE void nb_inst_zero(PyObject *o) noexcept;

/// Copy-construct 'dst' from 'src', mark it as ready and to be destructed (must have the same nb_type)
NB_CORE void nb_inst_copy(PyObject *dst, const PyObject *src) noexcept;

/// Move-construct 'dst' from 'src', mark it as ready and to be destructed (must have the same nb_type)
NB_CORE void nb_inst_move(PyObject *dst, const PyObject *src) noexcept;

/// Destruct 'dst', copy-construct 'dst' from 'src', mark ready and retain 'destruct' status (must have the same nb_type)
NB_CORE void nb_inst_replace_copy(PyObject *dst, const PyObject *src) noexcept;

/// Destruct 'dst', move-construct 'dst' from 'src', mark ready and retain 'destruct' status (must have the same nb_type)
NB_CORE void nb_inst_replace_move(PyObject *dst, const PyObject *src) noexcept;

/// Check if a particular instance uses a Python-derived type
NB_CORE bool nb_inst_python_derived(PyObject *o) noexcept;

/// Overwrite the instance's ready/destruct flags
NB_CORE void nb_inst_set_state(PyObject *o, bool ready, bool destruct) noexcept;

/// Query the 'ready' and 'destruct' flags of an instance
NB_CORE std::pair<bool, bool> nb_inst_state(PyObject *o) noexcept;

// ========================================================================

// Create and install a Python property object
NB_CORE void property_install(PyObject *scope, const char *name,
                              PyObject *getter, PyObject *setter) noexcept;

NB_CORE void property_install_static(PyObject *scope, const char *name,
                                     PyObje
