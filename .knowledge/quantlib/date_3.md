nips */
        detail::iso_datetime_holder iso_datetime(const Date&);
#endif

    }


    // inline definitions

    inline Date Date::startOfMonth(const Date& d) {
        Month m = d.month();
        Year y = d.year();
        return Date(1, m, y);
    }

    inline bool Date::isStartOfMonth(const Date& d) {
       return (d.dayOfMonth() == 1);
    }

#ifndef QL_HIGH_RESOLUTION_DATE
    inline Weekday Date::weekday() const {
        Integer w = serialNumber_ % 7;
        return Weekday(w == 0 ? 7 : w);
    }

    inline Day Date::dayOfMonth() const {
        return dayOfYear() - monthOffset(month(),isLeap(year()));
    }

    inline Day Date::dayOfYear() const {
        return serialNumber_ - yearOffset(year());
    }

    inline Date::serial_type Date::serialNumber() const {
        return serialNumber_;
    }

    inline Date Date::operator+(Date::serial_type days) const {
        return Date(serialNumber_+days);
    }

    inline Date Date::operator-(Date::serial_type days) const {
        return Date(serialNumber_-days);
    }

    inline Date Date::operator+(const Period& p) const {
        return advance(*this,p.length(),p.units());
    }

    inline Date Date::operator-(const Period& p) const {
        return advance(*this,-p.length(),p.units());
    }

    inline Date Date::endOfMonth(const Date& d) {
        Month m = d.month();
        Year y = d.year();
        return {monthLength(m, isLeap(y)), m, y};
    }

    inline bool Date::isEndOfMonth(const Date& d) {
       return (d.dayOfMonth() == monthLength(d.month(), isLeap(d.year())));
    }

    inline Date::serial_type operator-(const Date& d1, const Date& d2) {
        return d1.serialNumber()-d2.serialNumber();
    }

    inline Time daysBetween(const Date& d1, const Date& d2) {
        return Time(d2-d1);
    }

    inline bool operator==(const Date& d1, const Date& d2) {
        return (d1.serialNumber() == d2.serialNumber());
    }

    inline bool operator!=(const Date& d1, const Date& d2) {
        return (d1.serialNumber() != d2.serialNumber());
    }

    inline bool operator<(const Date& d1, const Date& d2) {
        return (d1.serialNumber() < d2.serialNumber());
    }

    inline bool operator<=(const Date& d1, const Date& d2) {
        return (d1.serialNumber() <= d2.serialNumber());
    }

    inline bool operator>(const Date& d1, const Date& d2) {
        return (d1.serialNumber() > d2.serialNumber());
    }

    inline bool operator>=(const Date& d1, const Date& d2) {
        return (d1.serialNumber() >= d2.serialNumber());
    }
#endif
}

namespace std {
    template<>
    struct hash<QuantLib::Date> {
        std::size_t operator()(const QuantLib::Date& d) const {
            return QuantLib::hash_value(d);
        }
    };
}

#endif
