struture are generally costly because they use a string comparison on
 *   some platforms. Because it is only used as a fallback for 'type_c2p_fast',
 *   protecting this member via the global `mutex` is sufficient.
 *
 * - `type_c2p_fast`: this data structure is *hot* and mostly read. It maps
 *   `std::type_info` to `type_info *` but uses pointer-based comparisons.
 *   The implementation depends on the Python build.
 *
 * - `translators`: This is an append-to-front-only singly linked list traversed
 *    while raising exceptions. The main concern is losing elements during
 *    concurrent append operations. We assume that this data structure is only
 *    written during module initialization and don't use locking.
 *
 * - `funcs`: data structure for function leak tracking. Not used in
 *   free-threaded mode .
 *
 * - `print_leak_warnings`, `print_implicit_cast_warnings`: simple boolean
 *   flags. No protection against concurrent conflicting updates.
 */

struct nb_internals {
    /// Internal nanobind module
    PyObject *nb_module;

    /// Meta-metaclass of nanobind instances
    PyTypeObject *nb_meta;

    /// Dictionary with nanobind metaclass(es) for different payload sizes
    PyObject *nb_type_dict;

    /// Types of nanobind functions and methods
    PyTypeObject *nb_func, *nb_method, *nb_bound_method;

    /// Property variant for static attributes (created on demand)
    nb_maybe_atomic<PyTypeObject *> nb_static_property = nullptr;
    descrsetfunc nb_static_property_descr_set = nullptr;

#if defined(NB_FREE_THREADED)
    Py_tss_t *nb_static_property_disabled = nullptr;
#else
    bool nb_static_property_disabled = false;
#endif

    /// N-dimensional array wrapper (created on demand)
    nb_maybe_atomic<PyTypeObject *> nb_ndarray = nullptr;

#if defined(NB_FREE_THREADED)
    nb_shard *shards = nullptr;
    size_t shard_mask = 0;

    // Heuristic shard selection (from pybind11 PR #5148 by @colesbury), uses
    // high pointer bits to group allocations by individual threads/cores.
    inline nb_shard &shard(void *p) {
        uintptr_t highbits = ((uintptr_t) p) >> 20;
        size_t index = ((size_t) fmix64((uint64_t) highbits)) & shard_mask;
        return shards[index];
    }
#else
    nb_shard shards[1];
    inline nb_shard &shard(void *) { return shards[0]; }
#endif

#if !defined(NB_FREE_THREADED)
    /// C++ -> Python type map -- fast version based on std::type_info pointer equality
    nb_type_map_fast type_c2p_fast;
#endif

    /// C++ -> Python type map -- slow fallback version based on hashed strings
    nb_type_map_slow type_c2p_slow;

#if !defined(NB_FREE_THREADED)
    /// nb_func/meth instance map for leak reporting (used as set, the value is unused)
    /// In free-threaded mode, functions are immortal and don't require this data structure.
    nb_ptr_map funcs;
#endif

    /// Registered C++ -> Python exception translators
    nb_translator_seq translators;

    /// Should nanobind print leak warnings on exit?
    bool print_leak_warnings = true;

    /// Should nanobind print warnings after implicit cast failures?
    bool print_implicit_cast_warnings = true;

    /// Pointer to a boolean that denotes if nanobind is fully initialized.
    bool *is_alive_ptr = nullptr;

#if defined(Py_LIMITED_API)
    // Cache important functions from PyType_Type and PyProperty_Type
    freefunc PyType_Type_tp_free;
    initproc PyType_Type_tp_init;
    destructor PyType_Type_tp_dealloc;
    setattrofunc PyType_Type_tp_setattro;
    descrgetfunc PyProperty_Type_tp_descr_get;
    descrsetfunc PyProperty_Type_tp_descr_set;
    size_t type_data_offset;
#endif

#if defined(NB_FREE_THREADED)
    PyMutex mutex { };
#endif

    // Size of the 'shards' data structure. Only rarely accessed, hence at the end
    size_t shard_count = 1;

    /// Reference count tracking modules + types + functions using shared state
    nb_maybe_atomic<uint32_t> shared_ref_count = 0;

    /// PyList keeping managed PyObjects alive. Cleared wh