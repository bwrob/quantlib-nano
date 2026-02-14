
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/termstructures/yield/flatforward.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_termstructures_yield_flatforward(nb::module_ &m) {
    nb::module_ &sub_m = m; 
    nb::class_<QuantLib::FlatForward, YieldTermStructure>
            (sub_m, "FlatForward", "! Flat interest-rate curve\n/*! \\ingroup yieldtermstructures */");
}
