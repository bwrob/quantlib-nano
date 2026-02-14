
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_time_daycounters_actual365fixed(nb::module_ &m) {
    nb::module_ &sub_m = m; 
////////////////////    <generated_from:actual365fixed.hpp>    ////////////////////
// #ifndef quantlib_actual365fixed_day_counter_h
// 
// #endif
// 

{ // <namespace QuantLib>
    nb::module_ sub_m = m.def_submodule("quant_lib", "");
    auto sub_m_ClassActual365Fixed =
        nb::class_<QuantLib::Actual365Fixed>
            (sub_m, "Actual365Fixed", "! \"Actual/365 (Fixed)\" day count convention, also know as\n        \"Act/365 (Fixed)\", \"A/365 (Fixed)\", or \"A/365F\".\n\n        \\warning According to ISDA, \"Actual/365\" (without \"Fixed\") is\n                 an alias for \"Actual/Actual (ISDA)\" (see\n                 ActualActual.)  If Actual/365 is not explicitly\n                 specified as fixed in an instrument specification,\n                 you might want to double-check its meaning.\n\n        \\ingroup daycounters\n");

    { // inner classes & enums of Actual365Fixed
        auto pyEnumConvention =
            nb::enum_<QuantLib::Actual365Fixed::Convention>(sub_m_ClassActual365Fixed, "Convention", "")
                .value("standard", QuantLib::Actual365Fixed::Standard, "")
                .value("canadian", QuantLib::Actual365Fixed::Canadian, "")
                .value("no_leap", QuantLib::Actual365Fixed::NoLeap, "");
    } // end of inner classes & enums of Actual365Fixed

    sub_m_ClassActual365Fixed
        .def(nb::init<QuantLib::Actual365Fixed::Convention>(),
            nb::arg("c") = QuantLib::Actual365Fixed::Standard)
        ;
} // </namespace QuantLib>
////////////////////    </generated_from:actual365fixed.hpp>    ////////////////////

}
