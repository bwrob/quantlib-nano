 static handle from_cpp(const Value &src, rv_policy policy, cleanup_list *cleanup) noexcept {
        return Caster::from_cpp(src, policy, cleanup);
    }
};

template <typename T>
struct type_caster<T, enable_if_t<std::is_base_of_v<detail::api_tag, T> && !T::nb_typed>> {
public:
    NB_TYPE_CASTER(T, T::Name)

    type_caster() : value(nullptr, ::nanobind::detail::steal_t()) { }

    bool from_python(handle src, uint8_t, cleanup_list *) noexcept {
        if (!isinstance<T>(src))
            return false;

        if constexpr (std::is_base_of_v<object, T>)
            value = borrow<T>(src);
        else
            value = src;

        return true;
    }

    static handle from_cpp(T&& src, rv_policy, cleanup_list *) noexcept {
        if constexpr (std::is_base_of_v<object, T>)
            return src.release();
        else
            return src.inc_ref();
    }

    static handle from_cpp(const T &src, rv_policy, cleanup_list *) noexcept {
        return src.inc_ref();
    }
};

template <typename T> NB_INLINE rv_policy infer_policy(rv_policy policy) {
    if constexpr (is_pointer_v<T>) {
        if (policy == rv_policy::automatic)
            policy = rv_policy::take_ownership;
        else if (policy == rv_policy::automatic_reference)
            policy = rv_policy::reference;
    } else if constexpr (std::is_lvalue_reference_v<T>) {
        if (policy == rv_policy::automatic ||
            policy == rv_policy::automatic_reference)
            policy = rv_policy::copy;
    } else {
        if (policy == rv_policy::automatic ||
            policy == rv_policy::automatic_reference ||
            policy == rv_policy::reference ||
            policy == rv_policy::reference_internal)
            policy = rv_policy::move;
    }
    return policy;
}

template <typename T, typename SFINAE = int> struct type_hook : std::false_type { };

template <typename Type_> struct type_caster_base : type_caster_base_tag {
    using Type = Type_;
    static constexpr auto Name = const_name<Type>();
    template <typename T> using Cast = precise_cast_t<T>;

    NB_INLINE bool from_python(handle src, uint8_t flags,
                               cleanup_list *cleanup) noexcept {
        return nb_type_get(&typeid(Type), src.ptr(), flags, cleanup,
                           (void **) &value);
    }

    template <typename T>
    NB_INLINE static handle from_cpp(T &&value, rv_policy policy,
                                     cleanup_list *cleanup) noexcept {
        Type *ptr;
        if constexpr (is_pointer_v<T>)
            ptr = (Type *) value;
        else
            ptr = (Type *) &value;

        policy = infer_policy<T>(policy);
        const std::type_info *type = &typeid(Type);

        constexpr bool has_type_hook =
            !std::is_base_of_v<std::false_type, type_hook<Type>>;
        if constexpr (has_type_hook)
            type = type_hook<Type>::get(ptr);

        if constexpr (!std::is_polymorphic_v<Type>) {
            return nb_type_put(type, ptr, policy, cleanup);
        } else {
            const std::type_info *type_p =
                (!has_type_hook && ptr) ? &typeid(*ptr) : nullptr;
            return nb_type_put_p(type, type_p, ptr, policy, cleanup);
        }
    }

    template <typename T_>
    bool can_cast() const noexcept {
        return std::is_pointer_v<T_> || (value != nullptr);
    }

    operator Type*() { return value; }

    operator Type&() {
        raise_next_overload_if_null(value);
        return *value;
    }

    operator Type&&() {
        raise_next_overload_if_null(value);
        return (Type &&) *value;
    }

private:
    Type *value;
};

template <typename Type, typename SFINAE>
struct type_caster : type_caster_base<Type> { };

template <bool Convert, typename T>
T cast_impl(handle h) {
    using Caster = detail::make_caster<T>;

    // A returned reference/pointer would usually refer into the type_caster
    // object, which will be destroyed before the returned value can be used,

