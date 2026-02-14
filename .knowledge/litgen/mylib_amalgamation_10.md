
        return r;
    }

    // Method that requires a parameter adaptation
    MY_API T sum2(const T v[2])
    {
        return sum() + v[0] + v[1];
    }
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/c_extern_c.h included by mylib/mylib_main/mylib.h                                //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*

Here, we test litgen with C libraries, such a glfw:

Features:
 - Handle #ifdef __cpluscplus
    __cpluscplus should be assumed to be always true
 - Handle extern:
        extern "C" { ... }
    The code inside such a block should be parsed as if extern was not there.
 - Handle functions with a void instead of empty params:
        void foo(void)
 - unnamed params:
        void blah(int)
 - Export #define as variable
    #define GLFW_KEY_LEFT_BRACKET       91  / * [ * /
    #define GLFW_PLATFORM_ERROR         0x00010008
    etc.
*/

#ifdef __cplusplus
extern "C" {
#endif

MY_API int extern_c_add(int a, int b) { return a + b; }

MY_API int foo_void_param(void) { return 42; }

MY_API int foo_unnamed_param(int , bool, float) { return 42; }

// This is zero
#define MY_ANSWER_ZERO_COMMENTED 0 // Will be published with is comment

// Will be published with its two comments (incl this one)
#define MY_ANSWER_ONE_COMMENTED 1 // This is one


#define MY_HEXVALUE 0x43242 // Will be published
#define MY_OCTALVALUE 043242 // Will be published
#define MY_STRING "Hello" // Will be published
#define MY_FLOAT 3.14 // Will be published

#define MY_ANSWER(x) (x + 42) // Will not be published!
#define MY_DEFINE_NO_VALUE // Will not be published!
#define MY_BROKEN_FLOAT 3.14.12345 // Will not be published!
#define MY_FUNCTION_CALL f(3.14) // Will not be published!

#ifdef __cplusplus
}
#endif

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/class_default_ctor_test.h included by mylib/mylib_main/mylib.h                   //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


namespace A
{
    enum class Foo
    {
        Foo1 = 0,
        Foo2 = 1,
        Foo3 = 2
    };

    // This struct has no default constructor, so a default named constructor
    // will be provided for python
    struct ClassNoDefaultCtor
    {
        bool b = true;
        int a;
        int c = 3;
        Foo foo = Foo::Foo1;
        const std::string s = "Allo";
    };

    namespace N
    {
        struct S {};
        enum class EC { a = 0 };
        enum E { E_a = 0 };

        MY_API void Foo(EC e = EC::a) {}
        MY_API void Foo(E e = E_a) {}
        MY_API void Foo(S s = S(), E e = E_a) {}
    }

}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/smart_ptr.h included by mylib/mylib_main/mylib.h                                 //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// With pybind11, SmartElem is mentioned in options.class_held_as_shared__regex
// (because it might be stored as a shared_ptr in the generated code)
struct SmartElem {
    int x = 0;
};


MY_API inline std::shared_ptr<SmartElem> make_shared_elem(int x)
{
    auto r = std::make_shared<SmartElem>();
    r->x = x;
    return r;
}


class ElemContainer
{
public:
    ElemContainer():
        vec { {1}, {2}},
        shared_ptr(make_shared_elem(3)),
        vec_shared_ptrs { make_shared_elem(4), make_shared_elem(5) }
    {
    }

    std::vector<SmartElem> vec;
    std::shared_ptr<SmartElem> shared_ptr;
    std::vector<std::shared_ptr<SmartElem>> vec_shared_ptrs;
};


// The signature below is incompatible with pybind11:
//     void change_unique_elem(std::unique_ptr<Ele
