en shared_ref_count
    /// reaches 0.
    PyObject *lifeline = nullptr;
};

// Names for the PyObject* entries in the per-module state array.
// These names are scoped, but will implicitly convert to int.
struct pyobj_name {
    enum : int {
        value_str = 0,      // string "value"
        copy_str,           // string "copy"
        clone_str,          // string "clone"
        array_str,          // string "array"
        from_dlpack_str,    // string "from_dlpack"
        dunder_dlpack_str,  // string "__dlpack__"
        max_version_str,    // string "max_version"
        dl_device_str,      // string "dl_device"
        string_count,

        copy_tpl = string_count,  // tuple ("copy")
        max_version_tpl, // tuple ("max_version")
        dl_cpu_tpl,      // tuple (1, 0), which corresponds to nb::device::cpu
        dl_version_tpl,  // tuple (dlpack::major_version, dlpack::minor_version)
        total_count
    };
};

extern PyObject *static_pyobjects[];

extern void internals_inc_ref();
extern void internals_dec_ref();

/// Append 'o' to the lifeline and transfer ownership to it
inline void new_object(nb_internals *p, PyObject *o) {
    PyList_Append(p->lifeline, o);
    Py_DECREF(o);
}

/// Create a type via PyType_FromSpec and transfer ownership to the lifeline
inline PyTypeObject *new_type(nb_internals *p, PyType_Spec *spec) {
    PyTypeObject *tp = (PyTypeObject *) PyType_FromSpec(spec);
    if (tp)
        new_object(p, (PyObject *) tp);
    return tp;
}

/// Convenience macro to potentially access cached functions
#if defined(Py_LIMITED_API)