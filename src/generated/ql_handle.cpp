
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/handle.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_handle(nb::module_ &m) {
    nb::module_ &sub_m = m; 

    nb::class_<Handle<Quote>>(sub_m, "HandleQuote");
    nb::class_<RelinkableHandle<Quote>>(sub_m, "RelinkableHandleQuote");

}
