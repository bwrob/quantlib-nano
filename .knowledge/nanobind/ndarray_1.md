expr bool is_signed  = std::is_signed_v<T>;
};

NAMESPACE_BEGIN(detail)

template <typename T, typename /* SFINAE */ = int> struct dtype_traits {
    using traits = ndarray_traits<T>;

    static constexpr int matches = traits::is_bool + traits::is_complex +
                                   traits::is_float + traits::is_int;
    static_assert(matches <= 1, "dtype matches multiple type categories!");

    static constexpr dlpack::dtype value{
        (uint8_t) ((traits::is_bool ? (int) dlpack::dtype_code::Bool : 0) +
                   (traits::is_complex ? (int) dlpack::dtype_code::Complex : 0) +
                   (traits::is_float ? (int) dlpack::dtype_code::Float : 0) +
                   (traits::is_int &&  traits::is_signed ? (int) dlpack::dtype_code::Int : 0) +
                   (traits::is_int && !traits::is_signed ? (int) dlpack::dtype_code::UInt : 0)),
        (uint8_t) matches ? sizeof(T) * 8 : 0,
        matches ? 1 : 0
    };

    static constexpr auto name =
        const_name<traits::is_complex>("complex", "") +
        const_name<traits::is_int &&  traits::is_signed>("int", "") +
        const_name<traits::is_int && !traits::is_signed>("uint", "") +
        const_name<traits::is_float>("float", "") +
        const_name<traits::is_bool>(const_name("bool"), const_name<sizeof(T) * 8>());
};

template <> struct dtype_traits<void> {
    static constexpr dlpack::dtype value{ 0, 0, 0 };
    static constexpr auto name = descr<0>();
};

template <typename T> struct dtype_traits<const T> {
    static constexpr dlpack::dtype value = dtype_traits<T>::value;
    static constexpr auto name = dtype_traits<T>::name;
};

template <ssize_t... Is> struct shape {
    static constexpr auto name =
        const_name("shape=(") +
        concat(const_name<Is == -1>(const_name("*"),
                                    const_name<(size_t) Is>())...) + const_name(")");
    static_assert(
        ((Is >= 0 || Is == -1) && ...),
        "The arguments to nanobind::shape must either be positive or equal to -1"
    );

    static void put(int64_t *out) {
        size_t ctr = 0;
        ((out[ctr++] = Is), ...);
    }

    static void put(size_t *out) {
        if constexpr (((Is == -1) || ...))
            detail::fail("Negative ndarray sizes are not allowed here!");
        size_t ctr = 0;
        ((out[ctr++] = (size_t) Is), ...);
    }
};

template <typename T>
constexpr bool is_ndarray_scalar_v = dtype_traits<T>::value.bits != 0;

template <typename> struct ndim_shape;
template <size_t... S> struct ndim_shape<std::index_sequence<S...>> {
    using type = shape<((void) S, -1)...>;
};

NAMESPACE_END(detail)

using detail::shape;

struct ro { };

template <size_t N>
using ndim = typename detail::ndim_shape<std::make_index_sequence<N>>::type;

template <typename T> constexpr dlpack::dtype dtype() {
    return detail::dtype_traits<T>::value;
}

NAMESPACE_BEGIN(detail)

/// Sentinel type to initialize ndarray_config_t<>
struct unused {
    using type = void;
    static constexpr int value = 0;
    static constexpr auto name = descr<0>();
};

/// ndarray_config describes a requested array configuration
struct ndarray_config {
    int device_type = 0;
    char order = '\0';
    bool ro = false;
    dlpack::dtype dtype { };
    int32_t ndim = -1;
    int64_t *shape = nullptr;

    ndarray_config() = default;
    template <typename T> ndarray_config(T)
        : device_type(T::DeviceType::value),
          order((char) T::Order::value),
          ro(std::is_const_v<typename T::Scalar>),
          dtype(nanobind::dtype<typename T::Scalar>()),
          ndim(T::N),
          shape(nullptr) { }
};

/// ndarray_config_t collects nd-array template parameters in a structured way.
/// Its "storage" is purely based on types members
template <typename /* SFINAE */ = int, typename...> struct ndarray_config_t;

template <> struct ndarray_config_t<int> {
    using Framework = no_framework;
    using Scalar = void;
    using Shape = unused;
    using Order 