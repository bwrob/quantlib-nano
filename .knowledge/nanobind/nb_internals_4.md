#  define NB_SHARD_ALIGNMENT
#endif

/**
 * The following data structure stores information associated with individual
 * instances. In free-threaded builds, it is split into multiple shards to avoid
 * lock contention.
 */
struct NB_SHARD_ALIGNMENT nb_shard {
    /**
     * C++ -> Python instance map
     *
     * This associative data structure maps a C++ instance pointer onto its
     * associated PyObject* (if bit 0 of the map value is zero) or a linked
     * list of type `nb_inst_seq*` (if bit 0 is set---it must be cleared before
     * interpreting the pointer in this case).
     *
     * The latter case occurs when several distinct Python objects reference
     * the same memory address (e.g. a struct and its first member).
     */
    nb_ptr_map inst_c2p;

    /// Dictionary storing keep_alive references
    nb_ptr_map keep_alive;

#if defined(NB_FREE_THREADED)
    PyMutex mutex { };
#endif
};


/**
 * Wraps a std::atomic if free-threading is enabled, otherwise a raw value.
 */
#if defined(NB_FREE_THREADED)
template<typename T>
struct nb_maybe_atomic {
  nb_maybe_atomic(T v) : value(v) {}

  std::atomic<T> value;
  T load_acquire() { return value.load(std::memory_order_acquire); }
  T load_relaxed() { return value.load(std::memory_order_relaxed); }
  void store_release(T w) { value.store(w, std::memory_order_release); }
};
#else
template<typename T>
struct nb_maybe_atomic {
  nb_maybe_atomic(T v) : value(v) {}

  T value;
  T load_acquire() { return value; }
  T load_relaxed() { return value; }
  void store_release(T w) { value = w; }
};
#endif

/**
 * `nb_internals` is the central data structure storing information related to
 * function/type bindings and instances. Separate nanobind extensions within the
 * same NB_DOMAIN furthermore share `nb_internals` to communicate with each
 * other, hence any changes here generally require an ABI version bump.
 *
 * The GIL protects the elements of this data structure from concurrent
 * modification. In free-threaded builds, a combination of locking schemes is
 * needed to achieve good performance.
 *
 * In particular, `inst_c2p` and `type_c2p_fast` are very hot and potentially
 * accessed several times while dispatching a single function call. The other
 * elements are accessed much less frequently and easier to deal with.
 *
 * The following list clarifies locking semantics for each member.
 *
 * - `nb_module`, `nb_meta`, `nb_func`, `nb_method`, `nb_bound_method`,
 *   `*_Type_tp_*`, `shard_count`, `is_alive_ptr`: these are initialized when
 *   loading the first nanobind extension within a domain, which happens within
 *   a critical section. They do not require locking.
 *
 * - `nb_type_dict`: created when the loading the first nanobind extension
 *   within a domain. While the dictionary itself is protected by its own
 *   lock, additional locking is needed to avoid races that create redundant
 *   entries. The `mutex` member is used for this.
 *
 * - `nb_static_property` and `nb_static_propert_descr_set`: created only once
 *   on demand, protected by `mutex`.
 *
 * - `nb_static_property_disabled`: needed to correctly implement assignments to
 *   static properties. Free-threaded builds store this flag using TLS to avoid
 *   concurrent modification.
 *
 * - `nb_static_property` and `nb_static_propert_descr_set`: created only once
 *   on demand, protected by `mutex`.
 *
 * - `nb_ndarray`: created only once on demand, protected by `mutex`.
 *
 * - `inst_c2p`: stores the C++ instance to Python object mapping. This
 *   data struture is *hot* and uses a sharded locking scheme to reduce
 *   lock contention.
 *
 * - `keep_alive`: stores lifetime dependencies (e.g., from the
 *   reference_internal return value policy). This data structure is
 *   potentially hot and shares the sharding scheme of `inst_c2p`.
 *
 * - `type_c2p_slow`: This is the ground-truth source of the `std::type_info`
 *   to `type_info *` mapping. Unrelated to free-threading, lookups into this
 *   data
