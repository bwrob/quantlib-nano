import os
import toml
import re
from litgen import LitgenOptions, generate_code_for_file

def load_config(path='benchmark_scope.toml'):
    with open(path, 'r') as f:
        return toml.load(f)

def generate_bindings():
    config_path = 'benchmark_scope.toml'
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    config = load_config(config_path)
    project_name = config['project']['name']
    
    output_dir = os.path.join(os.getcwd(), 'src/generated')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate ONE file for everything to avoid symbol visibility issues
    bindings_cpp_path = os.path.join(output_dir, "bindings.cpp")
    
    code = """
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/time/date.hpp>
#include <ql/time/calendar.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/calendars/target.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <ql/settings.hpp>
#include <ql/termstructures/yield/flatforward.hpp>
#include <ql/patterns/observable.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/quote.hpp>
#include <ql/handle.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_bindings(nb::module_ &m) {
    // 1. Enums
    nb::enum_<Month>(m, "Month")
        .value("January", January).value("February", February).value("March", March)
        .value("April", April).value("May", May).value("June", June)
        .value("July", July).value("August", August).value("September", September)
        .value("October", October).value("November", November).value("December", December);

    nb::enum_<TimeUnit>(m, "TimeUnit")
        .value("Days", Days).value("Weeks", Weeks).value("Months", Months).value("Years", Years);

    nb::enum_<BusinessDayConvention>(m, "BusinessDayConvention")
        .value("Following", Following).value("ModifiedFollowing", ModifiedFollowing)
        .value("Preceding", Preceding).value("ModifiedPreceding", ModifiedPreceding)
        .value("Unadjusted", Unadjusted).value("Nearest", Nearest);

    // 2. Base Classes
    nb::class_<Date>(m, "Date")
        .def(nb::init<>())
        .def(nb::init<int, Month, int>())
        .def("serialNumber", &Date::serialNumber);

    nb::class_<Calendar>(m, "Calendar")
        .def("advance", [](const Calendar& self, const Date& d, int n, TimeUnit unit, BusinessDayConvention c) {
            return self.advance(d, n, unit, c);
        }, nb::arg("d"), nb::arg("n"), nb::arg("unit"), nb::arg("c") = Following);

    nb::class_<DayCounter>(m, "DayCounter");
    nb::class_<Observable>(m, "Observable");
    nb::class_<TermStructure>(m, "TermStructure");
    nb::class_<YieldTermStructure, TermStructure>(m, "YieldTermStructure")
        .def("discount", [](const YieldTermStructure& self, const Date& d, bool extrapolate) {
            return self.discount(d, extrapolate);
        }, nb::arg("d"), nb::arg("extrapolate") = false);

    // 3. Concrete Classes
    nb::class_<TARGET, Calendar>(m, "TARGET").def(nb::init<>());
    nb::class_<Actual365Fixed, DayCounter>(m, "Actual365Fixed").def(nb::init<>());
    
    nb::class_<FlatForward, YieldTermStructure>(m, "FlatForward")
        .def(nb::init<const Date&, double, const DayCounter&>());

    nb::class_<Settings>(m, "Settings")
        .def_static("instance", &Settings::instance, nb::rv_policy::reference)
        .def_prop_rw("evaluationDate", 
            [](Settings& s) { return s.evaluationDate(); },
            [](Settings& s, const Date& d) { s.evaluationDate() = d; });
}
"""
    with open(bindings_cpp_path, 'w') as f:
        f.write(code)

    # Simplified registration header
    with open(os.path.join(output_dir, "registration.h"), 'w') as f:
        f.write("#include <nanobind/nanobind.h>\nvoid gen_bindings(nanobind::module_ &m);\n")
            
    print(f"Binding generation complete.")

if __name__ == "__main__":
    generate_bindings()
