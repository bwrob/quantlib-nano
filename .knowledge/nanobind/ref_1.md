c constexpr bool IsClass = true;
    NB_TYPE_CASTER(ref<T>, Caster::Name)

    bool from_python(handle src, uint8_t flags,
                     cleanup_list *cleanup) noexcept {
        Caster caster;
        if (!caster.from_python(src, flags, cleanup))
            return false;

        value = Value(caster.operator T *());
        return true;
    }

    static handle from_cpp(const ref<T> &value, rv_policy policy,
                           cleanup_list *cleanup) noexcept {
        if constexpr (std::is_base_of_v<intrusive_base, T>)
            if (policy != rv_policy::copy && policy != rv_policy::move && value.get())
                if (PyObject* obj = value->self_py())
                    return handle(obj).inc_ref();

        return Caster::from_cpp(value.get(), policy, cleanup);
    }
};
NAMESPACE_END(detail)
#endif

NAMESPACE_END(nanobind)