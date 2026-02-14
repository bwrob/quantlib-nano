/*
    nanobind/eigen/sparse.h: type casters for sparse Eigen matrices

    Copyright (c) 2023 Henri Menke and Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

#pragma once

#include <nanobind/ndarray.h>
#include <nanobind/eigen/dense.h>
#include <Eigen/SparseCore>

#include <memory>
#include <type_traits>
#include <utility>

NAMESPACE_BEGIN(NB_NAMESPACE)

NAMESPACE_BEGIN(detail)

/// Detect Eigen::SparseMatrix
template <typename T> constexpr bool is_eigen_sparse_matrix_v =
    is_eigen_sparse_v<T> &&
    !std::is_base_of_v<Eigen::SparseMapBase<T, Eigen::ReadOnlyAccessors>, T>;


/// Caster for Eigen::SparseMatrix
template <typename T> struct type_caster<T, enable_if_t<is_eigen_sparse_matrix_v<T>>> {
    using Scalar = typename T::Scalar;
    using StorageIndex = typename T::StorageIndex;
    using Index = typename T::Index;
    using SparseMap = Eigen::Map<T>;

    static_assert(std::is_same_v<T, Eigen::SparseMatrix<Scalar, T::Options, StorageIndex>>,
                  "nanobind: Eigen sparse caster only implemented for matrices");

    static constexpr bool RowMajor = T::IsRowMajor;

    using ScalarNDArray = ndarray<numpy, Scalar, shape<-1>>;
    using StorageIndexNDArray = ndarray<numpy, StorageIndex, shape<-1>>;

    using ScalarCaster = make_caster<ScalarNDArray>;
    using StorageIndexCaster = make_caster<StorageIndexNDArray>;

    NB_TYPE_CASTER(T, const_name<RowMajor>("scipy.sparse.csr_matrix[",
                                           "scipy.sparse.csc_matrix[")
                   + make_caster<Scalar>::Name + const_name("]"))

    ScalarCaster data_caster;
    StorageIndexCaster indices_caster, indptr_caster;

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {
        object obj = borrow(src);

        try {
            object matrix_type =
                module_::import_("scipy.sparse")
                    .attr(RowMajor ? "csr_matrix" : "csc_matrix");
            if (!obj.type().is(matrix_type))
                obj = matrix_type(obj);

            if (!cast<bool>(obj.attr("has_sorted_indices")))
                obj.attr("sort_indices")();

            if (object data_o = obj.attr("data");
                !data_caster.from_python(data_o, flags, cleanup))
                return false;

            if (object indices_o = obj.attr("indices");
                !indices_caster.from_python(indices_o, flags, cleanup))
                return false;

            if (object indptr_o = obj.attr("indptr");
                !indptr_caster.from_python(indptr_o, flags, cleanup))
                return false;

            object shape_o = obj.attr("shape");
            if (len(shape_o) != 2)
                return false;

            Index rows = cast<Index>(shape_o[0]),
                  cols = cast<Index>(shape_o[1]),
                  nnz = cast<Index>(obj.attr("nnz"));

            value = SparseMap(rows, cols, nnz,
                              indptr_caster.value.data(),
                              indices_caster.value.data(),
                              data_caster.value.data());
            return true;
        } catch (const python_error &) {
            return false;
        }
    }

    static handle from_cpp(T &&v, rv_policy policy, cleanup_list *cleanup) noexcept {
        if (policy == rv_policy::automatic ||
            policy == rv_policy::automatic_reference)
            policy = rv_policy::move;

        return from_cpp((const T &) v, policy, cleanup);
    }

    template <typename T2>
    static handle from_cpp(T2 &&v, rv_policy policy, cleanup_list *cleanup) noexcept {
        policy = infer_policy<T2>(policy);
        if constexpr (std::is_pointer_v<T2>)
            return from_cpp_internal((const T &) *v, policy, cleanup);
        else
            return from_cpp_internal((const T &) v, policy, cleanup);
    }

    static handle from_cpp_internal(const T &v, rv_policy policy, cle