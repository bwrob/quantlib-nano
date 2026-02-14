nst Quantity&);

    /*! \relates Quantity */
    bool close(const Quantity&, const Quantity&, Size n = 42);
    /*! \relates Quantity */
    bool close_enough(const Quantity&, const Quantity&, Size n = 42);


    // inline definitions

    inline Quantity::Quantity(CommodityType commodityType, UnitOfMeasure unitOfMeasure, Real amount)
    : commodityType_(std::move(commodityType)), unitOfMeasure_(std::move(unitOfMeasure)),
      amount_(amount) {}

    inline const CommodityType& Quantity::commodityType() const {
        return commodityType_;
    }

    inline const UnitOfMeasure& Quantity::unitOfMeasure() const {
        return unitOfMeasure_;
    }

    inline Real Quantity::amount() const {
        return amount_;
    }

    inline Quantity Quantity::rounded() const {
        return Quantity(commodityType_,
                        unitOfMeasure_,
                        unitOfMeasure_.rounding()(amount_));
    }

    inline Quantity Quantity::operator+() const {
        return *this;
    }

    inline Quantity Quantity::operator-() const {
        return Quantity(commodityType_, unitOfMeasure_, -amount_);
    }

    inline Quantity& Quantity::operator*=(Real x) {
        amount_ *= x;
        return *this;
    }

    inline Quantity& Quantity::operator/=(Real x) {
        amount_ /= x;
        return *this;
    }


    inline Quantity operator+(const Quantity& m1, const Quantity& m2) {
        Quantity tmp = m1;
        tmp += m2;
        return tmp;
    }

    inline Quantity operator-(const Quantity& m1, const Quantity& m2) {
        Quantity tmp = m1;
        tmp -= m2;
        return tmp;
    }

    inline Quantity operator*(const Quantity& m, Real x) {
        Quantity tmp = m;
        tmp *= x;
        return tmp;
    }

    inline Quantity operator*(Real x, const Quantity& m) {
        return m*x;
    }

    inline Quantity operator/(const Quantity& m, Real x) {
        Quantity tmp = m;
        tmp /= x;
        return tmp;
    }

    inline bool operator!=(const Quantity& m1, const Quantity& m2) {
        return !(m1 == m2);
    }

    inline bool operator>(const Quantity& m1, const Quantity& m2) {
        return m2 < m1;
    }

    inline bool operator>=(const Quantity& m1, const Quantity& m2) {
        return m2 <= m1;
    }

}


#endif