e_caster<D>>,
                               const D &, D &&>;

        def_prop_rw(name,
            [p](const T &c) -> const D & { return c.*p; },
            [p](T &c, Q value) { c.*p = (Q) value; },
            extra...);

        return *this;
    }

    template <typename D, typename... Extra>
    NB_INLINE class_ &def_rw_static(const char *name, D *p,
                                    const Extra &...extra) {
        using Q =
            std::conditional_t<detail::is_base_caster_v<detail::make_caster<D>>,
                               const D &, D &&>;

        def_prop_rw_static(name,
            [p](handle) -> const D & { return *p; },
            [p](handle, Q value) { *p = (Q) value; }, extra...);

        return *this;
    }

    template <typename C, typename D, typename... Extra>
    NB_INLINE class_ &def_ro(const char *name, D C::*p,
                             const Extra &...extra) {
        // Unions never satisfy is_base_of, thus the is_same alternative
        static_assert(std::is_base_of_v<C, T> || std::is_same_v<C, T>,
                      "def_ro() requires a (base) class member!");

        def_prop_ro(name,
            [p](const T &c) -> const D & { return c.*p; }, extra...);

        return *this;
    }

    template <typename D, typename... Extra>
    NB_INLINE class_ &def_ro_static(const char *name, D *p,
                                    const Extra &...extra) {
        def_prop_ro_static(name,
            [p](handle) -> const D & { return *p; }, extra...);

        return *this;
    }

    template <detail::op_id id, detail::op_type ot, typename L, typename R, typename... Extra>
    class_ &def(const detail::op_<id, ot, L, R> &op, const Extra&... extra) {
        op.execute(*this, extra...);
        return *this;
    }

    template <detail::op_id id, detail::op_type ot, typename L, typename R, typename... Extra>
    class_ & def_cast(const detail::op_<id, ot, L, R> &op, const Extra&... extra) {
        op.execute_cast(*this, extra...);
        return *this;
    }
};

template <typename T> class enum_ : public object {
public:
    static_assert(std::is_enum_v<T>, "nanobind::enum_<> requires an enumeration type!");

    using Base = class_<T>;
    using Underlying = std::underlying_type_t<T>;

    template <typename... Extra>
    NB_INLINE enum_(handle scope, const char *name, const Extra &... extra) {
        detail::enum_init_data ed { };
        ed.type = &typeid(T);
        ed.scope = scope.ptr();
        ed.name = name;
        ed.flags = std::is_signed_v<Underlying>
                       ? (uint32_t) detail::enum_flags::is_signed
                       : 0;
        (detail::enum_extra_apply(ed, extra), ...);
        m_ptr = detail::enum_create(&ed);
    }

    NB_INLINE enum_ &value(const char *name, T value, const char *doc = nullptr) {
        detail::enum_append(m_ptr, name, (int64_t) value, doc);
        return *this;
    }

    NB_INLINE enum_ &export_values() { detail::enum_export(m_ptr); return *this; }

    template <typename Func, typename... Extra>
    NB_INLINE enum_ &def(const char *name_, Func &&f, const Extra &... extra) {
        cpp_function_def<T>((detail::forward_t<Func>) f, scope(*this),
                            name(name_), is_method(), extra...);
        return *this;
    }

    template <typename Func, typename... Extra>
    NB_INLINE enum_ &def_static(const char *name_, Func &&f,
                                 const Extra &... extra) {
        static_assert(
            !std::is_member_function_pointer_v<Func>,
            "def_static(...) called with a non-static member function pointer");
        cpp_function_def((detail::forward_t<Func>) f, scope(*this), name(name_),
                         extra...);
        return *this;
    }

    template <typename Getter, typename Setter, typename... Extra>
    NB_INLINE enum_ &def_prop_rw(const char *name_, Getter &&getter,
                                 Setter &&setter, const Extra &...extra) {
        object