
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/time/calendar.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_time_calendar(nb::module_ &m) {
    nb::module_ &sub_m = m; 
    nb::class_<QuantLib::Calendar>
            (sub_m, "Calendar", "! This class provides methods for determining whether a date is a\n        business day or a holiday for a given market, and for\n        incrementing/decrementing a date of a given number of business days.\n\n        The Bridge pattern is used to provide the base behavior of the\n        calendar, namely, to determine whether a date is a business day.\n\n        A calendar should be defined for specific exchange holiday schedule\n        or for general country holiday schedule. Legacy city holiday schedule\n        calendars will be moved to the exchange/country convention.\n\n        \\ingroup datetime\n\n        \test the methods for adding and removing holidays are tested\n              by inspecting the calendar before and after their\n              invocation.\n");
}
