<< n_ << ", "
                   << v.n_ << ") cannot be added");
        std::transform(begin(),end(),v.begin(),begin(), std::plus<>());
        return *this;
    }


    inline const Array& Array::operator+=(Real x) {
        std::transform(begin(), end(), begin(), [=](Real y) -> Real { return y + x; });
        return *this;
    }

    inline const Array& Array::operator-=(const Array& v) {
        QL_REQUIRE(n_ == v.n_,
                   "arrays with different sizes (" << n_ << ", "
                   << v.n_ << ") cannot be subtracted");
        std::transform(begin(), end(), v.begin(), begin(), std::minus<>());
        return *this;
    }

    inline const Array& Array::operator-=(Real x) {
        std::transform(begin(),end(),begin(), [=](Real y) -> Real { return y - x; });
        return *this;
    }

    inline const Array& Array::operator*=(const Array& v) {
        QL_REQUIRE(n_ == v.n_,
                   "arrays with different sizes (" << n_ << ", "
                   << v.n_ << ") cannot be multiplied");
        std::transform(begin(), end(), v.begin(), begin(), std::multiplies<>());
        return *this;
    }

    inline const Array& Array::operator*=(Real x) {
        std::transform(begin(), end(), begin(), [=](Real y) -> Real { return y * x; });
        return *this;
    }

    inline const Array& Array::operator/=(const Array& v) {
        QL_REQUIRE(n_ == v.n_,
                   "arrays with different sizes (" << n_ << ", "
                   << v.n_ << ") cannot be divided");
        std::transform(begin(), end(), v.begin(), begin(), std::divides<>());
        return *this;
    }

    inline const Array& Array::operator/=(Real x) {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(x != 0.0, "division by zero");
        #endif
        std::transform(begin(), end(), begin(), [=](Real y) -> Real { return y / x; });
        return *this;
    }

    inline Real Array::operator[](Size i) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<n_,
                   "index (" << i << ") must be less than " << n_ <<
                   ": array access out of range");
        #endif
        return data_.get()[i];
    }

    inline Real Array::at(Size i) const {
        QL_REQUIRE(i<n_,
                   "index (" << i << ") must be less than " << n_ <<
                   ": array access out of range");
        return data_.get()[i];
    }

    inline Real Array::front() const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(n_>0, "null Array: array access out of range");
        #endif
        return data_.get()[0];
    }

    inline Real Array::back() const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(n_>0, "null Array: array access out of range");
        #endif
        return data_.get()[n_-1];
    }

    inline Real& Array::operator[](Size i) {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<n_,
                   "index (" << i << ") must be less than " << n_ <<
                   ": array access out of range");
        #endif
        return data_.get()[i];
    }

    inline Real& Array::at(Size i) {
        QL_REQUIRE(i<n_,
                   "index (" << i << ") must be less than " << n_ <<
                   ": array access out of range");
        return data_.get()[i];
    }

    inline Real& Array::front() {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(n_>0, "null Array: array access out of range");
        #endif
        return data_.get()[0];
    }

    inline Real& Array::back() {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(n_>0, "null Array: array access out of range");
        #endif
        return data_.get()[n_-1];
    }

    inline Size Array::size() const {
        return n_;
    }

    inline bool Array::empty() const {
        return n_ == 0;
    }

    inline Array::const_iterator Array::begin() const {
        return data_.get();
    }

    inline Array::iterator Array::be