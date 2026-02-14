xcept {
    ((T *) value)->~T();
}

template <typename, template <typename, typename> typename, typename...>
struct extract;

template <typename T, template <typename, typename> typename Pred>
struct extract<T, Pred> {
    using type = T;
};

template <typename T, template <typename, typename> typename Pred,
          typename Tv, typename... Ts>
struct extract<T, Pred, Tv, Ts...> {
    using type = std::conditional_t<
        Pred<T, Tv>::value,
        Tv,
        typename extract<T, Pred, Ts...>::type
    >;
};

template <typename T, typename Arg> using is_alias = std::is_base_of<T, Arg>;
template <typename T, typename Arg> using is_base = std::is_base_of<Arg, T>;

enum op_id : int;
enum op_type : int;
struct undefined_t;
template <op_id id, op_type ot, typename L = undefined_t, typename R = undefined_t> struct op_;

// The header file include/nanobind/stl/detail/traits.h extends this type trait
template <typename T, typename SFINAE = int>
struct is_copy_constructible : std::is_copy_constructible<T> { };

template <typename T>
constexpr bool is_copy_constructible_v = is_copy_constructible<T>::value;

NAMESPACE_END(detail)

// Low level access to nanobind type objects
inline bool type_check(handle h) { return detail::nb_type_check(h.ptr()); }
inline size_t type_size(handle h) { return detail::nb_type_size(h.ptr()); }
inline size_t type_align(handle h) { return detail::nb_type_align(h.ptr()); }
inline const std::type_info& type_info(handle h) { return *detail::nb_type_info(h.ptr()); }
template <typename T>
inline T &type_supplement(handle h) { return *(T *) detail::nb_type_supplement(h.ptr()); }
inline str type_name(handle h) { return steal<str>(detail::nb_type_name(h.ptr())); }

// Low level access to nanobind instance objects
inline bool inst_check(handle h) { return type_check(h.type()); }
inline str inst_name(handle h) {
    return steal<str>(detail::nb_inst_name(h.ptr()));
}
inline object inst_alloc(handle h) {
    return steal(detail::nb_inst_alloc((PyTypeObject *) h.ptr()));
}
inline object inst_alloc_zero(handle h) {
    return steal(detail::nb_inst_alloc_zero((PyTypeObject *) h.ptr()));
}
inline object inst_take_ownership(handle h, void *p) {
    return steal(detail::nb_inst_take_ownership((PyTypeObject *) h.ptr(), p));
}
inline object inst_reference(handle h, void *p, handle parent = handle()) {
    return steal(detail::nb_inst_reference((PyTypeObject *) h.ptr(), p, parent.ptr()));
}
inline void inst_zero(handle h) { detail::nb_inst_zero(h.ptr()); }
inline void inst_set_state(handle h, bool ready, bool destruct) {
    detail::nb_inst_set_state(h.ptr(), ready, destruct);
}
inline std::pair<bool, bool> inst_state(handle h) {
    return detail::nb_inst_state(h.ptr());
}
inline void inst_mark_ready(handle h) { inst_set_state(h, true, true); }
inline bool inst_ready(handle h) { return inst_state(h).first; }
inline void inst_destruct(handle h) { detail::nb_inst_destruct(h.ptr()); }
inline void inst_copy(handle dst, handle src) { detail::nb_inst_copy(dst.ptr(), src.ptr()); }
inline void inst_move(handle dst, handle src) { detail::nb_inst_move(dst.ptr(), src.ptr()); }
inline void inst_replace_copy(handle dst, handle src) { detail::nb_inst_replace_copy(dst.ptr(), src.ptr()); }
inline void inst_replace_move(handle dst, handle src) { detail::nb_inst_replace_move(dst.ptr(), src.ptr()); }
template <typename T> T *inst_ptr(handle h) { return (T *) detail::nb_inst_ptr(h.ptr()); }
inline void *type_get_slot(handle h, int slot_id) {
#if NB_TYPE_GET_SLOT_IMPL
    return detail::type_get_slot((PyTypeObject *) h.ptr(), slot_id);
#else
    return PyType_GetSlot((PyTypeObject *) h.ptr(), slot_id);
#endif
}

template <typename Visitor> struct def_visitor {
  protected:
    // Ensure def_visitor<T> can only be derived from, not constructed
    // directly
    def_visitor() {
        static_assert(std::is_base_of_v<def_visitor, Visitor>,
                      "def_visitor uses CRTP: def_visitor<T> should be "
                      "a base o
