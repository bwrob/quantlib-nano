
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/time/timeunit.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_time_timeunit(nb::module_ &m) {
    nb::module_ &sub_m = m; 
////////////////////    <generated_from:timeunit.hpp>    ////////////////////
// #ifndef quantlib_timeunit_hpp
// 
// #endif
// 

{ // <namespace QuantLib>
    nb::module_ sub_m = m.def_submodule("quant_lib", "");
    auto pyEnumTimeUnit =
        nb::enum_<QuantLib::TimeUnit>(sub_m, "TimeUnit", "! Units used to describe time periods\n/*! \\ingroup datetime */")
            .value("days", QuantLib::Days, "")
            .value("weeks", QuantLib::Weeks, "")
            .value("months", QuantLib::Months, "")
            .value("years", QuantLib::Years, "")
            .value("hours", QuantLib::Hours, "")
            .value("minutes", QuantLib::Minutes, "")
            .value("seconds", QuantLib::Seconds, "")
            .value("milliseconds", QuantLib::Milliseconds, "")
            .value("microseconds", QuantLib::Microseconds, "");
} // </namespace QuantLib>
////////////////////    </generated_from:timeunit.hpp>    ////////////////////

}
