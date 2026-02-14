  # Note: if you want to override protected functions, also fill `class_expose_protected_methods__regex`
    class_override_virtual_methods_in_python__regex: str = ""
 */

namespace Root
{
    namespace Inner
    {
        class MyVirtualClass
        {
        public:
            virtual ~MyVirtualClass() = default;

            MY_API std::string foo_concrete(int x, const std::string& name)
            {
                std::string r =
                      std::to_string(foo_virtual_protected(x))
                    + "_" + std::to_string(foo_virtual_public_pure())
                    + "_" + foo_virtual_protected_const_const(name);
                return r;
            }

            MY_API virtual int foo_virtual_public_pure() const = 0;
        protected:
            MY_API virtual int foo_virtual_protected(int x) const { return 42 + x; }
            MY_API virtual std::string foo_virtual_protected_const_const(const std::string& name) const {
                return std::string("Hello ") + name;
            }
        };

        // Here, we test Combining virtual functions and inheritance
        // See https://pybind11.readthedocs.io/en/stable/advanced/classes.html#combining-virtual-functions-and-inheritance
        class MyVirtualDerivate: public MyVirtualClass
        {
        public:
            MyVirtualDerivate(): MyVirtualClass() {};
            MY_API int foo_virtual_public_pure() const override { return 53; };
            MY_API virtual int foo_derivate() { return 48; }
        };
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/return_value_policy_test.h included by mylib/mylib_main/mylib.h                  //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//
// return_value_policy:
//
// If a function has an end-of-line comment which contains
//    `return_value_policy::reference` or `rv_policy::reference` (for nanobind),
// and if this function returns a pointer or a reference, litgen will automatically add
// `pybind11::return_value_policy::reference` when publishing it.
//
// Notes: `reference` could be replaced by `take_ownership`,
//   or any other member of `pybind11::return_value_policy` or `nb::rv_policy` (for nanobind)
//
// You can also set a global options for matching functions names that return a reference or a pointer
//     see
//             LitgenOptions.fn_return_force_policy_reference_for_pointers__regex
//     and
//             LitgenOptions.fn_return_force_policy_reference_for_references__regex: str = ""


struct MyConfig
{
    //
    // For example, singletons (such as the method below) should be returned as a reference,
    // otherwise python might destroy the singleton instance as soon as it goes out of scope.
    //

    MY_API static MyConfig& Instance() // return_value_policy::reference
    {
        static MyConfig instance;
        return instance;
    }

    int value = 0;
};

MY_API MyConfig* MyConfigInstance() { return & MyConfig::Instance(); } // return_value_policy::reference

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/inner_class_test.h included by mylib/mylib_main/mylib.h                          //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


namespace SomeNamespace
{
    struct ParentStruct
    {
        struct InnerStruct
        {
            int value;

            InnerStruct(int value = 10) : value(value) {}
            MY_API int add(int a, int b) { return a + b; }
        };

        enum class InnerEnum
        {
            Zero = 0,
            One,
            Two,
            Three
        };

        InnerStruct inner_struct = InnerStruct();
        InnerEnum inner_enum = InnerEnum::Three;
    };
} // namespace Som