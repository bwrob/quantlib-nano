ecimal);
    /*! \relates Money */
    Money operator*(Decimal, const Money&);
    /*! \relates Money */
    Money operator/(const Money&, Decimal);
    /*! \relates Money */
    Decimal operator/(const Money&, const Money&);

    /*! \relates Money */
    bool operator==(const Money&, const Money&);
    /*! \relates Money */
    bool operator!=(const Money&, const Money&);
    /*! \relates Money */
    bool operator<(const Money&, const Money&);
    /*! \relates Money */
    bool operator<=(const Money&, const Money&);
    /*! \relates Money */
    bool operator>(const Money&, const Money&);
    /*! \relates Money */
    bool operator>=(const Money&, const Money&);

    /*! \relates Money */
    bool close(const Money&, const Money&, Size n = 42);
    /*! \relates Money */
    bool close_enough(const Money&, const Money&, Size n = 42);

    // syntactic sugar

    /*! \relates Money */
    Money operator*(Decimal, const Currency&);
    /*! \relates Money */
    Money operator*(const Currency&, Decimal);

    // formatting

    /*! \relates Money */
    std::ostream& operator<<(std::ostream&, const Money&);


    // inline definitions

    inline Money::Money(Currency currency, Decimal value)
    : value_(value), currency_(std::move(currency)) {}

    inline Money::Money(Decimal value, Currency currency)
    : value_(value), currency_(std::move(currency)) {}

    inline const Currency& Money::currency() const {
        return currency_;
    }

    inline Decimal Money::value() const {
        return value_;
    }

    inline Money Money::rounded() const {
        return Money(currency_.rounding()(value_), currency_);
    }

    inline Money Money::operator+() const {
        return *this;
    }

    inline Money Money::operator-() const {
        return Money(-value_, currency_);
    }

    inline Money& Money::operator*=(Decimal x) {
        value_ *= x;
        return *this;
    }

    inline Money& Money::operator/=(Decimal x) {
        value_ /= x;
        return *this;
    }


    inline Money operator+(const Money& m1, const Money& m2) {
        Money tmp = m1;
        tmp += m2;
        return tmp;
    }

    inline Money operator-(const Money& m1, const Money& m2) {
        Money tmp = m1;
        tmp -= m2;
        return tmp;
    }

    inline Money operator*(const Money& m, Decimal x) {
        Money tmp = m;
        tmp *= x;
        return tmp;
    }

    inline Money operator*(Decimal x, const Money& m) {
        return m*x;
    }

    inline Money operator/(const Money& m, Decimal x) {
        Money tmp = m;
        tmp /= x;
        return tmp;
    }

    inline bool operator!=(const Money& m1, const Money& m2) {
        return !(m1 == m2);
    }

    inline bool operator>(const Money& m1, const Money& m2) {
        return m2 < m1;
    }

    inline bool operator>=(const Money& m1, const Money& m2) {
        return m2 <= m1;
    }

    inline Money operator*(Decimal value, const Currency& c) {
        return Money(value,c);
    }

    inline Money operator*(const Currency& c, Decimal value) {
        return Money(value,c);
    }

}


#endif
