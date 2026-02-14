 definitions

    inline bool DayCounter::empty() const {
        return !impl_;
    }

    inline std::string DayCounter::name() const {
        QL_REQUIRE(impl_, "no day counter implementation provided");
        return impl_->name();
    }

    inline Date::serial_type DayCounter::dayCount(const Date& d1,
                                                  const Date& d2) const {
        QL_REQUIRE(impl_, "no day counter implementation provided");
        return impl_->dayCount(d1,d2);
    }

    inline Time DayCounter::yearFraction(const Date& d1, const Date& d2,
        const Date& refPeriodStart, const Date& refPeriodEnd) const {
            QL_REQUIRE(impl_, "no day counter implementation provided");
            return impl_->yearFraction(d1,d2,refPeriodStart,refPeriodEnd);
    }


    inline bool operator==(const DayCounter& d1, const DayCounter& d2) {
        return (d1.empty() && d2.empty())
            || (!d1.empty() && !d2.empty() && d1.name() == d2.name());
    }

    inline bool operator!=(const DayCounter& d1, const DayCounter& d2) {
        return !(d1 == d2);
    }

    inline std::ostream& operator<<(std::ostream& out, const DayCounter &d) {
        return out << d.name();
    }

}

#endif