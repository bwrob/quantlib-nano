(Scalar *) ((uint8_t *) m_dltensor.data +
                           m_dltensor.byte_offset);
    }

    template <typename... Args2>
    NB_INLINE auto& operator()(Args2... indices) const {
        return *(Scalar *) ((uint8_t *) m_dltensor.data +
                            byte_offset(indices...));
    }

    template <typename... Args2> NB_INLINE auto view() const {
        using namespace detail;
        using Config2 = detail::ndarray_config_t<int, Args2..., Args...>;
        using Scalar2 = typename Config2::Scalar;
        constexpr size_t N = Config2::N >= 0 ? Config2::N : 0;

        constexpr bool has_scalar = !std::is_void_v<Scalar2>,
                       has_shape  = Config2::N >= 0;

        static_assert(has_scalar,
            "To use the ndarray::view<..>() method, you must add a scalar type "
            "annotation (e.g. 'float') to the template parameters of the parent "
            "ndarray, or to the call to .view<..>()");

        static_assert(has_shape,
            "To use the ndarray::view<..>() method, you must add a shape<..> "
            "or ndim<..> annotation to the template parameters of the parent "
            "ndarray, or to the call to .view<..>()");

        if constexpr (has_scalar && has_shape) {
            using Result = ndarray_view<Scalar2, N, Config2::Order::value>;
            return Result((Scalar2 *) data(), shape_ptr(), stride_ptr(),
                          std::make_index_sequence<N>(),
                          typename Config2::Shape());
        } else {
            return nullptr;
        }
    }

    auto cast(rv_policy rvp = rv_policy::automatic, class handle parent = {});

private:
    template <typename... Args2>
    NB_INLINE int64_t byte_offset(Args2... indices) const {
        constexpr bool has_scalar = !std::is_void_v<Scalar>,
                       has_shape  = Config::N != -1;

        static_assert(has_scalar,
            "To use ndarray::operator(), you must add a scalar type "
            "annotation (e.g. 'float') to the ndarray template parameters.");

        static_assert(has_shape,
            "To use ndarray::operator(), you must add a shape<> or "
            "ndim<> annotation to the ndarray template parameters.");

        if constexpr (has_scalar && has_shape) {
            static_assert(sizeof...(Args2) == (size_t) Config::N,
                          "ndarray::operator(): invalid number of arguments");

            size_t counter = 0;
            int64_t index = 0;
            ((index += int64_t(indices) * m_dltensor.strides[counter++]), ...);

            return (int64_t) m_dltensor.byte_offset + index * sizeof(Scalar);
        } else {
            return 0;
        }
    }

    detail::ndarray_handle *m_handle = nullptr;
    dlpack::dltensor m_dltensor;
};

inline bool ndarray_check(handle h) { return detail::ndarray_check(h.ptr()); }

NAMESPACE_BEGIN(detail)

template <typename T> struct dtype_name {
    static constexpr auto name = detail::const_name("dtype=") + dtype_traits<T>::name;
};

template <> struct dtype_name<void> : unused { };
template <> struct dtype_name<const void> : unused { };

template <typename T> struct dtype_const_name {
    static constexpr auto name = const_name<std::is_const_v<T>>("writable=False", "");
};

template <typename... Args> struct type_caster<ndarray<Args...>> {
    using Config = detail::ndarray_config_t<int, Args...>;
    using Scalar = typename Config::Scalar;

    NB_TYPE_CASTER(ndarray<Args...>,
                   Config::Framework::name +
                   const_name("[") +
                       concat_maybe(dtype_name<Scalar>::name,
                                    Config::Shape::name,
                                    Config::Order::name,
                                    Config::DeviceType::name,
                                    dtype_const_name<Scalar>::name) +
                   const_name("]"))

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {

