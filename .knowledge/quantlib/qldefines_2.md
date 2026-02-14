#    define QL_DEPRECATED __attribute__((deprecated))

#    define QL_DEPRECATED_DISABLE_WARNING                                 \
        _Pragma("clang diagnostic push")                                  \
        _Pragma("clang diagnostic ignored \"-Wdeprecated-declarations\"")

#    define QL_DEPRECATED_ENABLE_WARNING \
        _Pragma("clang diagnostic pop")
#elif defined(__GNUC__)

#    define QL_DEPRECATED __attribute__((deprecated))

#    define QL_DEPRECATED_DISABLE_WARNING                               \
        _Pragma("GCC diagnostic push")                                  \
        _Pragma("GCC diagnostic ignored \"-Wdeprecated-declarations\"")

#    define QL_DEPRECATED_ENABLE_WARNING \
        _Pragma("GCC diagnostic pop")
#else
// we don't know how to enable it, just define the macros away

#    define QL_DEPRECATED

#    define QL_DEPRECATED_DISABLE_WARNING

#    define QL_DEPRECATED_ENABLE_WARNING
#endif
// clang-format on

#endif
