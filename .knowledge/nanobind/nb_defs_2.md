#  define NB_MODULE_SLOTS_2                                                    \
   { Py_mod_gil, Py_MOD_GIL_NOT_USED },                                        \
   NB_MODULE_SLOTS_1
#endif

#define NB_NONCOPYABLE(X)                                                      \
    X(const X &) = delete;                                                     \
    X &operator=(const X &) = delete;

// Helper macros to ensure macro arguments are expanded before token pasting/stringification
#define NB_MODULE_IMPL(name, variable) NB_MODULE_IMPL2(name, variable)
#define NB_MODULE_IMPL2(name, variable)                                        \
    static void nanobind_##name##_exec_impl(nanobind::module_);                \
    static int nanobind_##name##_exec(PyObject *m) {                           \
        nanobind::detail::nb_module_exec(NB_DOMAIN_STR, m);                    \
        try {                                                                  \
            nanobind_##name##_exec_impl(                                       \
                nanobind::borrow<nanobind::module_>(m));                       \
            return 0;                                                          \
        } catch (nanobind::python_error &e) {                                  \
            e.restore();                                                       \
            nanobind::chain_error(                                             \
                PyExc_ImportError,                                             \
                "Encountered an error while initializing the extension.");     \
        } catch (const std::exception &e) {                                    \
            PyErr_SetString(PyExc_ImportError, e.what());                      \
        }                                                                      \
        return -1;                                                             \
    }                                                                          \
    static PyModuleDef_Slot nanobind_##name##_slots[] = {                      \
        { Py_mod_exec, (void *) nanobind_##name##_exec },                      \
        NB_MODULE_SLOTS_2                                                      \
    };                                                                         \
    static struct PyModuleDef nanobind_##name##_module = {                     \
        PyModuleDef_HEAD_INIT, #name, nullptr, 0, nullptr,                     \
        nanobind_##name##_slots, nullptr, nullptr,                             \
        nanobind::detail::nb_module_free                                       \
    };                                                                         \
    extern "C" [[maybe_unused]] NB_EXPORT PyObject *PyInit_##name(void);       \
    extern "C" PyObject *PyInit_##name(void) {                                 \
        return PyModuleDef_Init(&nanobind_##name##_module);                    \
    }                                                                          \
    void nanobind_##name##_exec_impl(nanobind::module_ variable)

#define NB_MODULE(name, variable) NB_MODULE_IMPL(name, variable)
