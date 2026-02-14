#  define check(cond, ...) if (NB_UNLIKELY(!(cond))) nanobind::detail::fail(__VA_ARGS__)
#endif

/// Nanobind function metadata (overloads, etc.)
struct func_data : func_data_prelim_base {
    arg_data *args;
    char *signature;
};

/// Python object representing an instance of a bound C++ type
struct nb_inst { // usually: 24 bytes
    PyObject_HEAD

    /// Offset to the actual instance data
    int32_t offset;

    /// State of the C++ object this instance points to: is it constructed?
    /// can we use it?
    uint8_t state : 2;

    // Values for `state`. Note that the numeric values of these are relied upon
    // for an optimization in `nb_type_get()`.
    static constexpr uint32_t state_uninitialized = 0; // not constructed
    static constexpr uint32_t state_relinquished = 1; // owned by C++, don't touch
    static constexpr uint32_t state_ready = 2; // constructed and usable

    /**
     * The variable 'offset' can either encode an offset relative to the
     * nb_inst address that leads to the instance data, or it can encode a
     * relative offset to a pointer that must be dereferenced to get to the
     * instance data. 'direct' is 'true' in the former case.
     */
    uint8_t direct : 1;

    /// Is the instance data co-located with the Python object?
    uint8_t internal : 1;

    /// Should the destructor be called when this instance is GCed?
    uint8_t destruct : 1;

    /// Should nanobind call 'operator delete' when this instance is GCed?
    uint8_t cpp_delete : 1;

    /// Does this instance use intrusive reference counting?
    uint8_t intrusive : 1;

    /// Does this instance hold references to others? (via internals.keep_alive)
    /// This may be accessed concurrently to 'state', so it must not be in
    /// the same bitfield as 'state'.
    uint8_t clear_keep_alive;

    // That's a lot of unused space. I wonder if there is a good use for it..
    uint16_t unused;
};

static_assert(sizeof(nb_inst) == sizeof(PyObject) + sizeof(uint32_t) * 2);

/// Python object representing a bound C++ function
struct nb_func {
    PyObject_VAR_HEAD
    PyObject* (*vectorcall)(PyObject *, PyObject * const*, size_t, PyObject *);
    uint32_t max_nargs; // maximum value of func_data::nargs for any overload
    bool complex_call;
    bool doc_uniform;
};

/// Python object representing a `nb_ndarray` (which wraps a DLPack ndarray)
struct nb_ndarray {
    PyObject_HEAD
    ndarray_handle *th;
};

/// Python object representing an `nb_method` bound to an instance (analogous to non-public PyMethod_Type)
struct nb_bound_method {
    PyObject_HEAD
    PyObject* (*vectorcall)(PyObject *, PyObject * const*, size_t, PyObject *);
    nb_func *func;
    PyObject *self;
};

/// Pointers require a good hash function to randomize the mapping to buckets
struct ptr_hash {
    size_t operator()(const void *p) const {
        // fmix32/64 from MurmurHash by Austin Appleby (public domain)
        if constexpr (sizeof(void *) == 4)
            return (size_t) fmix32((uint32_t) (uintptr_t) p);
        else
            return (size_t) fmix64((uint64_t) (uintptr_t) p);
    }
};

// Minimal allocator definition, contains only the parts needed by tsl::*
template <typename T> class py_allocator {
public:
    using value_type = T;
    using pointer = T *;
    using size_type = std::size_t;

    py_allocator() = default;
    py_allocator(const py_allocator &) = default;

    template <typename U> py_allocator(const py_allocator<U> &) { }

    pointer allocate(size_type n, const void * /*hint*/ = nullptr) noexcept {
        void *p = PyMem_Malloc(n * sizeof(T));
        if (!p)
            fail("PyMem_Malloc(): out of memory!");
        return static_cast<pointer>(p);
    }

    void deallocate(T *p, size_type /*n*/) noexcept { PyMem_Free(p); }
};

// Linked list of instances with the same pointer address. Usually just 1.
struct nb_inst_seq {
    PyObject *inst;
    nb_inst_seq *next;
};

// Linked list of type aliases when there are multiple 