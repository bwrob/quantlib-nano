(shape_o[1]);
            nnz = cast<Index>(src.attr("nnz"));
        } catch (const python_error &) {
            return false;
        }

        return true;
    }

    static handle from_cpp(const Map &v, rv_policy, cleanup_list *) noexcept {
        if (!v.isCompressed()) {
            PyErr_SetString(
                PyExc_ValueError,
                "nanobind: unable to return an Eigen sparse matrix that is not "
                "in a compressed format. Please call `.makeCompressed()` "
                "before returning the value on the C++ end.");
            return handle();
        }

        object matrix_type;
        try {
            matrix_type = module_::import_("scipy.sparse")
                              .attr(RowMajor ? "csr_matrix" : "csc_matrix");

            const Index rows = v.rows(), cols = v.cols();
            const size_t data_shape[] = { (size_t) v.nonZeros() };
            const size_t outer_indices_shape[] = {
                (size_t) ((RowMajor ? rows : cols) + 1)
            };

            ScalarNDArray data((void *) v.valuePtr(), 1, data_shape);
            StorageIndexNDArray
                outer_indices((void *) v.outerIndexPtr(), 1, outer_indices_shape),
                inner_indices((void *) v.innerIndexPtr(), 1, data_shape);

            return matrix_type(nanobind::make_tuple(
                                   cast(data, rv_policy::reference),
                                   cast(inner_indices, rv_policy::reference),
                                   cast(outer_indices, rv_policy::reference)),
                               nanobind::make_tuple(rows, cols))
                .release();
        } catch (python_error &e) {
            e.restore();
            return handle();
        }
    };

    operator Map() {
        return SparseMap(rows, cols, nnz,
                         indptr_caster.value.data(),
                         indices_caster.value.data(),
                         data_caster.value.data());
    }
};


/// Caster for Eigen::Ref<Eigen::SparseMatrix>, still needs to be implemented
template <typename T, int Options>
struct type_caster<Eigen::Ref<T, Options>, enable_if_t<is_eigen_sparse_matrix_v<T>>> {
    using Ref = Eigen::Ref<T, Options>;
    using Map = Eigen::Map<T, Options>;
    using MapCaster = make_caster<Map>;
    static constexpr auto Name = MapCaster::Name;
    template <typename T_> using Cast = Ref;
    template <typename T_> static constexpr bool can_cast() { return true; }

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept = delete;

    static handle from_cpp(const Ref &v, rv_policy policy, cleanup_list *cleanup) noexcept = delete;
};

NAMESPACE_END(detail)

NAMESPACE_END(NB_NAMESPACE)