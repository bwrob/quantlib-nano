
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <ql/time/date.hpp>
#include <ql/handle.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/compounding.hpp>

namespace nb = nanobind;
using namespace QuantLib;

void gen_ql_time_date(nb::module_ &m) {
    nb::module_ &sub_m = m; 
////////////////////    <generated_from:date.hpp>    ////////////////////
// #ifndef quantlib_date_hpp
// 
// #endif
// 

{ // <namespace QuantLib>
    nb::module_ sub_m = m.def_submodule("quant_lib", "");
    auto pyEnumMonth =
        nb::enum_<QuantLib::Month>(sub_m, "Month", "! Month names\n/*! \\ingroup datetime */")
            .value("january", QuantLib::January, "")
            .value("february", QuantLib::February, "")
            .value("march", QuantLib::March, "")
            .value("april", QuantLib::April, "")
            .value("may", QuantLib::May, "")
            .value("june", QuantLib::June, "")
            .value("july", QuantLib::July, "")
            .value("august", QuantLib::August, "")
            .value("september", QuantLib::September, "")
            .value("october", QuantLib::October, "")
            .value("november", QuantLib::November, "")
            .value("december", QuantLib::December, "")
            .value("jan", QuantLib::Jan, "")
            .value("feb", QuantLib::Feb, "")
            .value("mar", QuantLib::Mar, "")
            .value("apr", QuantLib::Apr, "")
            .value("jun", QuantLib::Jun, "")
            .value("jul", QuantLib::Jul, "")
            .value("aug", QuantLib::Aug, "")
            .value("sep", QuantLib::Sep, "")
            .value("oct", QuantLib::Oct, "")
            .value("nov", QuantLib::Nov, "")
            .value("dec", QuantLib::Dec, "");


    auto sub_m_ClassDate =
        nb::class_<QuantLib::Date>
            (sub_m, "Date", "")
        .def(nb::init<>(),
            "! \name constructors\n@{\n! Default constructor returning a null date.")
        .def(nb::init<Date::serial_type>(),
            nb::arg("serial_number"),
            "! Constructor taking a serial number as given by Applix or Excel.")
        .def(nb::init<Day, QuantLib::Month, Year>(),
            nb::arg("d"), nb::arg("m"), nb::arg("y"),
            "! More traditional constructor.")
        .def("weekday",
            &QuantLib::Date::weekday)
        .def("day_of_month",
            &QuantLib::Date::dayOfMonth)
        .def("day_of_year",
            &QuantLib::Date::dayOfYear)
        .def("month",
            &QuantLib::Date::month)
        .def("year",
            &QuantLib::Date::year)
        .def("serial_number",
            &QuantLib::Date::serialNumber)
        .def("__iadd__",
            nb::overload_cast<Date::serial_type>(&QuantLib::Date::operator+=),
            nb::arg("days"),
            "! \name date algebra\n@{\n! increments date by the given number of days")
        .def("__iadd__",
            nb::overload_cast<const Period &>(&QuantLib::Date::operator+=),
            nb::arg("param_0"),
            "! increments date by the given period")
        .def("__isub__",
            nb::overload_cast<Date::serial_type>(&QuantLib::Date::operator-=),
            nb::arg("days"),
            "! decrement date by the given number of days")
        .def("__isub__",
            nb::overload_cast<const Period &>(&QuantLib::Date::operator-=),
            nb::arg("param_0"),
            "! decrements date by the given period")
        .def("__add__",
            nb::overload_cast<Date::serial_type>(&QuantLib::Date::operator+, nb::const_),
            nb::arg("days"),
            "! returns a new date incremented by the given number of days")
        .def("__add__",
            nb::overload_cast<const Period &>(&QuantLib::Date::operator+, nb::const_),
            nb::arg("param_0"),
            "! returns a new date incremented by the given period")
        .def("__sub__",
            nb::overload_cast<Date::serial_type>(&QuantLib::Date::operator-, nb::const_),
            nb::arg("days"),
            "! returns a new date decremented by the given number of days")
        .def("__sub__",
            nb::overload_cast<const Period &>(&QuantLib::Date::operator-, nb::const_),
            nb::arg("param_0"),
            "! returns a new date decremented by the given period")
        .def_static("todays_date",
            &QuantLib::Date::todaysDate, "! \name static methods\n@{\n! today's date.")
        .def_static("min_date",
            &QuantLib::Date::minDate, "! earliest allowed date")
        .def_static("max_date",
            &QuantLib::Date::maxDate, "! latest allowed date")
        .def_static("is_leap",
            &QuantLib::Date::isLeap,
            nb::arg("y"),
            "! whether the given year is a leap one")
        .def_static("start_of_month",
            &QuantLib::Date::startOfMonth,
            nb::arg("d"),
            "! first day of the month to which the given date belongs")
        .def_static("is_start_of_month",
            &QuantLib::Date::isStartOfMonth,
            nb::arg("d"),
            "! whether a date is the first day of its month")
        .def_static("end_of_month",
            &QuantLib::Date::endOfMonth,
            nb::arg("d"),
            "! last day of the month to which the given date belongs")
        .def_static("is_end_of_month",
            &QuantLib::Date::isEndOfMonth,
            nb::arg("d"),
            "! whether a date is the last day of its month")
        .def_static("next_weekday",
            &QuantLib::Date::nextWeekday,
            nb::arg("d"), nb::arg("w"),
            "! E.g., the Friday following Tuesday, January 15th, 2002\n            was January 18th, 2002.\n\n            see http://www.cpearson.com/excel/DateTimeWS.htm\n")
        .def_static("nth_weekday",
            &QuantLib::Date::nthWeekday,
            nb::arg("n"), nb::arg("w"), nb::arg("m"), nb::arg("y"),
            "! E.g., the 4th Thursday of March, 1998 was March 26th,\n            1998.\n\n            see http://www.cpearson.com/excel/DateTimeWS.htm\n")
        ;


    sub_m.def("days_between",
        QuantLib::daysBetween,
        nb::arg("param_0"), nb::arg("param_1"),
        "! \\relates Date\n        \\brief Difference in days (including fraction of days) between dates\n");

    sub_m.def("hash_value",
        QuantLib::hash_value,
        nb::arg("d"),
        "!\n      Compute a hash value of @p d.\n\n      This method makes Date hashable via <tt>boost::hash</tt>.\n\n      Example:\n\n      \\code{.cpp}\n      #include <unordered_set>\n\n      std::unordered_set<Date> set;\n      Date d = Date(1, Jan, 2020);\n\n      set.insert(d);\n      assert(set.count(d)); // 'd' was added to 'set'\n      \\endcode\n\n      \\param [in] d Date to hash\n      \\return A hash value of @p d\n      \\relates Date\n");
    { // <namespace io>
        nb::module_ sub_m_Nsio = sub_m.def_submodule("io", "");
        sub_m_Nsio.def("short_date",
            QuantLib::io::short_date,
            nb::arg("param_0"),
            "! output dates in short format (mm/dd/yyyy)\n/*! \\ingroup manips */");

        sub_m_Nsio.def("long_date",
            QuantLib::io::long_date,
            nb::arg("param_0"),
            "! output dates in long format (Month ddth, yyyy)\n/*! \\ingroup manips */");

        sub_m_Nsio.def("iso_date",
            QuantLib::io::iso_date,
            nb::arg("param_0"),
            "! output dates in ISO format (yyyy-mm-dd)\n/*! \\ingroup manips */");

        sub_m_Nsio.def("formatted_date",
            QuantLib::io::formatted_date,
            nb::arg("param_0"), nb::arg("fmt"),
            "! output dates in user defined format using boost date functionality\n/*! \\ingroup manips */");
    } // </namespace io>

} // </namespace QuantLib>

{ // <namespace std>
    nb::module_ pyNsstd = m.def_submodule("std", "");
    
} // </namespace std>
////////////////////    </generated_from:date.hpp>    ////////////////////

}
