
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_termstructures_yieldtermstructure(nb::module_ &m) {
    nb::module_ &sub_m = m; 
    nb::class_<QuantLib::YieldTermStructure>
            (sub_m, "YieldTermStructure", "! This abstract class defines the interface of concrete\n        interest rate structures which will be derived from this one.\n\n        \\ingroup yieldtermstructures\n\n        \test observability against evaluation date changes is checked.\n");
}
