ex number.
template<typename T>
inline constexpr bool is_complex_v = is_complex<T>::value;

template <typename T>
struct has_arg_defaults : std::false_type {};

template <typename T>
constexpr bool has_arg_defaults_v = has_arg_defaults<intrinsic_t<T>>::value;

NAMESPACE_END(detail)

template <typename... Args>
static constexpr detail::overload_cast_impl<Args...> overload_cast = {};
static constexpr auto const_ = std::true_type{};

template <template<typename> class Op, typename Arg>
constexpr bool is_detected_v = detail::detector<void, Op, Arg>::value;

template <typename T>
using remove_opt_mono_t = typename detail::remove_opt_mono<T>::type;

template <template <typename> typename Base, typename T>
std::true_type is_base_of_template(const Base<T>*);

template <template <typename> typename Base>
std::false_type is_base_of_template(...);

template <typename T, template <typename> typename Base>
constexpr bool is_base_of_template_v =
    decltype(is_base_of_template<Base>(std::declval<T *>()))::value;

NAMESPACE_END(NB_NAMESPACE)