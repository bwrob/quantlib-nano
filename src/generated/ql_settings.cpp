
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/settings.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_settings(nb::module_ &m) {
    nb::module_ &sub_m = m; 
////////////////////    <generated_from:settings.hpp>    ////////////////////
// #ifndef quantlib_settings_hpp
// 
// #endif
// 

{ // <namespace QuantLib>
    nb::module_ sub_m = m.def_submodule("quant_lib", "");
    auto sub_m_ClassSettings =
        nb::class_<QuantLib::Settings>
            (sub_m, "Settings", "! global repository for run-time library settings")
        .def("evaluation_date",
            [](QuantLib::Settings & self) { return self.evaluationDate(); })
        .def("evaluation_date",
            [](QuantLib::Settings & self) { return self.evaluationDate(); })
        .def("anchor_evaluation_date",
            &QuantLib::Settings::anchorEvaluationDate, "! Call this to prevent the evaluation date to change at\n            midnight (and, incidentally, to gain quite a bit of\n            performance.)  If no evaluation date was previously set,\n            it is equivalent to setting the evaluation date to\n            Date::todaysDate(); if an evaluation date other than\n            Date() was already set, it has no effect.\n")
        .def("reset_evaluation_date",
            &QuantLib::Settings::resetEvaluationDate, "! Call this to reset the evaluation date to\n            Date::todaysDate() and allow it to change at midnight.  It\n            is equivalent to setting the evaluation date to Date().\n            This comes at the price of losing some performance, since\n            the evaluation date is re-evaluated each time it is read.\n")
        .def("include_reference_date_events",
            [](QuantLib::Settings & self) { return self.includeReferenceDateEvents(); })
        .def("include_reference_date_events",
            [](QuantLib::Settings & self) { return self.includeReferenceDateEvents(); })
        .def("include_todays_cash_flows",
            [](QuantLib::Settings & self) { return self.includeTodaysCashFlows(); })
        .def("include_todays_cash_flows",
            [](QuantLib::Settings & self) { return self.includeTodaysCashFlows(); })
        .def("enforces_todays_historic_fixings",
            [](QuantLib::Settings & self) { return self.enforcesTodaysHistoricFixings(); })
        .def("enforces_todays_historic_fixings",
            [](QuantLib::Settings & self) { return self.enforcesTodaysHistoricFixings(); })
        ;


    auto sub_m_ClassSavedSettings =
        nb::class_<QuantLib::SavedSettings>
            (sub_m, "SavedSettings", "helper class to temporarily and safely change the settings")
        .def(nb::init<>())
        ;
} // </namespace QuantLib>
////////////////////    </generated_from:settings.hpp>    ////////////////////

}
