  });
                    return true;
                }
                return false;
            };
        }

        (detail::type_extra_apply(d, extra), ...);

        m_ptr = detail::nb_type_new(&d);
    }

    template <typename Func, typename... Extra>
    NB_INLINE class_ &def(const char *name_, Func &&f, const Extra &... extra) {
        cpp_function_def<T>((detail::forward_t<Func>) f, scope(*this),
                            name(name_), is_method(), extra...);
        return *this;
    }

    template <typename Visitor, typename... Extra>
    NB_INLINE class_ &def(def_visitor<Visitor> &&arg, const Extra &... extra) {
        static_cast<Visitor&&>(arg).execute(*this, extra...);
        return *this;
    }

    template <typename Func, typename... Extra>
    NB_INLINE class_ &def_static(const char *name_, Func &&f,
                                 const Extra &... extra) {
        static_assert(
            !std::is_member_function_pointer_v<Func>,
            "def_static(...) called with a non-static member function pointer");
        cpp_function_def((detail::forward_t<Func>) f, scope(*this), name(name_),
                         extra...);
        return *this;
    }

    template <typename Getter, typename Setter, typename... Extra>
    NB_INLINE class_ &def_prop_rw(const char *name_, Getter &&getter,
                                  Setter &&setter, const Extra &...extra) {
        object get_p, set_p;

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

    template <typename Getter, typename Setter, typename... Extra>
    NB_INLINE class_ &def_prop_rw_static(const char *name_, Getter &&getter,
                                         Setter &&setter,
                                         const Extra &...extra) {
        object get_p, set_p;

        if constexpr (!std::is_same_v<Getter, std::nullptr_t>)
            get_p = cpp_function((detail::forward_t<Getter>) getter, is_getter(),
                                 rv_policy::reference,
                                 detail::filter_getter(extra)...);

        if constexpr (!std::is_same_v<Setter, std::nullptr_t>)
            set_p = cpp_function((detail::forward_t<Setter>) setter,
                                 detail::filter_setter(extra)...);

        detail::property_install_static(m_ptr, name_, get_p.ptr(), set_p.ptr());
        return *this;
    }

    template <typename Getter, typename... Extra>
    NB_INLINE class_ &def_prop_ro(const char *name_, Getter &&getter,
                                  const Extra &...extra) {
        return def_prop_rw(name_, getter, nullptr, extra...);
    }

    template <typename Getter, typename... Extra>
    NB_INLINE class_ &def_prop_ro_static(const char *name_,
                                         Getter &&getter,
                                         const Extra &...extra) {
        return def_prop_rw_static(name_, getter, nullptr, extra...);
    }

    template <typename C, typename D, typename... Extra>
    NB_INLINE class_ &def_rw(const char *name, D C::*p,
                             const Extra &...extra) {
        // Unions never satisfy is_base_of, thus the is_same alternative
        static_assert(std::is_base_of_v<C, T> || std::is_same_v<C, T>,
                      "def_rw() requires a (base) class member!");

        using Q =
            std::conditional_t<detail::is_base_caster_v<detail::mak
