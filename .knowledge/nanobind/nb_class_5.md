me T> auto filter_setter(const T &v) { return v; }
    template <typename T> auto filter_setter(const for_setter<T> &v) { return v.value; }
    template <typename T> std::nullptr_t filter_setter(const for_getter<T> &) { return nullptr; }
}

template <typename T, typename... Ts>
class class_ : public object {
public:
    NB_OBJECT_DEFAULT(class_, object, "type", PyType_Check)
    using Type = T;
    using Base  = typename detail::extract<T, detail::is_base,  Ts...>::type;
    using Alias = typename detail::extract<T, detail::is_alias, Ts...>::type;

    static_assert(sizeof(Alias) < (((uint64_t) 1) << 32), "Instance size is too big!");
    static_assert(alignof(Alias) < (1 << 8), "Instance alignment is too big!");
    static_assert(
        sizeof...(Ts) == !std::is_same_v<Base, T> + !std::is_same_v<Alias, T>,
        "nanobind::class_<> was invoked with extra arguments that could not be handled");

    static_assert(
        detail::is_base_caster_v<detail::make_caster<Type>>,
        "You attempted to bind a type that is already intercepted by a type "
        "caster. Having both at the same time is not allowed. Are you perhaps "
        "binding an STL type, while at the same time including a matching "
        "type caster from <nanobind/stl/*>? Or did you perhaps forget to "
        "declare NB_MAKE_OPAQUE(..) to specifically disable the type caster "
        "catch-all for a specific type? Please review the documentation "
        "to learn about the difference between bindings and type casters.");

    template <typename... Extra>
    NB_INLINE class_(handle scope, const char *name, const Extra &... extra) {
        detail::type_init_data d;

        d.flags = 0;
        d.align = (uint8_t) alignof(Alias);
        d.size = (uint32_t) sizeof(Alias);
        d.name = name;
        d.scope = scope.ptr();
        d.type = &typeid(T);

        if constexpr (!std::is_same_v<Base, T>) {
            d.base = &typeid(Base);
            d.flags |= (uint32_t) detail::type_init_flags::has_base;
        }

        if constexpr (detail::is_copy_constructible_v<T>) {
            d.flags |= (uint32_t) detail::type_flags::is_copy_constructible;

            if constexpr (!std::is_trivially_copy_constructible_v<T>) {
                d.flags |= (uint32_t) detail::type_flags::has_copy;
                d.copy = detail::wrap_copy<T>;
            }
        }

        if constexpr (std::is_move_constructible<T>::value) {
            d.flags |= (uint32_t) detail::type_flags::is_move_constructible;

            if constexpr (!std::is_trivially_move_constructible_v<T>) {
                d.flags |= (uint32_t) detail::type_flags::has_move;
                d.move = detail::wrap_move<T>;
            }
        }

        constexpr bool has_never_destruct = (std::is_same_v<Extra, never_destruct> || ...);

        if constexpr (std::is_destructible_v<T> && !has_never_destruct) {
            d.flags |= (uint32_t) detail::type_flags::is_destructible;

            if constexpr (!std::is_trivially_destructible_v<T>) {
                d.flags |= (uint32_t) detail::type_flags::has_destruct;
                d.destruct = detail::wrap_destruct<T>;
            }
        }

        if constexpr (detail::has_shared_from_this_v<T>) {
            d.flags |= (uint32_t) detail::type_flags::has_shared_from_this;
            d.keep_shared_from_this_alive = [](PyObject *self) noexcept {
                // weak_from_this().lock() is equivalent to shared_from_this(),
                // except that it returns an empty shared_ptr instead of
                // throwing an exception if there is no active shared_ptr
                // for this object. (Added in C++17.)
                if (auto sp = inst_ptr<T>(self)->weak_from_this().lock()) {
                    detail::keep_alive(self, new auto(std::move(sp)),
                                       [](void *p) noexcept {
                                           delete (decltype(sp) *) p;
                                     