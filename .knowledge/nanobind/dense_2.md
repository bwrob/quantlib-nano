   static constexpr auto Name = Caster::Name;
    template <typename T_> using Cast = T;
    template <typename T_> static constexpr bool can_cast() { return true; }

    /// Generating an expression template from a Python object is, of course, not possible
    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept = delete;

    template <typename T2>
    static handle from_cpp(T2 &&v, rv_policy policy, cleanup_list *cleanup) noexcept {
        return Caster::from_cpp(std::forward<T2>(v), policy, cleanup);
    }
};

/** \brief Type caster for ``Eigen::Map<T>``

  The ``Eigen::Map<..>`` type exists to efficiently access memory provided by a
  caller. Given that, the nanobind type caster refuses to turn incompatible
  inputs into a ``Eigen::Map<T>`` when this would require an implicit
  conversion.
*/

template <typename T, int Options, typename StrideType>
struct type_caster<Eigen::Map<T, Options, StrideType>,
                   enable_if_t<is_eigen_plain_v<T> &&
                               is_ndarray_scalar_v<typename T::Scalar>>> {
    using Map = Eigen::Map<T, Options, StrideType>;
    using NDArray =
        array_for_eigen_t<Map, std::conditional_t<std::is_const_v<T>,
                                                  const typename Map::Scalar,
                                                  typename Map::Scalar>>;
    using NDArrayCaster = type_caster<NDArray>;
    static constexpr auto Name = NDArrayCaster::Name;
    template <typename T_> using Cast = Map;
    template <typename T_> static constexpr bool can_cast() { return true; }

    NDArrayCaster caster;

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {
        // Disable implicit conversions
        return from_python_(src, flags & ~(uint8_t)cast_flags::convert, cleanup);
    }

    bool from_python_(handle src, uint8_t flags, cleanup_list* cleanup) noexcept {
        if (!caster.from_python(src, flags & ~(uint8_t)cast_flags::accepts_none, cleanup))
            return false;

        // Check for memory layout compatibility of non-contiguous 'Map' types
        if constexpr (!is_contiguous_v<Map>)  {
            // Dynamic inner strides support any input, check the fixed case
            if constexpr (StrideType::InnerStrideAtCompileTime != Eigen::Dynamic) {
                // A compile-time stride of 0 implies "contiguous" ..
                int64_t is_expected = StrideType::InnerStrideAtCompileTime == 0
                                      ? 1 /*  .. and equals 1 for the inner stride */
                                      : StrideType::InnerStrideAtCompileTime,
                        is_actual = caster.value.stride(
                            (ndim_v<T> != 1 && T::IsRowMajor) ? 1 : 0);

                if (is_expected != is_actual)
                    return false;
            }

            // Analogous check for the outer strides
            if constexpr (ndim_v<T> == 2 && StrideType::OuterStrideAtCompileTime != Eigen::Dynamic) {
                int64_t os_expected = StrideType::OuterStrideAtCompileTime == 0
                                        ? caster.value.shape(T::IsRowMajor ? 1 : 0)
                                        : StrideType::OuterStrideAtCompileTime,
                        os_actual   = caster.value.stride(T::IsRowMajor ? 0 : 1);

                if (os_expected != os_actual)
                    return false;
            }
        }
        return true;
    }

    static handle from_cpp(const Map &v, rv_policy policy, cleanup_list *cleanup) noexcept {
        size_t shape[ndim_v<T>];
        int64_t strides[ndim_v<T>];

        if constexpr (ndim_v<T> == 1) {
            shape[0] = v.size();
            strides[0] = v.innerStride();
        } else {
            shape[0] = v.rows();
            shape[1] = v.cols();
            strides[0] = v.rowStride();
            strides[1] = v.colStride();
        }

        return NDArrayCaster::from_cpp(
            NDArray((void *) v.data
