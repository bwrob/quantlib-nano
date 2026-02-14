 -->    def add_c_array2(values: List[int]) -> int:
// (and the runtime will check that the list size is exactly 2)
MY_API inline int const_array2_add(const int values[2]) { return values[0] + values[1];}


// Test with a modifiable array: since the input array is not const, it could be modified.
// Thus, it will be published as a function accepting Boxed values:
// -->    def array2_modify(values_0: BoxedUnsignedLong, values_1: BoxedUnsignedLong) -> None:
MY_API inline void array2_modify(unsigned long values[2])
{
    values[0] = values[1] + values[0];
    values[1] = values[0] * values[1];
}

struct Point2
{
    int x, y;
};

// Test with a modifiable array that uses a user defined struct.
// Since the user defined struct is mutable in python, it will not be Boxed,
// and the python signature will be:
//-->    def get_points(out_0: Point2, out_1: Point2) -> None:
MY_API inline void array2_modify_mutable(Point2 out[2]) { out[0] = {0, 1}; out[1] = {2, 3}; }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/c_style_buffer_to_pyarray_test.h included by mylib/mylib_main/mylib.h            //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <stdint.h>
#include <stddef.h>

//
// C Style buffer to py::array tests
//
// litgen is able to recognize and transform pairs of params whose C++ signature resemble
//     (T* data, size_t|int count)
// Where
//   * `T` is a *known* numeric type, or a templated type
//   * `count` name resemble a size
//        (see LitgenOptions.fn_params_buffer_size_names__regex)
//

// add_inside_buffer: modifies a buffer by adding a value to its elements
// Will be published in python as:
// -->    def add_inside_buffer(buffer: np.ndarray, number_to_add: int) -> None:
// Warning, the python function will accept only uint8 numpy arrays, and check it at runtime!
MY_API inline void add_inside_buffer(uint8_t* buffer, size_t buffer_size, uint8_t number_to_add)
{
    for (size_t i  = 0; i < buffer_size; ++i)
        buffer[i] += number_to_add;
}

// buffer_sum: returns the sum of a *const* buffer
// Will be published in python as:
// -->    def buffer_sum(buffer: np.ndarray, stride: int = -1) -> int:
MY_API inline int buffer_sum(const uint8_t* buffer, size_t buffer_size, size_t stride= sizeof(uint8_t))
{
    int sum = 0;
    for (size_t i  = 0; i < buffer_size; ++i)
        sum += (int)buffer[i];
    return sum;
}

// add_inside_two_buffers: modifies two mutable buffers
// litgen will detect that this function uses two buffers of same size.
// Will be published in python as:
// -->    def add_inside_two_buffers(buffer_1: np.ndarray, buffer_2: np.ndarray, number_to_add: int) -> None:
MY_API inline void add_inside_two_buffers(uint8_t* buffer_1, uint8_t* buffer_2, size_t buffer_size, uint8_t number_to_add)
{
    for (size_t i  = 0; i < buffer_size; ++i)
    {
        buffer_1[i] += number_to_add;
        buffer_2[i] += number_to_add;
    }
}

// templated_mul_inside_buffer: template function that modifies an array by multiplying its elements by a given factor
// litgen will detect that this function can be published as using a numpy array.
// It will be published in python as:
// -->    def mul_inside_buffer(buffer: np.ndarray, factor: float) -> None:
//
// The type will be detected at runtime and the correct template version will be called accordingly!
// An error will be thrown if the numpy array numeric type is not supported.
template<typename T> MY_API void templated_mul_inside_buffer(T* buffer, size_t buffer_size, double factor)
{
    for (size_t i  = 0; i < buffer_size; ++i)
        buffer[i] *= (T)factor;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/c_string_list_test.h included by mylib/mylib_main/mylib.h                        //
/////