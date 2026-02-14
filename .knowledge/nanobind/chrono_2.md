s not fit in an int",
                     o, name, value);
        Py_DECREF(value);
        return false;
    }
    Py_DECREF(value);
    *dest = static_cast<int>(lval);
    return true;
}

NB_NOINLINE inline bool unpack_timedelta(PyObject *o, int *days,
                                         int *secs, int *usecs) {
    datetime_types.ensure_ready();
    if (PyType_IsSubtype(Py_TYPE(o),
                         (PyTypeObject *) datetime_types.timedelta.ptr())) {
        if (!set_from_int_attr(days, o, "days") ||
            !set_from_int_attr(secs, o, "seconds") ||
            !set_from_int_attr(usecs, o, "microseconds")) {
            raise_python_error();
        }
        return true;
    }
    return false;
}

NB_NOINLINE inline bool unpack_datetime(PyObject *o,
                                        int *year, int *month, int *day,
                                        int *hour, int *minute, int *second,
                                        int *usec) {
    datetime_types.ensure_ready();
    if (PyType_IsSubtype(Py_TYPE(o),
                         (PyTypeObject *) datetime_types.datetime.ptr())) {
        if (!set_from_int_attr(usec, o, "microsecond") ||
            !set_from_int_attr(second, o, "second") ||
            !set_from_int_attr(minute, o, "minute") ||
            !set_from_int_attr(hour, o, "hour") ||
            !set_from_int_attr(day, o, "day") ||
            !set_from_int_attr(month, o, "month") ||
            !set_from_int_attr(year, o, "year")) {
            raise_python_error();
        }
        return true;
    }
    if (PyType_IsSubtype(Py_TYPE(o),
                         (PyTypeObject *) datetime_types.date.ptr())) {
        *usec = *second = *minute = *hour = 0;
        if (!set_from_int_attr(day, o, "day") ||
            !set_from_int_attr(month, o, "month") ||
            !set_from_int_attr(year, o, "year")) {
            raise_python_error();
        }
        return true;
    }
    if (PyType_IsSubtype(Py_TYPE(o),
                         (PyTypeObject *) datetime_types.time.ptr())) {
        *day = 1;
        *month = 1;
        *year = 1970;
        if (!set_from_int_attr(usec, o, "microsecond") ||
            !set_from_int_attr(second, o, "second") ||
            !set_from_int_attr(minute, o, "minute") ||
            !set_from_int_attr(hour, o, "hour")) {
            raise_python_error();
        }
        return true;
    }
    return false;
}

inline PyObject* pack_timedelta(int days, int secs, int usecs) noexcept {
    try {
        datetime_types.ensure_ready();
        return datetime_types.timedelta(days, secs, usecs).release().ptr();
    } catch (python_error& e) {
        e.restore();
        return nullptr;
    }
}

inline PyObject* pack_datetime(int year, int month, int day,
                               int hour, int minute, int second,
                               int usec) noexcept {
    try {
        datetime_types.ensure_ready();
        return datetime_types.datetime(
                year, month, day, hour, minute, second, usec).release().ptr();
    } catch (python_error& e) {
        e.restore();
        return nullptr;
    }
}

#else // !defined(Py_LIMITED_API) && !defined(PYPY_VERSION)

NB_NOINLINE inline bool unpack_timedelta(PyObject *o, int *days,
                                         int *secs, int *usecs) {
    if (!PyDateTimeAPI) {
        PyDateTime_IMPORT;
        if (!PyDateTimeAPI)
            raise_python_error();
    }
    if (PyDelta_Check(o)) {
        *days = PyDateTime_DELTA_GET_DAYS(o);
        *secs = PyDateTime_DELTA_GET_SECONDS(o);
        *usecs = PyDateTime_DELTA_GET_MICROSECONDS(o);
        return true;
    }
    return false;
}

NB_NOINLINE inline bool unpack_datetime(PyObject *o,
                                        int *year, int *month, int *day,
                                        int *hour, int *minute, int *second,
                                        int *usec) {
    if (!PyDateTimeAPI) {
        PyDateTime_IMPORT;
