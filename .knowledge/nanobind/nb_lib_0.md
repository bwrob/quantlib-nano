/*
    nanobind/nb_lib.h: Interface to libnanobind.so

    Copyright (c) 2022 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

NAMESPACE_BEGIN(NB_NAMESPACE)

NAMESPACE_BEGIN(dlpack)

// The version of DLPack that is supported by libnanobind
static constexpr uint32_t major_version = 1;
static constexpr uint32_t minor_version = 1;

// Forward declarations for types in ndarray.h (1)
struct dltensor;
struct dtype;

NAMESPACE_END(dlpack)

NAMESPACE_BEGIN(detail)

// Forward declarations for types in ndarray.h (2)
struct ndarray_handle;
struct ndarray_config;

/**
 * Helper class to clean temporaries created by function dispatch.
 * The first element serves a special role: it stores the 'self'
 * object of method calls (for rv_policy::reference_internal).
 */
struct NB_CORE cleanup_list {
public:
    static constexpr uint32_t Small = 6;

    cleanup_list(PyObject *self) :
        m_size{1},
        m_capacity{Small},
        m_data{m_local} {
        m_local[0] = self;
    }

    ~cleanup_list() = default;

    /// Append a single PyObject to the cleanup stack
    NB_INLINE void append(PyObject *value) noexcept {
        if (m_size >= m_capacity)
            expand();
        m_data[m_size++] = value;
    }

    NB_INLINE PyObject *self() const {
        return m_local[0];
    }

    /// Decrease the reference count of all appended objects
    void release() noexcept;

    /// Does the list contain any entries? (besides the 'self' argument)
    bool used() { return m_size != 1; }

    /// Return the size of the cleanup stack
    size_t size() const { return m_size; }

    /// Subscript operator
    PyObject *operator[](size_t index) const { return m_data[index]; }

protected:
    /// Out of memory, expand..
    void expand() noexcept;

protected:
    uint32_t m_size;
    uint32_t m_capacity;
    PyObject **m_data;
    PyObject *m_local[Small];
};

// ========================================================================

/// Raise a runtime error with the given message
#if defined(__GNUC__)
    __attribute__((noreturn, __format__ (__printf__, 1, 2)))
#else
    [[noreturn]]
#endif
NB_CORE void raise(const char *fmt, ...);

/// Raise a type error with the given message
#if defined(__GNUC__)
    __attribute__((noreturn, __format__ (__printf__, 1, 2)))
#else
    [[noreturn]]
#endif
NB_CORE void raise_type_error(const char *fmt, ...);

/// Abort the process with a fatal error
#if defined(__GNUC__)
    __attribute__((noreturn, __format__ (__printf__, 1, 2)))
#else
    [[noreturn]]
#endif
NB_CORE void fail(const char *fmt, ...) noexcept;

/// Raise nanobind::python_error after an error condition was found
[[noreturn]] NB_CORE void raise_python_error();

/// Raise nanobind::next_overload
NB_CORE void raise_next_overload_if_null(void *p);

/// Raise nanobind::cast_error
[[noreturn]] NB_CORE void raise_python_or_cast_error();

// ========================================================================

NB_CORE void nb_module_exec(const char *domain, PyObject *m);
NB_CORE void nb_module_free(void *m);

// ========================================================================

/// Convert a Python object into a Python unicode string
NB_CORE PyObject *str_from_obj(PyObject *o);

/// Convert an UTF8 null-terminated C string into a Python unicode string
NB_CORE PyObject *str_from_cstr(const char *c);

/// Convert an UTF8 C string + size into a Python unicode string
NB_CORE PyObject *str_from_cstr_and_size(const char *c, size_t n);

// ========================================================================

/// Convert a Python object into a Python byte string
NB_CORE PyObject *bytes_from_obj(PyObject *o);

/// Convert an UTF8 null-terminated C string into a Python byte string
NB_CORE PyObject *bytes_from_cstr(const char *c);

/// Convert a memory region into a Python byte string
NB_CORE PyObject *bytes_from_cstr_and_size(const void *c, size_t n);
