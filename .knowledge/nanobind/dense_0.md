/*
    nanobind/eigen/dense.h: type casters for dense Eigen
    vectors and matrices

    Copyright (c) 2023 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.
*/

#pragma once

#include <nanobind/ndarray.h>
#include <Eigen/Core>

static_assert(EIGEN_VERSION_AT_LEAST(3, 3, 1),
              "Eigen matrix support in nanobind requires Eigen >= 3.3.1");

NAMESPACE_BEGIN(NB_NAMESPACE)

/// Function argument types that are compatible with various array flavors
using DStride = Eigen::Stride<Eigen::Dynamic, Eigen::Dynamic>;
template <typename T> using DRef = Eigen::Ref<T, 0, DStride>;
template <typename T> using DMap = Eigen::Map<T, 0, DStride>;

NAMESPACE_BEGIN(detail)

/// Determine the number of dimensions of the given Eigen type
template <typename T>
constexpr int ndim_v = bool(T::IsVectorAtCompileTime) ? 1 : 2;

/// Extract the compile-time strides of the given Eigen type
template <typename T> struct stride {
    using type = Eigen::Stride<0, 0>;
};

template <typename T, int Options, typename StrideType> struct stride<Eigen::Map<T, Options, StrideType>> {
    using type = StrideType;
};

template <typename T, int Options, typename StrideType> struct stride<Eigen::Ref<T, Options, StrideType>> {
    using type = StrideType;
};

template <typename T> using stride_t = typename stride<T>::type;

/** \brief Identify types with a contiguous memory representation.
 *
 * This includes all specializations of ``Eigen::Matrix``/``Eigen::Array`` and
 * certain specializations of ``Eigen::Map`` and ``Eigen::Ref``. Note: Eigen
 * interprets a compile-time stride of 0 as contiguous.
 */
template <typename T>
constexpr bool is_contiguous_v =
    (stride_t<T>::InnerStrideAtCompileTime == 0 ||
     stride_t<T>::InnerStrideAtCompileTime == 1) &&
    (ndim_v<T> == 1 || stride_t<T>::OuterStrideAtCompileTime == 0 ||
     (stride_t<T>::OuterStrideAtCompileTime != Eigen::Dynamic &&
      int(stride_t<T>::OuterStrideAtCompileTime) == int(T::InnerSizeAtCompileTime)));

/// Identify types with a static or dynamic layout that support contiguous storage
template <typename T>
constexpr bool can_map_contiguous_memory_v =
    (stride_t<T>::InnerStrideAtCompileTime == 0 ||
     stride_t<T>::InnerStrideAtCompileTime == 1 ||
     stride_t<T>::InnerStrideAtCompileTime == Eigen::Dynamic) &&
    (ndim_v<T> == 1 || stride_t<T>::OuterStrideAtCompileTime == 0 ||
     stride_t<T>::OuterStrideAtCompileTime == Eigen::Dynamic ||
     int(stride_t<T>::OuterStrideAtCompileTime) == int(T::InnerSizeAtCompileTime));

/* This type alias builds the most suitable 'ndarray' for the given Eigen type.
   In particular, it

  - matches the underlying scalar type
  - matches the number of dimensions (i.e. whether the type is a vector/matrix)
  - matches the shape (if the row/column count is known at compile time)
  - matches the in-memory ordering when the Eigen type is contiguous.

  This is helpful because type_caster<ndarray<..>> will then perform the
  necessary conversion steps (if given incompatible input) to enable data
  exchange with Eigen.

  A limitation of this approach is that ndarray does not support compile-time
  strides besides c_contig and f_contig. If an Eigen type requires
  non-contiguous strides (at compile-time) and we are given an ndarray with
  unsuitable strides (at run-time), type casting will fail. Note, however, that
  this is rather unusual, since the default stride type of Eigen::Map requires
  contiguous memory, and the one of Eigen::Ref requires a contiguous inner
  stride, while handling any outer stride.
*/

template <typename T, typename Scalar = typename T::Scalar>
using array_for_eigen_t = ndarray<
    Scalar,
    numpy,
    std::conditional_t<
        ndim_v<T> == 1,
        shape<T::SizeAtCompileTime>,
        shape<T::RowsAtCompileTime,
              T::ColsAtCompileTime>>,
    std::conditional_t<
        is_contiguous_v<T>,
        std::conditional_t<
    