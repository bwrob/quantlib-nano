value2)
{
    *value1 += 1;
    *value2 += 2;
    return false;
}

// Will be published in python as:
// -->    def change_void_int_default_null(label: str, value: Optional[int] = None) -> Tuple[bool, Optional[int]]:
MY_API bool ChangeVoidIntDefaultNull(const char* label, int * value = nullptr)
{
    if (value != nullptr)
        *value += 1;
    return true;
}

// Will be published in python as:
// -->    def change_void_int_array(label: str, value: List[int]) -> Tuple[bool, List[int]]:
MY_API bool ChangeVoidIntArray(const char* label, int value[3])
{
    value[0] += 1;
    value[1] += 2;
    value[2] += 3;
    return true;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/overload_test.h included by mylib/mylib_main/mylib.h                             //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//
// litgen is able to detect automatically the presence of overloads that require
// to use `py::overload_cast<...>` when publishing
//

//
// overload on free functions
//

MY_API int add_overload(int a, int b) { return a + b; } // type: ignore
MY_API int add_overload(int a, int b, int c) { return a + b + c; } // type: ignore

//
// overload on methods
//

struct FooOverload
{
    MY_API int add_overload(int a, int b) { return a + b; } // type: ignore
    MY_API int add_overload(int a, int b, int c) { return a + b + c; } // type: ignore
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/enum_test.h included by mylib/mylib_main/mylib.h                                 //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// BasicEnum: a simple C-style enum
enum BasicEnum
{
    // C-style enums often contain a prefix that is the enum name in itself, in order
    // not to pollute the parent namespace.
    // Since enum members do not leak to the parent namespace in python, litgen will remove the prefix by default.

    BasicEnum_a = 1, // This will be exported as BasicEnum.a
    BasicEnum_aa,    // This will be exported as BasicEnum.aa
    BasicEnum_aaa,   // This will be exported as BasicEnum.aaa

    // Lonely comment

    // This is value b
    BasicEnum_b,

    BasicEnum_count // By default this "count" item is not exported: see options.enum_flag_skip_count
};


// ClassEnum: a class enum that should be published
enum class ClassEnum
{
    On = 0,
    Off,
    Unknown
};


// EnumDetail should not be published, as its name ends with "Detail"
// (see `options.enum_exclude_by_name__regex = "Detail$"` inside autogenerate_mylib.py)
enum class EnumDetail
{
    On,
    Off,
    Unknown
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/class_test.h included by mylib/mylib_main/mylib.h                                //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <vector>


// This is the class doc. It will be published as MyClass.__doc__
class MyClass
{
public:
    MyClass(int factor = 10, const std::string& message = "hello"): factor(factor), message(message) {}
    ~MyClass() {}


    ///////////////////////////////////////////////////////////////////////////
    // Simple struct members
    ///////////////////////////////////////////////////////////////////////////
    int factor = 10, delta = 0;
    std::string message;


    ///////////////////////////////////////////////////////////////////////////
    // Stl container members
    ///////////////////////////////////////////////////////////////////////////

    // By default, modifications from python are not propagated to C++ for stl containers
    // (se