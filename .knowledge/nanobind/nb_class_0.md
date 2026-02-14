/*
    nanobind/nb_class.h: Functionality for binding C++ classes/structs

    Copyright (c) 2022 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

NAMESPACE_BEGIN(NB_NAMESPACE)
NAMESPACE_BEGIN(detail)

/// Flags about a type that persist throughout its lifetime
enum class type_flags : uint32_t {
    /// Does the type provide a C++ destructor?
    is_destructible          = (1 << 0),

    /// Does the type provide a C++ copy constructor?
    is_copy_constructible    = (1 << 1),

    /// Does the type provide a C++ move constructor?
    is_move_constructible    = (1 << 2),

    /// Is the 'destruct' field of the type_data structure set?
    has_destruct             = (1 << 4),

    /// Is the 'copy' field of the type_data structure set?
    has_copy                 = (1 << 5),

    /// Is the 'move' field of the type_data structure set?
    has_move                 = (1 << 6),

    /// Internal: does the type maintain a list of implicit conversions?
    has_implicit_conversions = (1 << 7),

    /// Is this a python type that extends a bound C++ type?
    is_python_type           = (1 << 8),

    /// This type does not permit subclassing from Python
    is_final                 = (1 << 9),

    /// Instances of this type support dynamic attribute assignment
    has_dynamic_attr         = (1 << 10),

    /// The class uses an intrusive reference counting approach
    intrusive_ptr            = (1 << 11),

    /// Is this a class that inherits from enable_shared_from_this?
    /// If so, type_data::keep_shared_from_this_alive is also set.
    has_shared_from_this     = (1 << 12),

    /// Instances of this type can be referenced by 'weakref'
    is_weak_referenceable    = (1 << 13),

    /// A custom signature override was specified
    has_signature            = (1 << 14),

    /// The class implements __class_getitem__ similar to typing.Generic
    is_generic               = (1 << 15),

    /// Does the type implement a custom __new__ operator?
    has_new                  = (1 << 16),

    /// Does the type implement a custom __new__ operator that can take no args
    /// (except the type object)?
    has_nullary_new          = (1 << 17)

    // One more bit available without needing a larger reorganization
};

/// Flags about a type that are only relevant when it is being created.
/// These are currently stored in type_data::flags alongside the type_flags
/// for more efficient memory layout, but could move elsewhere if we run
/// out of flags.
enum class type_init_flags : uint32_t {
    /// Is the 'supplement' field of the type_init_data structure set?
    has_supplement           = (1 << 19),

    /// Is the 'doc' field of the type_init_data structure set?
    has_doc                  = (1 << 20),

    /// Is the 'base' field of the type_init_data structure set?
    has_base                 = (1 << 21),

    /// Is the 'base_py' field of the type_init_data structure set?
    has_base_py              = (1 << 22),

    /// This type provides extra PyType_Slot fields
    has_type_slots           = (1 << 23),

    all_init_flags           = (0x1f << 19)
};

// See internals.h
struct nb_alias_chain;

// Implicit conversions for C++ type bindings, used in type_data below
struct implicit_t {
    const std::type_info **cpp;
    bool (**py)(PyTypeObject *, PyObject *, cleanup_list *) noexcept;
};

// Forward and reverse mappings for enumerations, used in type_data below
struct enum_tbl_t {
    void *fwd;
    void *rev;
};

/// Information about a type that persists throughout its lifetime
struct type_data {
    uint32_t size;
    uint32_t align : 8;
    uint32_t flags : 24;
    const char *name;
    const std::type_info *type;
    PyTypeObject *type_py;
    nb_alias_chain *alias_chain;
#if defined(Py_LIMITED_API)
    PyObject* (*vectorcall)(PyObject *, PyObject * const*, size_t, PyObject *);
#endif
    void *init; // Constructor nb_func

