        ndim_v<T> == 1 || T::IsRowMajor,
            c_contig,
            f_contig>,
        unused>>;

/// Any kind of Eigen class
template <typename T> constexpr bool is_eigen_v = is_base_of_template_v<T, Eigen::EigenBase>;

/// Detects Eigen::Array, Eigen::Matrix, etc.
template <typename T> constexpr bool is_eigen_plain_v = is_base_of_template_v<T, Eigen::PlainObjectBase>;

/// Detect Eigen::SparseMatrix
template <typename T> constexpr bool is_eigen_sparse_v = is_base_of_template_v<T, Eigen::SparseMatrixBase>;

/// Detects expression templates
template <typename T> constexpr bool is_eigen_xpr_v =
    is_eigen_v<T> && !is_eigen_plain_v<T> && !is_eigen_sparse_v<T> &&
    !std::is_base_of_v<Eigen::MapBase<T, Eigen::ReadOnlyAccessors>, T>;

template <typename T>
struct type_caster<T, enable_if_t<is_eigen_plain_v<T> &&
                                  is_ndarray_scalar_v<typename T::Scalar>>> {
    using Scalar = typename T::Scalar;
    using NDArray = array_for_eigen_t<T>;
    using NDArrayCaster = make_caster<NDArray>;

    NB_TYPE_CASTER(T, NDArrayCaster::Name)

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {
        // We're in any case making a copy, so non-writable inputs area also okay
        using NDArrayConst = array_for_eigen_t<T, const typename T::Scalar>;
        make_caster<NDArrayConst> caster;
        if (!caster.from_python(src, flags & ~(uint8_t)cast_flags::accepts_none, cleanup))
            return false;

        const NDArrayConst &array = caster.value;
        if constexpr (ndim_v<T> == 1)
            value.resize(array.shape(0));
        else
            value.resize(array.shape(0), array.shape(1));

        // The layout is contiguous & compatible thanks to array_for_eigen_t<T>
        memcpy(value.data(), array.data(), array.size() * sizeof(Scalar));

        return true;
    }

    template <typename T2>
    static handle from_cpp(T2 &&v, rv_policy policy, cleanup_list *cleanup) noexcept {
        policy = infer_policy<T2>(policy);
        if constexpr (std::is_pointer_v<T2>)
            return from_cpp_internal((const T &) *v, policy, cleanup);
        else
            return from_cpp_internal((const T &) v, policy, cleanup);
    }

    static handle from_cpp_internal(const T &v, rv_policy policy, cleanup_list *cleanup) noexcept {
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

        void *ptr = (void *) v.data();

        if (policy == rv_policy::move) {
            // Don't bother moving when the data is static or occupies <1KB
            if ((T::SizeAtCompileTime != Eigen::Dynamic ||
                 (size_t) v.size() < (1024 / sizeof(Scalar))))
                policy = rv_policy::copy;
        }

        object owner;
        if (policy == rv_policy::move) {
            T *temp = new T((T&&) v);
            owner = capsule(temp, [](void *p) noexcept { delete (T *) p; });
            ptr = temp->data();
            policy = rv_policy::reference;
        } else if (policy == rv_policy::reference_internal && cleanup->self()) {
            owner = borrow(cleanup->self());
            policy = rv_policy::reference;
        }

        object o = steal(NDArrayCaster::from_cpp(
            NDArray(ptr, ndim_v<T>, shape, owner, strides),
            policy, cleanup));

        return o.release();
    }
};

/// Caster for Eigen expression templates
template <typename T>
struct type_caster<T, enable_if_t<is_eigen_xpr_v<T> &&
                                  is_ndarray_scalar_v<typename T::Scalar>>> {
    using Array = Eigen::Array<typename T::Scalar, T::RowsAtCompileTime,
                               T::ColsAtCompileTime>;
    using Caster = make_caster<Array>;
 