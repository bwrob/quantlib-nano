 get_p, set_p;

        if constexpr (!std::is_same_v<Getter, std::nullptr_t>)
            get_p = cpp_function<T>((detail::forward_t<Getter>) getter,
                                    is_method(), is_getter(),
                                    rv_policy::reference_internal,
                                    detail::filter_getter(extra)...);

        if constexpr (!std::is_same_v<Setter, std::nullptr_t>)
            set_p = cpp_function<T>((detail::forward_t<Setter>) setter,
                                    is_method(), detail::filter_setter(extra)...);

        detail::property_install(m_ptr, name_, get_p.ptr(), set_p.ptr());
        return *this;
    }


    template <typename Getter, typename... Extra>
    NB_INLINE enum_ &def_prop_ro(const char *name_, Getter &&getter,
                                 const Extra &...extra) {
        return def_prop_rw(name_, getter, nullptr, extra...);
    }
};

template <typename Source, typename Target> void implicitly_convertible() {
    if constexpr (!std::is_same_v<Source, Target>) {
        using Caster = detail::make_caster<Source>;
        static_assert(
            !std::is_enum_v<Target> || !detail::is_base_caster_v<Target>,
            "implicitly_convertible(): 'Target' cannot be an enumeration "
            "unless it is opaque.");

        if constexpr (detail::is_base_caster_v<Caster>) {
            detail::implicitly_convertible(&typeid(Source), &typeid(Target));
        } else {
            detail::implicitly_convertible(
                [](PyTypeObject *, PyObject *src,
                   detail::cleanup_list *cleanup) noexcept -> bool {
                    return Caster().from_python(src, detail::cast_flags::convert,
                                                cleanup);
                },
                &typeid(Target));
        }
    }
}

NAMESPACE_END(NB_NAMESPACE)
