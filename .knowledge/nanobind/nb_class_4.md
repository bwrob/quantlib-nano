return; // somethign strange about this call; don't meddle
            handle type_created = Py_TYPE(ret);
            if (type_created.is(type_requested))
                return; // already created the requested type so no fixup needed

            if (type_check(type_created) &&
                PyType_IsSubtype((PyTypeObject *) type_requested.ptr(),
                                 (PyTypeObject *) type_created.ptr()) &&
                type_info(type_created) == type_info(type_requested)) {
                // The new_ constructor returned an instance of a bound type T.
                // The user wanted an instance of some python subclass S of T.
                // Since both wrap the same C++ type, we can satisfy the request
                // by returning a pyobject of type S that wraps a C++ T*, and
                // handling the lifetimes by having that pyobject keep the
                // already-created T pyobject alive.
                object wrapper = inst_reference(type_requested,
                                                inst_ptr<void>(ret),
                                                /* parent = */ ret);
                handle(ret).dec_ref();
                ret = wrapper.release().ptr();
            }
        }
    };
}

template <typename Func, typename Sig = detail::function_signature_t<Func>>
struct new_;

template <typename Func, typename Return, typename... Args>
struct new_<Func, Return(Args...)> : def_visitor<new_<Func, Return(Args...)>> {
    std::remove_reference_t<Func> func;

    new_(Func &&f) : func((detail::forward_t<Func>) f) {}

    template <typename Class, typename... Extra>
    NB_INLINE void execute(Class &cl, const Extra&... extra) {
        // If this is the first __new__ overload we're defining, then wrap
        // nanobind's built-in __new__ so we overload with it instead of
        // replacing it; this is important for pickle support.
        // We can't do this if the user-provided __new__ takes no
        // arguments, because it would make an ambiguous overload set.
        constexpr size_t num_defaults =
            ((std::is_same_v<Extra, arg_v> ||
              std::is_same_v<Extra, arg_locked_v>) + ... + 0);
        constexpr size_t num_varargs =
            ((std::is_same_v<detail::intrinsic_t<Args>, args> ||
              std::is_same_v<detail::intrinsic_t<Args>, kwargs>) + ... + 0);
        detail::wrap_base_new(cl, sizeof...(Args) > num_defaults + num_varargs);

        auto wrapper = [func_ = (detail::forward_t<Func>) func](handle, Args... args) {
            return func_((detail::forward_t<Args>) args...);
        };

        auto policy = call_policy<detail::new_returntype_fixup_policy>();
        if constexpr ((std::is_base_of_v<arg, Extra> || ...)) {
            // If any argument annotations are specified, add another for the
            // extra class argument that we don't forward to Func, so visible
            // arg() annotations stay aligned with visible function arguments.
            cl.def_static("__new__", std::move(wrapper), arg("cls"), extra...,
                          policy);
        } else {
            cl.def_static("__new__", std::move(wrapper), extra..., policy);
        }
        cl.def("__init__", [](handle, Args...) {}, extra...);
    }
};
template <typename Func> new_(Func&& f) -> new_<Func>;

template <typename T> struct for_setter {
    T value;
    for_setter(const T &value) : value(value) { }
};

template <typename T> struct for_getter {
    T value;
    for_getter(const T &value) : value(value) { }
};

template <typename T> for_getter(T) -> for_getter<std::decay_t<T>>;
template <typename T> for_setter(T) -> for_setter<std::decay_t<T>>;

namespace detail {
    template <typename T> auto filter_getter(const T &v) { return v; }
    template <typename T> auto filter_getter(const for_getter<T> &v) { return v.value; }
    template <typename T> std::nullptr_t filter_getter(const for_setter<T> &) { return nullptr; }

    template <typena
