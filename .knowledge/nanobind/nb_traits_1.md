t analyze_method<Ret (Cls::*)(Args...) const noexcept> {
    using func = Ret(Args...);
    static constexpr size_t argc = sizeof...(Args);
};

template <typename F>
struct strip_function_object {
    using type = typename analyze_method<decltype(&F::operator())>::func;
};

// Extracts the function signature from a function, function pointer or lambda.
template <typename Function, typename F = std::remove_reference_t<Function>>
using function_signature_t = std::conditional_t<
    std::is_function_v<F>, F,
    typename std::conditional_t<
        std::is_pointer_v<F> || std::is_member_pointer_v<F>,
        std::remove_pointer<F>,
        strip_function_object<F>>::type>;

template <typename T>
using forward_t = std::conditional_t<std::is_lvalue_reference_v<T>, T, T &&>;

template <typename...> inline constexpr bool false_v = false;

template <typename... Args> struct overload_cast_impl {
    template <typename Return>
    constexpr auto operator()(Return (*pf)(Args...)) const noexcept
                              -> decltype(pf) { return pf; }

    template <typename Return, typename Class>
    constexpr auto operator()(Return (Class::*pmf)(Args...), std::false_type = {}) const noexcept
                              -> decltype(pmf) { return pmf; }

    template <typename Return, typename Class>
    constexpr auto operator()(Return (Class::*pmf)(Args...) const, std::true_type) const noexcept
                              -> decltype(pmf) { return pmf; }
};

/// Detector pattern
template <typename SFINAE, template <typename> typename Op, typename Arg>
struct detector : std::false_type { };

template <template <typename> typename Op, typename Arg>
struct detector<std::void_t<Op<Arg>>, Op, Arg>
    : std::true_type { };

/* This template is used for docstring generation and specialized in
   ``stl/{variant,optional.h}`` to strip away std::optional and
   ``std::variant<std::monostate>`` in top-level argument types and
   avoid redundancy when combined with nb::arg(...).none(). */
template <typename T> struct remove_opt_mono { using type = T; };

// Detect std::enable_shared_from_this without including <memory>
template <typename T>
auto has_shared_from_this_impl(T *ptr) ->
    decltype(ptr->weak_from_this().lock().get(), std::true_type{});
std::false_type has_shared_from_this_impl(...);

template <typename T>
constexpr bool has_shared_from_this_v =
    decltype(has_shared_from_this_impl((T *) nullptr))::value;

/// Base of all type casters for traditional bindings created via nanobind::class_<>
struct type_caster_base_tag {
    static constexpr bool IsClass = true;
};

/// Check if a type caster represents traditional bindings created via nanobind::class_<>
template <typename Caster>
constexpr bool is_base_caster_v = std::is_base_of_v<type_caster_base_tag, Caster>;

template <typename T> using is_class_caster_test = std::enable_if_t<T::IsClass>;

/// Generalized version of the is_base_caster_v test that also accepts unique_ptr/shared_ptr
template <typename Caster>
constexpr bool is_class_caster_v = detail::detector<void, is_class_caster_test, Caster>::value;

// Primary template
template<typename T, typename = int>
struct is_complex : std::false_type {};

// Specialization if `T` is complex, i.e., `T` has a member type `value_type`,
// member functions `real()` and `imag()` that return such, and the size of
// `T` is twice that of `value_type`.
template<typename T>
struct is_complex<T, enable_if_t<std::is_same_v<
                                     decltype(std::declval<T>().real()),
                                     typename T::value_type>
                              && std::is_same_v<
                                     decltype(std::declval<T>().imag()),
                                     typename T::value_type>
                              && (sizeof(T) ==
                                  2 * sizeof(typename T::value_type))>>
    : std::true_type {};

/// True if the type `T` is a complete type representing a compl