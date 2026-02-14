/////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "string.h"

//
// C String lists tests:
//   Two consecutive params (const char *, int | size_t) are exported as List[str]
//
// The following function will be exported with the following python signature:
// -->    def c_string_list_total_size(items: List[str], output_0: BoxedInt, output_1: BoxedInt) -> int:
//
MY_API inline size_t c_string_list_total_size(const char * const items[], int items_count, int output[2])
{
    size_t total = 0;
    for (size_t i = 0; i < items_count; ++i)
        total += strlen(items[i]);
    output[0] = (int)total;
    output[1] = (int)(total + 1);
    return total;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/modifiable_immutable_test.h included by mylib/mylib_main/mylib.h                 //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <string>

//
// Modifiable immutable python types test
//

// litgen adapts functions params that use modifiable pointer or reference to a type
// that is immutable in python.
// On the C++ side, these params are modifiable by the function.
// We need to box them into a Boxed type to ensure that any modification made by C++
// is visible when going back to Python.
//
// Note: immutable data types in python are
//   - Int, Float, String (correctly handled by litgen)
//   - Complex, Bytes (not handled)
//   - Tuple (not handled)


/////////////////////////////////////////////////////////////////////////////////////////////
// Test Part 1: in the functions below, the value parameters will be "Boxed"
//
// This is caused by the following options during generation:
//     options.fn_params_replace_modifiable_immutable_by_boxed__regex = code_utils.join_string_by_pipe_char([
//         r"^Toggle",
//         r"^Modify",
//      ])
/////////////////////////////////////////////////////////////////////////////////////////////


// Test with pointer:
// Will be published in python as:
// -->    def toggle_bool_pointer(v: BoxedBool) -> None:
MY_API void ToggleBoolPointer(bool *v)
{
    *v = !(*v);
}

// Test with nullable pointer
// Will be published in python as:
// -->    def toggle_bool_nullable(v: BoxedBool = None) -> None:
MY_API void ToggleBoolNullable(bool *v = NULL)
{
    if (v != NULL)
        *v = !(*v);
}

// Test with reference
// Will be published in python as:
// -->    def toggle_bool_reference(v: BoxedBool) -> None:
MY_API void ToggleBoolReference(bool &v)
{
    v = !(v);
}

// Test modifiable String
// Will be published in python as:
// -->    def modify_string(s: BoxedString) -> None:
MY_API void ModifyString(std::string* s) { (*s) += "hello"; }


/////////////////////////////////////////////////////////////////////////////////////////////
//
// Test Part 2: in the functions below, the python return type is modified:
// the python functions will return a tuple:
//     (original_return_value, modified_parameter)
//
// This is caused by the following options during generation:
//
//     options.fn_params_output_modifiable_immutable_to_return__regex = r"^Change"
/////////////////////////////////////////////////////////////////////////////////////////////


// Test with int param + int return type
// Will be published in python as:
// --> def change_bool_int(label: str, value: int) -> Tuple[bool, int]:
MY_API bool ChangeBoolInt(const char* label, int * value)
{
    *value += 1;
    return true;
}

// Will be published in python as:
// -->    def change_void_int(label: str, value: int) -> int:
MY_API void ChangeVoidInt(const char* label, int * value)
{
    *value += 1;
}

// Will be published in python as:
// -->    def change_bool_int2(label: str, value1: int, value2: int) -> Tuple[bool, int, int]:
MY_API bool ChangeBoolInt2(const char* label, int * value1, int *
