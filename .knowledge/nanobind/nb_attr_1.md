;

struct type_slots_callback {
    using cb_t = void (*)(const detail::type_init_data *t,
                          PyType_Slot *&slots, size_t max_slots) noexcept;
    type_slots_callback(cb_t callback) : callback(callback) { }
    cb_t callback;
};

struct sig {
    const char *value;
    sig(const char *value) : value(value) { }
};

struct is_getter { };

template <typename Policy> struct call_policy final {};

NAMESPACE_BEGIN(literals)
constexpr arg operator""_a(const char *name, size_t) { return arg(name); }
NAMESPACE_END(literals)

NAMESPACE_BEGIN(detail)

enum class func_flags : uint32_t {
    /* Low 3 bits reserved for return value policy */

    /// Did the user specify a name for this function, or is it anonymous?
    has_name = (1 << 4),
    /// Did the user specify a scope in which this function should be installed?
    has_scope = (1 << 5),
    /// Did the user specify a docstring?
    has_doc = (1 << 6),
    /// Did the user specify nb::arg/arg_v annotations for all arguments?
    has_args = (1 << 7),
    /// Does the function signature contain an *args-style argument?
    has_var_args = (1 << 8),
    /// Does the function signature contain an *kwargs-style argument?
    has_var_kwargs = (1 << 9),
    /// Is this function a method of a class?
    is_method = (1 << 10),
    /// Is this function a method called __init__? (automatically generated)
    is_constructor = (1 << 11),
    /// Can this constructor be used to perform an implicit conversion?
    is_implicit = (1 << 12),
    /// Is this function an arithmetic operator?
    is_operator = (1 << 13),
    /// When the function is GCed, do we need to call func_data_prelim::free_capture?
    has_free = (1 << 14),
    /// Should the func_new() call return a new reference?
    return_ref = (1 << 15),
    /// Does this overload specify a custom function signature (for docstrings, typing)
    has_signature = (1 << 16),
    /// Does this function potentially modify the elements of the PyObject*[] array
    /// representing its arguments? (nb::keep_alive() or call_policy annotations)
    can_mutate_args = (1 << 17)
};

enum cast_flags : uint8_t {
    // Enable implicit conversions (code assumes this has value 1, don't reorder..)
    convert = (1 << 0),

    // Passed to the 'self' argument in a constructor call (__init__)
    construct = (1 << 1),

    // Indicates that the function dispatcher should accept 'None' arguments
    accepts_none = (1 << 2),

    // Indicates that this cast is performed by nb::cast or nb::try_cast.
    // This implies that objects added to the cleanup list may be
    // released immediately after the caster's final output value is
    // obtained, i.e., before it is used.
    manual = (1 << 3)
};


struct arg_data {
    const char *name;
    const char *signature;
    PyObject *name_py;
    PyObject *value;
    uint8_t flag;
};

struct func_data_prelim_base {
    // A small amount of space to capture data used by the function/closure
    void *capture[3];

    // Callback to clean up the 'capture' field
    void (*free_capture)(void *);

    /// Implementation of the function call
    PyObject *(*impl)(void *, PyObject **, uint8_t *, rv_policy,
                      cleanup_list *);

    /// Function signature description
    const char *descr;

    /// C++ types referenced by 'descr'
    const std::type_info **descr_types;

    /// Supplementary flags
    uint32_t flags;

    /// Total number of parameters accepted by the C++ function; nb::args
    /// and nb::kwargs parameters are counted as one each. If the
    /// 'has_args' flag is set, then there is one arg_data structure
    /// for each of these.
    uint16_t nargs;

    /// Number of parameters to the C++ function that may be filled from
    /// Python positional arguments without additional ceremony.
    /// nb::args and nb::kwargs parameters are not counted in this total, nor
    /// are any parameters after nb::args or after a nb::kw_only annotation.
    /// The parameters counted