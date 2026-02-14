aking or returning ``ref<T>``-typed values.
 */
struct NB_INTRUSIVE_EXPORT intrusive_counter {
public:
    intrusive_counter() noexcept = default;

    // The counter value is not affected by copy/move assignment/construction
    intrusive_counter(const intrusive_counter &) noexcept { }
    intrusive_counter(intrusive_counter &&) noexcept { }
    intrusive_counter &operator=(const intrusive_counter &) noexcept { return *this; }
    intrusive_counter &operator=(intrusive_counter &&) noexcept { return *this; }

    /// Increase the object's reference count
    void inc_ref() const noexcept;

    /// Decrease the object's reference count, return ``true`` if it should be deallocated
    bool dec_ref() const noexcept;

    /// Return the Python object associated with this instance (or NULL)
    PyObject *self_py() const noexcept;

    /// Set the Python object associated with this instance
    void set_self_py(PyObject *self) noexcept;

protected:
    /**
     * \brief Mutable counter. Note that the value ``1`` actually encodes
     * a zero reference count (see the file ``counter.inl`` for details).
     */
    mutable uintptr_t m_state = 1;
};

static_assert(
    sizeof(intrusive_counter) == sizeof(void *),
    "The intrusive_counter class should always have the same size as a pointer.");

/// Reference-counted base type of an object hierarchy
class NB_INTRUSIVE_EXPORT intrusive_base {
public:
    /// Increase the object's reference count
    void inc_ref() const noexcept { m_ref_count.inc_ref(); }

    /// Decrease the object's reference count, return ``true`` if it should be deallocated
    bool dec_ref() const noexcept { return m_ref_count.dec_ref(); }

    /// Set the Python object associated with this instance
    void set_self_py(PyObject *self) noexcept { m_ref_count.set_self_py(self); }

    /// Return the Python object associated with this instance (or NULL)
    PyObject *self_py() const noexcept { return m_ref_count.self_py(); }

    /// Virtual destructor
    virtual ~intrusive_base() = default;

private:
    mutable intrusive_counter m_ref_count;
};

/**
 * \brief Increase the reference count of an intrusively reference-counted
 * object ``o`` if ``o`` is non-NULL.
 */
inline void inc_ref(const intrusive_base *o) noexcept {
    if (o)
        o->inc_ref();
}

/**
 * \brief Decrease the reference count and potentially delete an intrusively
 * reference-counted object ``o`` if ``o`` is non-NULL.
 */
inline void dec_ref(const intrusive_base *o) noexcept {
    if (o && o->dec_ref())
        delete o;
}

/**
 * \brief Install Python reference counting handlers
 *
 * The ``intrusive_counter`` class is designed so that the dependency on Python is
 * *optional*: the code compiles in ordinary C++ projects, in which case the
 * Python reference counting functionality will simply not be used.
 *
 * Python binding code must invoke ``intrusive_init`` once to supply two
 * functions that increase and decrease the reference count of a Python object,
 * while ensuring that the GIL is held.
 */
extern NB_INTRUSIVE_EXPORT
void intrusive_init(void (*intrusive_inc_ref_py)(PyObject *) noexcept,
                    void (*intrusive_dec_ref_py)(PyObject *) noexcept);

NAMESPACE_END(nanobind)