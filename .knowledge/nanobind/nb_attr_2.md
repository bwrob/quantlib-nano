 here may be either named (nb::arg("name")) or
    /// unnamed (nb::arg()).  If unnamed, they are effectively positional-only.
    /// nargs_pos is always <= nargs.
    uint16_t nargs_pos;

    // ------- Extra fields -------

    const char *name;
    const char *doc;
    PyObject *scope;
};

template<size_t Size> struct func_data_prelim : func_data_prelim_base {
    arg_data args[Size];
};

template<> struct func_data_prelim<0> : func_data_prelim_base {};


template <typename F>
NB_INLINE void func_extra_apply(F &f, const name &name, size_t &) {
    f.name = name.value;
    f.flags |= (uint32_t) func_flags::has_name;
}

template <typename F>
NB_INLINE void func_extra_apply(F &f, const scope &scope, size_t &) {
    f.scope = scope.value;
    f.flags |= (uint32_t) func_flags::has_scope;
}

template <typename F>
NB_INLINE void func_extra_apply(F &f, const sig &s, size_t &) {
    f.flags |= (uint32_t) func_flags::has_signature;
    f.name = s.value;
}

template <typename F>
NB_INLINE void func_extra_apply(F &f, const char *doc, size_t &) {
    f.doc = doc;
    f.flags |= (uint32_t) func_flags::has_doc;
}

template <typename F>
NB_INLINE void func_extra_apply(F &f, is_method, size_t &) {
    f.flags |= (uint32_t) func_flags::is_method;
}

template <typename F>
NB_INLINE void func_extra_apply(F &, is_getter, size_t &) { }

template <typename F>
NB_INLINE void func_extra_apply(F &f, is_implicit, size_t &) {
    f.flags |= (uint32_t) func_flags::is_implicit;
}

template <typename F>
NB_INLINE void func_extra_apply(F &f, is_operator, size_t &) {
    f.flags |= (uint32_t) func_flags::is_operator;
}

template <typename F>
NB_INLINE void func_extra_apply(F &f, rv_policy pol, size_t &) {
    f.flags = (f.flags & ~0b111) | (uint16_t) pol;
}

template <typename F>
NB_INLINE void func_extra_apply(F &, std::nullptr_t, size_t &) { }

template <typename F>
NB_INLINE void func_extra_apply(F &f, const arg &a, size_t &index) {
    uint8_t flag = 0;
    if (a.none_)
        flag |= (uint8_t) cast_flags::accepts_none;
    if (a.convert_)
        flag |= (uint8_t) cast_flags::convert;

    arg_data &arg = f.args[index];
    arg.flag |= flag;
    arg.name = a.name_;
    arg.signature = a.signature_;
    arg.value = nullptr;
    index++;
}
// arg_locked will select the arg overload; the locking is added statically
// in nb_func.h

template <typename F>
NB_INLINE void func_extra_apply(F &f, const arg_v &a, size_t &index) {
    arg_data &ad = f.args[index];
    func_extra_apply(f, (const arg &) a, index);
    ad.value = a.value.ptr();
}
template <typename F>
NB_INLINE void func_extra_apply(F &f, const arg_locked_v &a, size_t &index) {
    arg_data &ad = f.args[index];
    func_extra_apply(f, (const arg_locked &) a, index);
    ad.value = a.value.ptr();
}

template <typename F>
NB_INLINE void func_extra_apply(F &, kw_only, size_t &) {}

template <typename F>
NB_INLINE void func_extra_apply(F &, lock_self, size_t &) {}

template <typename F, typename... Ts>
NB_INLINE void func_extra_apply(F &, call_guard<Ts...>, size_t &) {}

template <typename F, size_t Nurse, size_t Patient>
NB_INLINE void func_extra_apply(F &f, nanobind::keep_alive<Nurse, Patient>, size_t &) {
    f.flags |= (uint32_t) func_flags::can_mutate_args;
}

template <typename F, typename Policy>
NB_INLINE void func_extra_apply(F &f, call_policy<Policy>, size_t &) {
    f.flags |= (uint32_t) func_flags::can_mutate_args;
}

template <typename... Ts> struct func_extra_info {
    using call_guard = void;
    static constexpr bool pre_post_hooks = false;
    static constexpr size_t nargs_locked = 0;
};

template <typename T, typename... Ts> struct func_extra_info<T, Ts...>
    : func_extra_info<Ts...> { };

template <typename... Cs, typename... Ts>
struct func_extra_info<call_guard<Cs...>, Ts...> : func_extra_info<Ts...> {
    static_assert(std::is_same_v<typename func_extra_info<Ts...>::call_guard, void>,
                  "call_guard<> can only be specified once!");
    using call_guard = nanobi
