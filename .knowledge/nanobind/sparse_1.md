anup_list *) noexcept {
        if (!v.isCompressed()) {
            PyErr_SetString(PyExc_ValueError,
                            "nanobind: unable to return an Eigen sparse matrix that is not in a compressed format. "
                            "Please call `.makeCompressed()` before returning the value on the C++ end.");
            return handle();
        }

        object matrix_type;
        try {
            matrix_type = module_::import_("scipy.sparse").attr(RowMajor ? "csr_matrix" : "csc_matrix");
        } catch (python_error &e) {
            e.restore();
            return handle();
        }

        const Index rows = v.rows(), cols = v.cols();
        const size_t data_shape[] = { (size_t) v.nonZeros() };
        const size_t outer_indices_shape[] = { (size_t) ((RowMajor ? rows : cols) + 1) };

        T *src = std::addressof(const_cast<T &>(v));
        object owner;
        if (policy == rv_policy::move) {
            src = new T(std::move(v));
            owner = capsule(src, [](void *p) noexcept { delete (T *) p; });
        }

        ScalarNDArray data(src->valuePtr(), 1, data_shape, owner);
        StorageIndexNDArray outer_indices(src->outerIndexPtr(), 1, outer_indices_shape, owner);
        StorageIndexNDArray inner_indices(src->innerIndexPtr(), 1, data_shape, owner);

        try {
            return matrix_type(nanobind::make_tuple(
                                   std::move(data), std::move(inner_indices), std::move(outer_indices)),
                               nanobind::make_tuple(rows, cols))
                .release();
        } catch (python_error &e) {
            e.restore();
            return handle();
        }
    }
};


/// Caster for Eigen::Map<Eigen::SparseMatrix>, still needs to be implemented.
template <typename T>
struct type_caster<Eigen::Map<T>, enable_if_t<is_eigen_sparse_matrix_v<T>>> {
    using Scalar = typename T::Scalar;
    using StorageIndex = typename T::StorageIndex;
    using Index = typename T::Index;
    using SparseMap = Eigen::Map<T>;
    using Map = Eigen::Map<T>;
    using SparseMatrixCaster = type_caster<T>;
    static constexpr bool RowMajor = T::IsRowMajor;

    using ScalarNDArray = ndarray<numpy, Scalar, shape<-1>>;
    using StorageIndexNDArray = ndarray<numpy, StorageIndex, shape<-1>>;

    using ScalarCaster = make_caster<ScalarNDArray>;
    using StorageIndexCaster = make_caster<StorageIndexNDArray>;

    static constexpr auto Name = const_name<RowMajor>("scipy.sparse.csr_matrix[",
                                           "scipy.sparse.csc_matrix[")
                   + make_caster<Scalar>::Name + const_name("]");

    template <typename T_> using Cast = Map;
    template <typename T_> static constexpr bool can_cast() { return true; }

    ScalarCaster data_caster;
    StorageIndexCaster indices_caster, indptr_caster;
    Index rows, cols, nnz;

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {
        flags = ~(uint8_t) cast_flags::convert;

        try {
            object matrix_type =
                module_::import_("scipy.sparse")
                    .attr(RowMajor ? "csr_matrix" : "csc_matrix");
            if (!src.type().is(matrix_type))
                return false;

            if (!cast<bool>(src.attr("has_sorted_indices")))
                src.attr("sort_indices")();

            if (object data_o = src.attr("data");
                !data_caster.from_python(data_o, flags, cleanup))
                return false;

            if (object indices_o = src.attr("indices");
                !indices_caster.from_python(indices_o, flags, cleanup))
                return false;

            if (object indptr_o = src.attr("indptr");
                !indptr_caster.from_python(indptr_o, flags, cleanup))
                return false;

            object shape_o = src.attr("shape");
            if (len(shape_o) != 2)
                return false;

            rows = cast<Index>(shape_o[0]);
            cols = cast<Index>
