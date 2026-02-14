#    define QL_ENABLE_THREAD_SAFE_OBSERVER_PATTERN
#endif

/* If defined, date objects willsupport an intraday datetime
   resolution down to microseconds.  Strictly monotone daycounters
   (`Actual360`, `Actual365Fixed` and `ActualActual`) will take the
   additional information into account and allow for accurate intraday
   pricing.  If undefined, the smallest resolution of date objects is
   a single day.  Intraday datetime resolution is experimental.
*/
#ifndef QL_HIGH_RESOLUTION_DATE
//#    define QL_HIGH_RESOLUTION_DATE
#endif

/* If defined, lazy objects will raise an exception when they detect a
   notification cycle which would result in an infinite recursion
   loop. If undefined, they will break the recursion without throwing.
   Enabling this option is recommended but might cause existing code
   to throw.
*/
#ifndef QL_THROW_IN_CYCLES
//#    define QL_THROW_IN_CYCLES
#endif

/* If defined, lazy objects will forward the first notification
   received, and discard the others until recalculated; the rationale
   is that observers were already notified, and don't need further
   notifications until they recalculate, at which point this object
   would be recalculated too.  After recalculation, this object would
   again forward the first notification received.  Although not always
   correct, this behavior is a lot faster and thus is the current
   default.
*/
#ifndef QL_FASTER_LAZY_OBJECTS

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