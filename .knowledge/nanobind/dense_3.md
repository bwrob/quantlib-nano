(), ndim_v<T>, shape, handle(), strides),
            (policy == rv_policy::automatic ||
             policy == rv_policy::automatic_reference)
                ? rv_policy::reference
                : policy,
            cleanup);
    }

    StrideType strides() const {
        constexpr int IS = StrideType::InnerStrideAtCompileTime,
                      OS = StrideType::OuterStrideAtCompileTime;

        int64_t inner = caster.value.stride(0),
                outer;

        if constexpr (ndim_v<T> == 1)
            outer = caster.value.shape(0);
        else
            outer = caster.value.stride(1);

        (void) inner; (void) outer;
        if constexpr (ndim_v<T> == 2 && T::IsRowMajor)
            std::swap(inner, outer);

        // Eigen may expect a stride of 0 to avoid an assertion failure
        if constexpr (IS == 0)
            inner = 0;

        // Starting from numpy 2.4, dl_tensors' stride field is *always* set (for ndim > 0).
        // This also includes when shape=(0,0), when numpy reports the stride to be zero.
        // This creates an incompatibility with Eigen compile-time vectors, which expect
        // runtime and compile-time strides to be identical (e.g. for Eigen::VectorXi, equal to 1).
        if (ndim_v<T> == 1 && caster.value.shape(0) == 0)
            inner = IS;

        if constexpr (OS == 0)
            outer = 0;

        if constexpr (std::is_same_v<StrideType, Eigen::InnerStride<IS>>)
            return StrideType(inner);
        else if constexpr (std::is_same_v<StrideType, Eigen::OuterStride<OS>>)
            return StrideType(outer);
        else
            return StrideType(outer, inner);
    }

    operator Map() {
        NDArray &t = caster.value;
        if constexpr (ndim_v<T> == 1)
            return Map(t.data(), t.shape(0), strides());
        else
            return Map(t.data(), t.shape(0), t.shape(1), strides());
    }
};

/** \brief Caster for Eigen::Ref<T>

  Compared to the ``Eigen::Map<T>`` type caster above, the reference caster
  accepts a wider set of inputs when it is used in *constant reference* mode
  (i.e., ``Eigen::Ref<const T>``). In this case, it performs stride conversions
  (except for unusual non-contiguous strides) as well as conversions of the
  underlying scalar type (if implicit conversions are enabled).

  For non-constant references, the caster matches that of ``Eigen::Map<T>`` and
  requires an input with the expected layout (so that changes can propagate to
  the caller).
*/
template <typename T, int Options, typename StrideType>
struct type_caster<Eigen::Ref<T, Options, StrideType>,
                   enable_if_t<is_eigen_plain_v<T> &&
                               is_ndarray_scalar_v<typename T::Scalar>>> {
    using Ref = Eigen::Ref<T, Options, StrideType>;

    /// Potentially convert strides/dtype when casting constant references
    static constexpr bool MaybeConvert =
        std::is_const_v<T> &&
        // Restrict to contiguous 'T' (limitation in Eigen, see PR #215)
        can_map_contiguous_memory_v<Ref>;

    using NDArray =
        array_for_eigen_t<Ref, std::conditional_t<std::is_const_v<T>,
                                                  const typename Ref::Scalar,
                                                  typename Ref::Scalar>>;
    using NDArrayCaster = type_caster<NDArray>;

    /// Eigen::Map<T> caster with fixed strides
    using Map = Eigen::Map<T, Options, StrideType>;
    using MapCaster = make_caster<Map>;

    // Extended version taking arbitrary strides
    using DMap = Eigen::Map<const T, Options, DStride>;
    using DMapCaster = make_caster<DMap>;

    /**
     * The constructor of ``Ref<const T>`` uses one of two strategies
     * depending on the input. It may either
     *
     * 1. Create a copy ``Ref<const T>::m_object`` (owned by Ref), or
     * 2. Reference the existing input (non-owned).
     *
     * When the value below is ``true``, then it is guaranteed that
     * ``Ref(<DMap instance>)`` ow
