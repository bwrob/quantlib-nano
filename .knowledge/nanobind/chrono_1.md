#  pragma GCC diagnostic ignored "-Wattributes"
#endif

NAMESPACE_BEGIN(NB_NAMESPACE)
NAMESPACE_BEGIN(detail)

// Unpack a datetime.timedelta object into integer days, seconds, and
// microseconds. Returns true if successful, false if `o` is not a timedelta,
// or throws nb::python_error if something else went wrong.
bool unpack_timedelta(PyObject *o, int *days, int *secs, int *usecs);

// Unpack a datetime.date, datetime.time, or datetime.datetime object into
// integer year, month, day, hour, minute, second, and microsecond fields.
// Time objects will be considered to represent that time on Jan 1, 1970.
// Date objects will be considered to represent midnight on that date.
// Returns true if succesful, false if `o` is not a date, time, or datetime,
// or throws nb::python_error if something else went wrong.
bool unpack_datetime(PyObject *o, int *year, int *month, int *day,
                     int *hour, int *minute, int *second,
                     int *usec);

// Create a datetime.timedelta object from integer days, seconds, and
// microseconds.  Returns a new reference, or nullptr and sets the
// Python error indicator on error.
PyObject* pack_timedelta(int days, int secs, int usecs) noexcept;

// Create a timezone-naive datetime.datetime object from its components.
// Returns a new reference, or nullptr and sets the Python error indicator
// on error.
PyObject* pack_datetime(int year, int month, int day,
                        int hour, int minute, int second,
                        int usec) noexcept;

// Note: Several of the functions defined in this header are marked
// 'inline' for linkage purposes (since they might be in multiple
// translation units and the linker should pick one) but NB_NOINLINE
// because we don't want the bloat of actually inlining them. They are
// defined in this header instead of in the built nanobind library in
// order to avoid increasing the library size for users who don't care
// about datetimes.

#if defined(Py_LIMITED_API) || defined(PYPY_VERSION)

struct datetime_types_t {
    // Types defined by the datetime module
    handle datetime;
    handle time;
    handle date;
    handle timedelta;

    // Ensure that the above four handles point to valid Python objects.
    // If unable, throw nb::python_error.
    void ensure_ready() {
        if (datetime.is_valid())
            return;

        object mod = module_::import_("datetime");
        object datetime_o = mod.attr("datetime");
        object time_o = mod.attr("time");
        object date_o = mod.attr("date");
        object timedelta_o = mod.attr("timedelta");

        // Leak references to these datetime types. We could improve upon
        // this by storing them in the internals structure and decref'ing
        // in internals_cleanup(), but it doesn't seem worthwhile for
        // something this fundamental. We can't store nb::object in this
        // structure because it might be destroyed after the Python
        // interpreter has finalized.
        datetime = datetime_o.release();
        time = time_o.release();
        date = date_o.release();
        timedelta = timedelta_o.release();
    }
};

inline datetime_types_t datetime_types;

// Set *dest to the integer value of getattr(o, name). Returns true
// on success, false and sets the Python error indicator on failure.
// The attribute value must be a Python integer object; other types
// of numbers are not supported.
NB_NOINLINE inline bool set_from_int_attr(int *dest, PyObject *o,
                                          const char *name) noexcept {
    PyObject *value = PyObject_GetAttrString(o, name);
    if (!value)
        return false;
    long lval = PyLong_AsLong(value);
    if (lval == -1 && PyErr_Occurred()) {
        Py_DECREF(value);
        return false;
    }
    if (lval < std::numeric_limits<int>::min() ||
        lval > std::numeric_limits<int>::max()) {
        PyErr_Format(PyExc_OverflowError,
                     "%R attribute '%s' (%R) doe
