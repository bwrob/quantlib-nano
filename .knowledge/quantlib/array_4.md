gin() {
        return data_.get();
    }

    inline Array::const_iterator Array::end() const {
        return data_.get()+n_;
    }

    inline Array::iterator Array::end() {
        return data_.get()+n_;
    }

    inline Array::const_reverse_iterator Array::rbegin() const {
        return const_reverse_iterator(end());
    }

    inline Array::reverse_iterator Array::rbegin() {
        return reverse_iterator(end());
    }

    inline Array::const_reverse_iterator Array::rend() const {
        return const_reverse_iterator(begin());
    }

    inline Array::reverse_iterator Array::rend() {
        return reverse_iterator(begin());
    }

    inline void Array::resize(Size n) {
        if (n > n_) {
            Array swp(n);
            std::copy(begin(), end(), swp.begin());
            swap(swp);
        }
        else if (n < n_) {
            n_ = n;
        }
    }

    inline void Array::swap(Array& from) noexcept {
        data_.swap(from.data_);
        std::swap(n_, from.n_);
    }

    // dot product and norm

    inline Real DotProduct(const Array& v1, const Array& v2) {
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be multiplied");
        return std::inner_product(v1.begin(),v1.end(),v2.begin(),Real(0.0));
    }

    inline Real Norm2(const Array& v) {
        return std::sqrt(DotProduct(v, v));
    }

    // overloaded operators

    // unary

    inline Array operator+(const Array& v) {
        Array result = v;
        return result;
    }

    inline Array operator+(Array&& v) {
        return std::move(v);
    }

    inline Array operator-(const Array& v) {
        Array result(v.size());
        std::transform(v.begin(), v.end(), result.begin(), std::negate<>());
        return result;
    }

    inline Array operator-(Array&& v) {
        Array result = std::move(v);
        std::transform(result.begin(), result.end(), result.begin(), std::negate<>());
        return result;
    }

    // binary operators

    inline Array operator+(const Array& v1, const Array& v2) {
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be added");
        Array result(v1.size());
        std::transform(v1.begin(),v1.end(),v2.begin(),result.begin(), std::plus<>());
        return result;
    }

    inline Array operator+(const Array& v1, Array&& v2) {
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be added");
        Array result = std::move(v2);
        std::transform(v1.begin(), v1.end(), result.begin(), result.begin(), std::plus<>());
        return result;
    }

    inline Array operator+(Array&& v1, const Array& v2) {
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be added");
        Array result = std::move(v1);
        std::transform(result.begin(), result.end(), v2.begin(), result.begin(), std::plus<>());
        return result;
    }

    inline Array operator+(Array&& v1, Array&& v2) { // NOLINT(cppcoreguidelines-rvalue-reference-param-not-moved)
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be added");
        Array result = std::move(v2);
        std::transform(v1.begin(), v1.end(), result.begin(), result.begin(), std::plus<>());
        return result;
    }

    inline Array operator+(const Array& v1, Real a) {
        Array result(v1.size());
        std::transform(v1.begin(), v1.end(), result.begin(), [=](Real y) -> Real { return y + a; });
        return result;
    }

    inline Array operator+(Array&& v1, Real a) {
        Array result = std::move(v1);