#include <nanobind/nanobind.h>
#include "generated/registration.h"
#include <iostream>

namespace nb = nanobind;

NB_MODULE(quantlib_nano_cpp, m) {
    m.doc() = "QuantLib Python bindings using nanobind and litgen";

    gen_ql_patterns_observable(m);
    // gen_ql_quote(m); // Failed to generate
    gen_ql_handle(m);
    // gen_ql_patterns_lazyobject(m); // Failed to generate
    // gen_ql_termstructure(m); // Failed to generate
    gen_ql_termstructures_yieldtermstructure(m);
    gen_ql_termstructures_yield_flatforward(m);
    gen_ql_time_date(m);
    gen_ql_settings(m);
    gen_ql_time_calendars_target(m);
    gen_ql_time_daycounters_actual365fixed(m);
    gen_ql_time_timeunit(m);
    gen_ql_time_calendar(m);
}
