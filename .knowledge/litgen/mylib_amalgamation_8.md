gex)
{
    MY_API int FooDetails() { return 43; }
}

namespace // MY_API This anonymous namespace should be excluded
{
    MY_API int LocalFunction() { return 44; }
}

namespace Mylib  // MY_API This namespace should not be outputted as a submodule (it is considered a root namespace)
{
    // this is an inner namespace (this comment should become the namespace doc)
    namespace Inner
    {
        MY_API int FooInner() { return 45; }
    }

    // This is a second occurrence of the same inner namespace
    // The generated python module will merge these occurrences
    // (and this comment will be ignored, since the Inner namespace already has a doc)
    namespace Inner
    {
        MY_API int FooInner2() { return 46; }
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/operators.h included by mylib/mylib_main/mylib.h                                 //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct IntWrapper
{
    int value;
    IntWrapper(int v) : value(v) {}

    // arithmetic operators
    MY_API IntWrapper operator+(IntWrapper b) { return IntWrapper{ value + b.value}; }
    MY_API IntWrapper operator-(IntWrapper b) { return IntWrapper{ value - b.value }; }

    // Unary minus operator
    MY_API IntWrapper operator-() { return IntWrapper{ -value }; }

    // Comparison operator
    MY_API bool operator<(IntWrapper b) { return value < b.value; }

    // Two overload of the += operator
    MY_API IntWrapper operator+=(IntWrapper b) { value += b.value; return *this; }
    MY_API IntWrapper operator+=(int b) { value += b; return *this; }

    // Two overload of the call operator, with different results
    MY_API int operator()(IntWrapper b) { return value * b.value + 2; }
    MY_API int operator()(int b) { return value * b + 3; }
};


struct IntWrapperSpaceship
{
    int value;

    IntWrapperSpaceship(int v): value(v) {}

    // Test spaceship operator, which will be split into 5 operators in Python!
    // ( <, <=, ==, >=, >)
    // Since we have two overloads, 10 python methods will be built
    MY_API int operator<=>(IntWrapperSpaceship& o) { return value - o.value; }
    MY_API int operator<=>(int& o) { return value - o; }
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/call_policies_test.h included by mylib/mylib_main/mylib.h                        //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <iostream>

struct CallGuardLogger;


// ============================================================================
// call_guard
// ============================================================================
// If you add a comment to the function with reads:
//     py::call_guard<YourCallGuard>()
// Then, it will be taken into account
// See https://pybind11.readthedocs.io/en/stable/advanced/functions.html#call-guard
// The comment may be a comment on previous line or an end-of-line comment

MY_API void call_guard_tester() // py::call_guard<CallGuardLogger>()
{
    std::cout << "call_guard_tester\n";
}


// ============================================================================
// keep-alive
// ============================================================================
// If you add a comment to the function with reads:
//     py::keep-alive<1, 2>()
// Then, it will be taken into account
// See https://pybind11.readthedocs.io/en/stable/advanced/functions.html#keep-alive
// The comment may be a comment on previous line or an end-of-line comment
//
// (No integration test implemented for this)


// ============================================================================
// return value policy
// => see doc inside return_value_policy_test.h
// ===============
