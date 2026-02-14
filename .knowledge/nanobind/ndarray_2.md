= unused;
    using DeviceType = unused;
    static constexpr int32_t N = -1;
};

// Template infrastructure to collect ndarray annotations and fail if duplicates are found
template <typename... Args> struct ndarray_config_t<int, ro, Args...> : ndarray_config_t<int, Args...> {
    using Scalar = std::add_const_t<typename ndarray_config_t<int, Args...>::Scalar>;
};

template <typename... Args> struct ndarray_config_t<int, unused, Args...> : ndarray_config_t<int, Args...> { };

template <typename Arg, typename... Args> struct ndarray_config_t<enable_if_t<is_ndarray_scalar_v<Arg>>, Arg, Args...> : ndarray_config_t<int, Args...> {
    using Scalar = std::conditional_t<
        std::is_const_v<typename ndarray_config_t<int, Args...>::Scalar>,
        std::add_const_t<Arg>, Arg>;
};

template <typename Arg, typename... Args> struct ndarray_config_t<enable_if_t<Arg::is_device_type>, Arg, Args...> : ndarray_config_t<int, Args...> {
    using DeviceType = Arg;
};

template <typename Arg, typename... Args> struct ndarray_config_t<enable_if_t<Arg::is_framework>, Arg, Args...> : ndarray_config_t<int, Args...> {
    using Framework = Arg;
};

template <typename Arg, typename... Args> struct ndarray_config_t<enable_if_t<Arg::is_order>, Arg, Args...> : ndarray_config_t<int, Args...> {
    using Order = Arg;
};

template <ssize_t... Is, typename... Args> struct ndarray_config_t<int, shape<Is...>, Args...> : ndarray_config_t<int, Args...> {
    using Shape = shape<Is...>;
    static constexpr int32_t N = sizeof...(Is);
};

NAMESPACE_END(detail)

template <typename Scalar, size_t Dim, char Order> struct ndarray_view {
    ndarray_view() = default;
    ndarray_view(const ndarray_view &) = default;
    ndarray_view(ndarray_view &&) = default;
    ndarray_view &operator=(const ndarray_view &) = default;
    ndarray_view &operator=(ndarray_view &&) noexcept = default;
    ~ndarray_view() noexcept = default;

    template <typename... Args> NB_INLINE Scalar &operator()(Args... indices) const {
        static_assert(
            sizeof...(Args) == Dim,
            "ndarray_view::operator(): invalid number of arguments");

        const int64_t indices_i64[] { (int64_t) indices... };
        int64_t offset = 0;
        for (size_t i = 0; i < Dim; ++i)
            offset += indices_i64[i] * m_strides[i];

        return *(m_data + offset);
    }

    size_t ndim() const { return Dim; }
    size_t shape(size_t i) const { return m_shape[i]; }
    int64_t stride(size_t i) const { return m_strides[i]; }
    Scalar *data() const { return m_data; }

private:
    template <typename...> friend class ndarray;

    template <size_t... I1, ssize_t... I2>
    ndarray_view(Scalar *data, const int64_t *shape, const int64_t *strides,
                 std::index_sequence<I1...>, nanobind::shape<I2...>)
        : m_data(data) {

        /* Initialize shape/strides with compile-time knowledge if
           available (to permit vectorization, loop unrolling, etc.) */
        ((m_shape[I1] = (I2 == -1) ? shape[I1] : (int64_t) I2), ...);
        ((m_strides[I1] = strides[I1]), ...);

        if constexpr (Order == 'F') {
            m_strides[0] = 1;
            for (size_t i = 1; i < Dim; ++i)
                m_strides[i] = m_strides[i - 1] * m_shape[i - 1];
        } else if constexpr (Order == 'C') {
            m_strides[Dim - 1] = 1;
            for (Py_ssize_t i = (Py_ssize_t) Dim - 2; i >= 0; --i)
                m_strides[i] = m_strides[i + 1] * m_shape[i + 1];
        }
    }

    Scalar *m_data = nullptr;
    int64_t m_shape[Dim] { };
    int64_t m_strides[Dim] { };
};


template <typename... Args> class ndarray {
public:
    template <typename...> friend class ndarray;

    using Config = detail::ndarray_config_t<int, Args...>;
    using Scalar = typename Config::Scalar;
    static constexpr bool ReadOnly = std::is_const_v<Scalar>;
    static constexpr char Order = Config::Order::value;
    static constexpr int DeviceType = Config::DeviceType::value;
    using V