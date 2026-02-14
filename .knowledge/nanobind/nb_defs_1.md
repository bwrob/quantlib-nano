#    define NB_TYPE_FROM_METACLASS_IMPL 1 // Custom implementation of PyType_FromMetaclass

#  else

#    define NB_TYPE_FROM_METACLASS_IMPL 0

#  endif
#else

#  define NB_TYPE_FROM_METACLASS_IMPL 1

#  define NB_TYPE_GET_SLOT_IMPL 1
#endif

#if defined(Py_LIMITED_API)

#  define NB_DYNAMIC_VERSION Py_Version
#else

#  define NB_DYNAMIC_VERSION PY_VERSION_HEX
#endif

#define NB_MODULE_SLOTS_0 { 0, nullptr }

#if PY_VERSION_HEX < 0x030C0000

#  define NB_MODULE_SLOTS_1 NB_MODULE_SLOTS_0
#else

#  define NB_MODULE_SLOTS_1                                                    \
    { Py_mod_multiple_interpreters,                                            \
      Py_MOD_MULTIPLE_INTERPRETERS_NOT_SUPPORTED },                            \
    NB_MODULE_SLOTS_0
#endif

#if !defined(NB_FREE_THREADED)

#  define NB_MODULE_SLOTS_2 NB_MODULE_SLOTS_1
#else