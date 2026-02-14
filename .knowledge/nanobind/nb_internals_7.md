#  define NB_SLOT(type, name) internals->type##_##name
#else

#  define NB_SLOT(type, name) type.name
#endif

extern nb_internals *internals;
extern PyTypeObject *nb_meta_cache;

extern char *type_name(const std::type_info *t);

// Forward declarations
extern PyObject *inst_new_ext(PyTypeObject *tp, void *value);
extern PyObject *inst_new_int(PyTypeObject *tp, PyObject *args, PyObject *kwds);
extern PyTypeObject *nb_static_property_tp() noexcept;
extern type_data *nb_type_c2p(nb_internals *internals,
                              const std::type_info *type);
extern void nb_type_unregister(type_data *t) noexcept;

extern PyObject *call_one_arg(PyObject *fn, PyObject *arg) noexcept;

/// Fetch the nanobind function record from a 'nb_func' instance
NB_INLINE func_data *nb_func_data(void *o) {
    return (func_data *) (((char *) o) + sizeof(nb_func));
}

#if defined(Py_LIMITED_API)
extern type_data *nb_type_data_static(PyTypeObject *o) noexcept;
#endif

/// Fetch the nanobind type record from a 'nb_type' instance
NB_INLINE type_data *nb_type_data(PyTypeObject *o) noexcept{
    #if !defined(Py_LIMITED_API)
        return (type_data *) (((char *) o) + sizeof(PyHeapTypeObject));
    #else
        return nb_type_data_static(o);
    #endif
}

inline void *inst_ptr(nb_inst *self) {
    void *ptr = (void *) ((intptr_t) self + self->offset);
    return self->direct ? ptr : *(void **) ptr;
}

template <typename T> struct scoped_pymalloc {
    scoped_pymalloc(size_t size = 1, size_t extra_bytes = 0) {
        // Tip: construct objects in the extra bytes using placement new.
        ptr = (T *) PyMem_Malloc(size * sizeof(T) + extra_bytes);
        if (!ptr)
            fail("scoped_pymalloc(): could not allocate %llu bytes of memory!",
                 (unsigned long long) (size * sizeof(T) + extra_bytes));
    }
    ~scoped_pymalloc() { PyMem_Free(ptr); }
    T *release() {
        T *temp = ptr;
        ptr = nullptr;
        return temp;
    }
    T *get() const { return ptr; }
    T &operator[](size_t i) { return ptr[i]; }
    T *operator->() { return ptr; }
private:
    T *ptr{ nullptr };
};


/// RAII lock/unlock guards for free-threaded builds
#if defined(NB_FREE_THREADED)
struct lock_shard {
    nb_shard &s;
    lock_shard(nb_shard &s) : s(s) { PyMutex_Lock(&s.mutex); }
    ~lock_shard() { PyMutex_Unlock(&s.mutex); }
};
struct lock_internals {
    nb_internals *i;
    lock_internals(nb_internals *i) : i(i) { PyMutex_Lock(&i->mutex); }
    ~lock_internals() { PyMutex_Unlock(&i->mutex); }
};
struct unlock_internals {
    nb_internals *i;
    unlock_internals(nb_internals *i) : i(i) { PyMutex_Unlock(&i->mutex); }
    ~unlock_internals() { PyMutex_Lock(&i->mutex); }
};
#else
struct lock_shard { lock_shard(nb_shard &) { } };
struct lock_internals { lock_internals(nb_internals *) { } };
struct unlock_internals { unlock_internals(nb_internals *) { } };
struct lock_obj { lock_obj(PyObject *) { } };
#endif

extern char *strdup_check(const char *);
extern void *malloc_check(size_t size);

extern char *extract_name(const char *cmd, const char *prefix, const char *s);


NAMESPACE_END(detail)
NAMESPACE_END(NB_NAMESPACE)