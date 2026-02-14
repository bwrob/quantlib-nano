at (e.g. "2 weeks")
        /*! \ingroup manips */
        detail::long_period_holder long_period(const Period&);

        //! output periods in short format (e.g. "2w")
        /*! \ingroup manips */
        detail::short_period_holder short_period(const Period&);

    }

    // inline definitions

    inline Period Period::normalized() const {
        Period p = *this;
        p.normalize();
        return p;
    }

    template <typename T>
    inline Period operator*(T n, TimeUnit units) {
        return {Integer(n), units};
    }

    template <typename T>
    inline Period operator*(TimeUnit units, T n) {
        return {Integer(n), units};
    }

    inline Period operator-(const Period& p) { return {-p.length(), p.units()}; }

    inline Period operator*(Integer n, const Period& p) { return {n * p.length(), p.units()}; }

    inline Period operator*(const Period& p, Integer n) { return {n * p.length(), p.units()}; }

    inline bool operator==(const Period& p1, const Period& p2) {
        return !(p1 < p2 || p2 < p1);
    }

    inline bool operator!=(const Period& p1, const Period& p2) {
        return !(p1 == p2);
    }

    inline bool operator>(const Period& p1, const Period& p2) {
        return p2 < p1;
    }

    inline bool operator<=(const Period& p1, const Period& p2) {
        return !(p1 > p2);
    }

    inline bool operator>=(const Period& p1, const Period& p2) {
        return !(p1 < p2);
    }

}

#endif
