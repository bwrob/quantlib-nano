ostream& operator<<(std::ostream&, const Calendar&);


    // inline definitions

    inline bool Calendar::empty() const {
        return !impl_;
    }

    inline std::string Calendar::name() const {
        QL_REQUIRE(impl_, "no calendar implementation provided");
        return impl_->name();
    }

    inline const std::set<Date>& Calendar::addedHolidays() const {
        QL_REQUIRE(impl_, "no calendar implementation provided");

        return impl_->addedHolidays;
    }

    inline const std::set<Date>& Calendar::removedHolidays() const {
        QL_REQUIRE(impl_, "no calendar implementation provided");

        return impl_->removedHolidays;
    }

    inline bool Calendar::isBusinessDay(const Date& d) const {
        QL_REQUIRE(impl_, "no calendar implementation provided");

#ifdef QL_HIGH_RESOLUTION_DATE
        const Date _d(d.dayOfMonth(), d.month(), d.year());
#else
        const Date& _d = d;
#endif

        if (!impl_->addedHolidays.empty() &&
            impl_->addedHolidays.find(_d) != impl_->addedHolidays.end())
            return false;

        if (!impl_->removedHolidays.empty() &&
            impl_->removedHolidays.find(_d) != impl_->removedHolidays.end())
            return true;

        return impl_->isBusinessDay(_d);
    }

    inline bool Calendar::isStartOfMonth(const Date& d) const {
        return d <= startOfMonth(d);
    }

    inline Date Calendar::startOfMonth(const Date& d) const {
        return adjust(Date::startOfMonth(d), Following);
    }

    inline bool Calendar::isEndOfMonth(const Date& d) const {
        return d >= endOfMonth(d);
    }

    inline Date Calendar::endOfMonth(const Date& d) const {
        return adjust(Date::endOfMonth(d), Preceding);
    }

    inline bool Calendar::isHoliday(const Date& d) const {
        return !isBusinessDay(d);
    }

    inline bool Calendar::isWeekend(Weekday w) const {
        QL_REQUIRE(impl_, "no calendar implementation provided");
        return impl_->isWeekend(w);
    }

    inline bool operator==(const Calendar& c1, const Calendar& c2) {
        return (c1.empty() && c2.empty())
            || (!c1.empty() && !c2.empty() && c1.name() == c2.name());
    }

    inline bool operator!=(const Calendar& c1, const Calendar& c2) {
        return !(c1 == c2);
    }

    inline std::ostream& operator<<(std::ostream& out, const Calendar &c) {
        return out << c.name();
    }

}

#endif