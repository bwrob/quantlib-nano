#    define QL_FASTER_LAZY_OBJECTS
#endif

/* If defined, `std::any` and related classes and functions will be
   used instead of `boost::any`. If undefined, the Boost facilities
   will be used.
*/
#ifndef QL_USE_STD_ANY

#    define QL_USE_STD_ANY
#endif

/* If defined, `std::optional` and related classes and functions will
   be used instead of `boost::optional`. If undefined, the Boost
   facilities will be used.
*/
#ifndef QL_USE_STD_OPTIONAL

#    define QL_USE_STD_OPTIONAL
#endif

/* If defined, `std::shared_ptr` and related classes and functions
   will used instead of `boost::shared_ptr`. If undefined, the Boost
   facilities will be used. Note that `std::shared_ptr` does not check
   access and can cause segmentation faults.
*/
#ifndef QL_USE_STD_SHARED_PTR
//#    define QL_USE_STD_SHARED_PTR
#endif

/* If defined, `Null` will be implemented as a template function.
   This allows the code to work with user-defined `Real` types but was
   reported to cause internal compiler errors with Visual C++ 2022 in
   some cases.  If undefined, `Null` will be implemented as a class
   template, as in previous releases.
*/
#ifndef QL_NULL_AS_FUNCTIONS
//#    define QL_NULL_AS_FUNCTIONS
#endif

/* If defined, a parallel unit test runner will be used to execute the
   C++ test suite. This will reduce the runtime on multi core CPUs.
*/
#ifndef QL_ENABLE_PARALLEL_UNIT_TEST_RUNNER
//#    define QL_ENABLE_PARALLEL_UNIT_TEST_RUNNER
#endif

#endif