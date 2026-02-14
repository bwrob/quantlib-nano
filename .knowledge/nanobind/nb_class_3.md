f T");
    }
};

template <typename... Args> struct init : def_visitor<init<Args...>> {
    template <typename T, typename... Ts> friend class class_;
    NB_INLINE init() {}

private:
    template <typename Class, typename... Extra>
    NB_INLINE static void execute(Class &cl, const Extra&... extra) {
        using Type = typename Class::Type;
        using Alias = typename Class::Alias;
        cl.def(
            "__init__",
            [](pointer_and_handle<Type> v, Args... args) {
                if constexpr (!std::is_same_v<Type, Alias> &&
                              std::is_constructible_v<Type, Args...>) {
                    if (!detail::nb_inst_python_derived(v.h.ptr())) {
                        new (v.p) Type{ (detail::forward_t<Args>) args... };
                        return;
                    }
                }
                new ((void *) v.p) Alias{ (detail::forward_t<Args>) args... };
            },
            extra...);
    }
};

template <typename Arg> struct init_implicit : def_visitor<init_implicit<Arg>> {
    template <typename T, typename... Ts> friend class class_;
    NB_INLINE init_implicit() { }

private:
    template <typename Class, typename... Extra>
    NB_INLINE static void execute(Class &cl, const Extra&... extra) {
        using Type = typename Class::Type;
        using Alias = typename Class::Alias;

        cl.def(
            "__init__",
            [](pointer_and_handle<Type> v, Arg arg) {
                if constexpr (!std::is_same_v<Type, Alias> &&
                              std::is_constructible_v<Type, Arg>) {
                    if (!detail::nb_inst_python_derived(v.h.ptr())) {
                        new ((Type *) v.p) Type{ (detail::forward_t<Arg>) arg };
                        return;
                    }
                }
                new ((Alias *) v.p) Alias{ (detail::forward_t<Arg>) arg };
            }, is_implicit(), extra...);

        using Caster = detail::make_caster<Arg>;

        if constexpr (!detail::is_class_caster_v<Caster>) {
            detail::implicitly_convertible(
                [](PyTypeObject *, PyObject *src,
                   detail::cleanup_list *cleanup) noexcept -> bool {
                    return Caster().from_python(
                        src, detail::cast_flags::convert, cleanup);
                },
                &typeid(Type));
        }
    }
};

namespace detail {
    // This is 'inline' so we can define it in a header and not pay
    // for it if unused, and also 'noinline' so we don't generate
    // multiple copies and produce code bloat.
    NB_NOINLINE inline void wrap_base_new(handle cls, bool do_wrap) {
        if (PyCFunction_Check(cls.attr("__new__").ptr())) {
            if (do_wrap) {
                cpp_function_def(
                    [](handle type) {
                        if (!type_check(type))
                            throw cast_error();
                        return inst_alloc(type);
                    },
                    scope(cls), name("__new__"));
            }
        } else {
            if (!do_wrap) {
                // We already defined the wrapper, so this zero-arg overload
                // would be unreachable. Raise an error rather than hiding it.
                raise("nanobind: %s must define its zero-argument __new__ "
                      "before any other overloads", type_name(cls).c_str());
            }
        }
    }

    // Call policy that ensures __new__ returns an instance of the correct
    // Python type, even when deriving from the C++ class in Python
    struct new_returntype_fixup_policy {
        static inline void precall(PyObject **, size_t,
                                   detail::cleanup_list *) {}
        NB_NOINLINE static inline void postcall(PyObject **args, size_t,
                                                PyObject *&ret) {
            handle type_requested = args[0];
            if (ret == nullptr || !type_requested.is_type())
                