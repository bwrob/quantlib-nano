   \code
    QL_TRACE(message);
    \endcode
    can be used to output a trace of the code being executed. If
    tracing was disabled during configuration, such statements are
    removed by the preprocessor for maximum performance; if it was
    enabled, whether and where the message is output depends on the
    current settings.
*/

/*! \def QL_TRACE_ENTER_FUNCTION
    \brief output tracing information

    The statement
    \code
    QL_TRACE_ENTER_FUNCTION;
    \endcode
    can be used at the beginning of a function to trace the fact that
    the program execution is entering such function. It should be
    paired with a corresponding QL_TRACE_EXIT_FUNCTION macro. Such
    statement might be ignored; refer to QL_TRACE for details. Also,
    function information might not be available depending on the
    compiler.
*/

/*! \def QL_TRACE_EXIT_FUNCTION
    \brief output tracing information

    The statement
    \code
    QL_TRACE_EXIT_FUNCTION;
    \endcode
    can be used before returning from a function to trace the fact
    that the program execution is exiting such function. It should be
    paired with a corresponding QL_TRACE_ENTER_FUNCTION macro. Such
    statement might be ignored; refer to QL_TRACE for details. Also,
    function information might not be available depending on the
    compiler.
*/

/*! \def QL_TRACE_LOCATION
    \brief output tracing information

    The statement
    \code
    QL_TRACE_LOCATION;
    \endcode
    can be used to trace the current file and line. Such statement
    might be ignored; refer to QL_TRACE for details.
*/

/*! \def QL_TRACE_VARIABLE
    \brief output tracing information

    The statement
    \code
    QL_TRACE_VARIABLE(variable);
    \endcode
    can be used to trace the current value of a variable. Such
    statement might be ignored; refer to QL_TRACE for details. Also,
    the variable type must allow sending it to an output stream.
*/

/*! @} */

/*! @} */

#if defined(QL_ENABLE_TRACING)

#define QL_DEFAULT_TRACER   QuantLib::detail::Tracing::instance()

#define QL_TRACE_ENABLE \
QL_DEFAULT_TRACER.enable()

#define QL_TRACE_DISABLE \
QL_DEFAULT_TRACER.disable()

#define QL_TRACE_ON(out) \
QL_DEFAULT_TRACER.setStream(out)

#define QL_TRACE(message) \
if (QL_DEFAULT_TRACER.enabled()) \
    try { \
        QL_DEFAULT_TRACER.stream() << "trace[" << QL_DEFAULT_TRACER.depth() \
                                   << "]: " << message << std::endl; \
    } catch (...) {} \
else

#define QL_TRACE_ENTER_FUNCTION \
if (QL_DEFAULT_TRACER.enabled()) \
    try { \
        QL_DEFAULT_TRACER.down(); \
        QL_DEFAULT_TRACER.stream() << "trace[" << QL_DEFAULT_TRACER.depth() \
                                   << "]: " \
                                   << "Entering " << BOOST_CURRENT_FUNCTION \
                                   << std::endl; \
    } catch (...) {} \
else

#define QL_TRACE_EXIT_FUNCTION \
if (QL_DEFAULT_TRACER.enabled()) \
    try { \
        QL_DEFAULT_TRACER.stream() << "trace[" << QL_DEFAULT_TRACER.depth() \
                                   << "]: " \
                                   << "Exiting " << BOOST_CURRENT_FUNCTION \
                                   << std::endl; \
        QL_DEFAULT_TRACER.up(); \
    } catch (...) { QL_DEFAULT_TRACER.up(); } \
else

#define QL_TRACE_LOCATION \
QL_TRACE("At line " << __LINE__ << " in " << __FILE__)

#define QL_TRACE_VARIABLE(variable) \
QL_TRACE(#variable << " = " << variable)

#else

#define QL_DEFAULT_TRACER
#define QL_TRACE_ENABLE
#define QL_TRACE_DISABLE
#define QL_TRACE_ON(out)
#define QL_TRACE(message)
#define QL_TRACE_ENTER_FUNCTION
#define QL_TRACE_EXIT_FUNCTION
#define QL_TRACE_LOCATION
#define QL_TRACE_VARIABLE(variable)

#endif

#endif