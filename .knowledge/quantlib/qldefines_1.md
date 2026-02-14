#   define QL_REAL double
#endif


/*! \defgroup macros QuantLib macros

    Global definitions and a few macros which help porting the
    code to different compilers.

    @{
*/

#if (defined(_DEBUG) || defined(DEBUG))
    #define QL_DEBUG
#endif

#if   defined(HAVE_CONFIG_H)    // Dynamically created by configure
   #include <ql/config.hpp>
/* Use BOOST_MSVC instead of _MSC_VER since some other vendors (Metrowerks,
   for example) also #define _MSC_VER
*/
#elif defined(BOOST_MSVC)       // Microsoft Visual C++
   #include <ql/config.msvc.hpp>
#elif defined(__MINGW32__)      // Minimalistic GNU for Windows
   #include <ql/config.mingw.hpp>
#elif defined(__SUNPRO_CC)      // Sun Studio
   #include <ql/config.sun.hpp>
#else                           // We hope that the compiler follows ANSI
   #include <ql/config.ansi.hpp>
#endif


// extra debug checks
#ifdef QL_DEBUG
    #ifndef QL_EXTRA_SAFETY_CHECKS
        #define QL_EXTRA_SAFETY_CHECKS
    #endif
#endif

#ifdef QL_ENABLE_THREAD_SAFE_OBSERVER_PATTERN
    #if BOOST_VERSION < 105800
        #error Boost version 1.58 or higher is required for the thread-safe observer pattern
    #endif
#endif

#ifdef QL_ENABLE_PARALLEL_UNIT_TEST_RUNNER
    #if BOOST_VERSION < 105900
        #error Boost version 1.59 or higher is required for the parallel unit test runner
    #endif
#endif

// ensure that needed math constants are defined
#include <ql/mathconstants.hpp>


// import global functions into std namespace
#if defined(BOOST_NO_STDC_NAMESPACE)
    #include <cmath>
    namespace std {
        using ::sqrt; using ::abs; using ::fabs;
        using ::exp; using ::log; using ::pow;
        using ::sin; using ::cos; using ::asin; using ::acos;
        using ::sinh; using ::cosh;
        using ::floor; using ::fmod; using ::modf;
    }
#endif


/*! \defgroup limitMacros Numeric limits

    Some compilers do not give an implementation of
    <code>\<limits\></code> yet.  For the code to be portable
    these macros should be used instead of the corresponding method of
    <code>std::numeric_limits</code> or the corresponding macro
    defined in <code><limits.h></code>.

    @{
*/
/*! \def QL_MIN_INTEGER
    Defines the value of the largest representable negative integer value
*/
/*! \def QL_MAX_INTEGER
    Defines the value of the largest representable integer value
*/
/*! \def QL_MIN_REAL
    Defines the value of the largest representable negative
    floating-point value
*/
/*! \def QL_MIN_POSITIVE_REAL
    Defines the value of the smallest representable positive double value
*/
/*! \def QL_MAX_REAL
    Defines the value of the largest representable floating-point value
*/
/*! \def QL_EPSILON
    Defines the machine precision for operations over doubles
*/
#include <limits>
// limits used as such
#define QL_MIN_INTEGER         ((std::numeric_limits<QL_INTEGER>::min)())
#define QL_MAX_INTEGER         ((std::numeric_limits<QL_INTEGER>::max)())
#define QL_MIN_REAL           -((std::numeric_limits<QL_REAL>::max)())
#define QL_MAX_REAL            ((std::numeric_limits<QL_REAL>::max)())
#define QL_MIN_POSITIVE_REAL   ((std::numeric_limits<QL_REAL>::min)())
#define QL_EPSILON             ((std::numeric_limits<QL_REAL>::epsilon)())
/*! @} */

/*! @}  */


// For the time being we're keeping a QL_DEPRECATED macro because
// of <https://stackoverflow.com/questions/38378693/>.  We need to
// use it to deprecate constructors until we drop support for VC++2015.
// Other features (methods, typedefs etc.) can use [[deprecated]] and
// possibly add a message.

// emit warning when using deprecated features
// clang-format off
#if defined(BOOST_MSVC)       // Microsoft Visual C++

#    define QL_DEPRECATED __declspec(deprecated)

#    define QL_DEPRECATED_DISABLE_WARNING \
        __pragma(warning(push))           \
        __pragma(warning(disable : 4996))

#    define QL_DEPRECATED_ENABLE_WARNING \
        __pragma(warning(pop))
#elif defined(__clang__)
