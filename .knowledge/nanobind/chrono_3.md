
        if (!PyDateTimeAPI)
            raise_python_error();
    }
    if (PyDateTime_Check(o)) {
        *usec = PyDateTime_DATE_GET_MICROSECOND(o);
        *second = PyDateTime_DATE_GET_SECOND(o);
        *minute = PyDateTime_DATE_GET_MINUTE(o);
        *hour = PyDateTime_DATE_GET_HOUR(o);
        *day = PyDateTime_GET_DAY(o);
        *month = PyDateTime_GET_MONTH(o);
        *year = PyDateTime_GET_YEAR(o);
        return true;
    }
    if (PyDate_Check(o)) {
        *usec = 0;
        *second = 0;
        *minute = 0;
        *hour = 0;
        *day = PyDateTime_GET_DAY(o);
        *month = PyDateTime_GET_MONTH(o);
        *year = PyDateTime_GET_YEAR(o);
        return true;
    }
    if (PyTime_Check(o)) {
        *usec = PyDateTime_TIME_GET_MICROSECOND(o);
        *second = PyDateTime_TIME_GET_SECOND(o);
        *minute = PyDateTime_TIME_GET_MINUTE(o);
        *hour = PyDateTime_TIME_GET_HOUR(o);
        *day = 1;
        *month = 1;
        *year = 1970;
        return true;
    }
    return false;
}

inline PyObject* pack_timedelta(int days, int secs, int usecs) noexcept {
    if (!PyDateTimeAPI) {
        PyDateTime_IMPORT;
        if (!PyDateTimeAPI)
            return nullptr;
    }
    return PyDelta_FromDSU(days, secs, usecs);
}

inline PyObject* pack_datetime(int year, int month, int day,
                               int hour, int minute, int second,
                               int usec) noexcept {
    if (!PyDateTimeAPI) {
        PyDateTime_IMPORT;
        if (!PyDateTimeAPI)
            return nullptr;
    }
    return PyDateTime_FromDateAndTime(year, month, day,
                                      hour, minute, second, usec);
}

#endif // !defined(Py_LIMITED_API) && !defined(PYPY_VERSION)
//
#if defined(__GNUC__)
