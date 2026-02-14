=============================================================


// ============================================================================
// CallGuardLogger: dummy call guard for the tests
// ============================================================================
struct CallGuardLogger
{
    CallGuardLogger() {
        ++nb_construct;
    }
    ~CallGuardLogger() {
        ++nb_destroy;
    }

    static int nb_construct;
    static int nb_destroy;
};

int CallGuardLogger::nb_construct = 0;
int CallGuardLogger::nb_destroy = 0;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/qualified_scoping_test.h included by mylib/mylib_main/mylib.h                    //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


namespace N
{
    struct S {};
    enum class EC { a = 0 };
    enum E { E_a = 0 };

    MY_API void Foo(EC e = EC::a) {}
    MY_API void Foo(E e = E_a) {}
    MY_API void Foo(S s = S(), E e = E_a) {}
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/template_function_test.h included by mylib/mylib_main/mylib.h                    //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// AddTemplated is a template function that will be implemented for the types ["int", "double", "std::string"]
//
// See inside autogenerate_mylib.py:
//     options.fn_template_options.add_specialization(r"^AddTemplated$", ["int", "double", "std::string"])

template<typename T>
MY_API T AddTemplated(T a, T b)
{
    return  a + b;
}


// SumVectorAndCArray is a template function that will be implemented for the types ["int", "std::string"]
//
// Here, we test two additional thing:
//  - nesting of the T template parameter into a vector
//  - mixing template and function parameter adaptations (here other_values[2] will be transformed into a List[T]
//
// See inside autogenerate_mylib.py:
//     options.fn_template_options.SumVectorAndCArray(r"^SumVector", ["int", "std::string"])

template<typename T>
MY_API T SumVectorAndCArray(std::vector<T> xs, const T other_values[2])
{
    T sum = T{};
    for (const T & v: xs )
        sum += v;
    sum += other_values[0];
    sum += other_values[1];
    return sum;
}


// Same test, as a method

struct FooTemplateFunctionTest
{
    template<typename T>
    MY_API T SumVectorAndCArray(std::vector<T> xs, const T other_values[2])
    {
        T sum = T{};
        for (const T & v: xs )
            sum += v;
        sum += other_values[0];
        sum += other_values[1];
        return sum;
    }
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/template_class_test.h included by mylib/mylib_main/mylib.h                       //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


//  MyTemplateClass is a template class that will be implemented for the types ["int", "std::string"]
//
// See inside autogenerate_mylib.py:
//        options.class_template_options.add_specialization(
//            class_name_regex=r"^MyTemplateClass$",  # r".*" => all classes
//        cpp_types_list=["int", "double"],  # instantiated types
//        naming_scheme=litgen.TemplateNamingScheme.camel_case_suffix,
//        )

template<typename T>
struct MyTemplateClass
{
public:
    std::vector<T> values;

    // Standard constructor
    MyTemplateClass() {}

    // Constructor that will need a parameter adaptation
    MyTemplateClass(const T v[2]) {
        values.push_back(v[0]);
        values.push_back(v[1]);
    }

    // Standard method
    MY_API T sum()
    {
        T r = {};
        for (const auto & x: values)
            r += x;