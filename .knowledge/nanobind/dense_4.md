ns the underlying data.
     */
    static constexpr bool DMapConstructorOwnsData =
        !Eigen::internal::traits<Ref>::template match<DMap>::type::value;

    static constexpr auto Name =
        const_name<MaybeConvert>(DMapCaster::Name, MapCaster::Name);

    template <typename T_> using Cast = Ref;
    template <typename T_> static constexpr bool can_cast() { return true; }

    MapCaster caster;
    struct Empty { };
    std::conditional_t<MaybeConvert, DMapCaster, Empty> dcaster;

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {
        // Try a direct cast without implicit conversion first
        if (caster.from_python(src, flags, cleanup))
            return true;

        // Potentially convert strides/dtype when casting constant references
        if constexpr (MaybeConvert) {
            /* Generating an implicit copy requires some object to assume
               ownership. During a function call, ``dcaster`` can serve that
               role (this case is detected by checking whether ``flags`` has
               the ``manual`` flag set). When used in other situations (e.g.
               ``nb::cast()``), the created ``Eigen::Ref<..>`` must take
               ownership of the copy. This is only guranteed to work if
               DMapConstructorOwnsData.

               If neither of these is possible, we disable implicit
               conversions. */

            if ((flags & (uint8_t) cast_flags::manual) &&
                !DMapConstructorOwnsData)
                flags &= ~(uint8_t) cast_flags::convert;

            if (dcaster.from_python_(src, flags, cleanup))
                return true;
        }

        return false;
    }

    static handle from_cpp(const Ref &v, rv_policy policy, cleanup_list *cleanup) noexcept {
        // Copied from the Eigen::Map caster

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
            NDArray((void *) v.data(), ndim_v<T>, shape, handle(), strides),
            (policy == rv_policy::automatic ||
             policy == rv_policy::automatic_reference)
                ? rv_policy::reference
                : policy,
            cleanup);
    }

    operator Ref() {
        if constexpr (MaybeConvert) {
            if (dcaster.caster.value.is_valid())
                return Ref(dcaster.operator DMap());
        }

        return Ref(caster.operator Map());
    }
};

NAMESPACE_END(detail)

NAMESPACE_END(NB_NAMESPACE)
