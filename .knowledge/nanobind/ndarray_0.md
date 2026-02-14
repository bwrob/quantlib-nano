/*
    nanobind/ndarray.h: functionality to exchange n-dimensional arrays with
    other array programming frameworks (NumPy, PyTorch, etc.)

    Copyright (c) 2022 Wenzel Jakob

    All rights reserved. Use of this source code is governed by a
    BSD-style license that can be found in the LICENSE file.

    The API below is based on the DLPack project
    (https://github.com/dmlc/dlpack/blob/main/include/dlpack/dlpack.h)
*/

#pragma once

#include <nanobind/nanobind.h>
#include <initializer_list>

NAMESPACE_BEGIN(NB_NAMESPACE)

/// DLPack API/ABI data structures are part of a separate namespace.
NAMESPACE_BEGIN(dlpack)

enum class dtype_code : uint8_t {
    Int = 0, UInt = 1, Float = 2, Bfloat = 4, Complex = 5, Bool = 6,
    Float8_E3M4 = 7, Float8_E4M3 = 8, Float8_E4M3B11FNUZ = 9,
    Float8_E4M3FN = 10, Float8_E4M3FNUZ = 11, Float8_E5M2 = 12,
    Float8_E5M2FNUZ = 13, Float8_E8M0FNU = 14,
    Float6_E2M3FN = 15, Float6_E3M2FN = 16,
    Float4_E2M1FN = 17
};

struct device {
    int32_t device_type = 0;
    int32_t device_id = 0;
};

struct dtype {
    uint8_t code = 0;
    uint8_t bits = 0;
    uint16_t lanes = 0;

    constexpr bool operator==(const dtype &o) const {
        return code == o.code && bits == o.bits && lanes == o.lanes;
    }

    constexpr bool operator!=(const dtype &o) const { return !operator==(o); }
};

struct dltensor {
    void *data = nullptr;
    nanobind::dlpack::device device;
    int32_t ndim = 0;
    nanobind::dlpack::dtype dtype;
    int64_t *shape = nullptr;
    int64_t *strides = nullptr;
    uint64_t byte_offset = 0;
};

NAMESPACE_END(dlpack)

#define NB_FRAMEWORK(Name, Value, label)                                       \
    struct Name {                                                              \
        static constexpr auto name = detail::const_name(label);                \
        static constexpr int value = Value;                                    \
        static constexpr bool is_framework = true;                             \
    }

#define NB_DEVICE(Name, Value)                                                 \
    struct Name {                                                              \
        static constexpr auto name = detail::const_name("device='" #Name "'"); \
        static constexpr int value = Value;                                    \
        static constexpr bool is_device_type = true;                           \
    }

#define NB_ORDER(Name, Value)                                                  \
    struct Name {                                                              \
        static constexpr auto name = detail::const_name("order='" Value "'");  \
        static constexpr char value = Value[0];                                \
        static constexpr bool is_order = true;                                 \
    }

NB_ORDER(c_contig, "C");
NB_ORDER(f_contig, "F");
NB_ORDER(any_contig, "A");

NB_FRAMEWORK(no_framework, 0, "ndarray");
NB_FRAMEWORK(numpy, 1, "numpy.ndarray");
NB_FRAMEWORK(pytorch, 2, "torch.Tensor");
NB_FRAMEWORK(tensorflow, 3, "tensorflow.python.framework.ops.EagerTensor");
NB_FRAMEWORK(jax, 4, "jaxlib.xla_extension.DeviceArray");
NB_FRAMEWORK(cupy, 5, "cupy.ndarray");
NB_FRAMEWORK(memview, 6, "memoryview");
NB_FRAMEWORK(array_api, 7, "ArrayLike");

NAMESPACE_BEGIN(device)
NB_DEVICE(none, 0); NB_DEVICE(cpu, 1); NB_DEVICE(cuda, 2);
NB_DEVICE(cuda_host, 3); NB_DEVICE(opencl, 4); NB_DEVICE(vulkan, 7);
NB_DEVICE(metal, 8); NB_DEVICE(rocm, 10); NB_DEVICE(rocm_host, 11);
NB_DEVICE(cuda_managed, 13); NB_DEVICE(oneapi, 14);
NAMESPACE_END(device)

#undef NB_FRAMEWORK
#undef NB_DEVICE
#undef NB_ORDER

template <typename T> struct ndarray_traits {
    static constexpr bool is_complex = detail::is_complex_v<T>;
    static constexpr bool is_float   = std::is_floating_point_v<T>;
    static constexpr bool is_bool    = std::is_same_v<std::remove_cv_t<T>, bool>;
    static constexpr bool is_int     = std::is_integral_v<T> && !is_bool;
    static const