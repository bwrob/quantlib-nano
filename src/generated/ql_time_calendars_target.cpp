
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/time/calendars/target.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_time_calendars_target(nb::module_ &m) {
    nb::module_ &sub_m = m; 
////////////////////    <generated_from:target.hpp>    ////////////////////
// #ifndef quantlib_target_calendar_h
// 
// #endif
// 

{ // <namespace QuantLib>
    nb::module_ sub_m = m.def_submodule("quant_lib", "");
    auto sub_m_ClassTARGET =
        nb::class_<QuantLib::TARGET>
            (sub_m, "TARGET", "! Holidays (see http://www.ecb.int):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday (since 2000)</li>\n        <li>Easter Monday (since 2000)</li>\n        <li>Labour Day, May 1st (since 2000)</li>\n        <li>Christmas, December 25th</li>\n        <li>Day of Goodwill, December 26th (since 2000)</li>\n        <li>December 31st (1998, 1999, and 2001)</li>\n        </ul>\n\n        \\ingroup calendars\n\n        \test the correctness of the returned results is tested\n              against a list of known holidays.\n")
        .def(nb::init<>())
        ;
} // </namespace QuantLib>
////////////////////    </generated_from:target.hpp>    ////////////////////

}
