 v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be multiplied");
        Array result = std::move(v1);
        std::transform(result.begin(), result.end(), v2.begin(), result.begin(), std::multiplies<>());
        return result;
    }

    inline Array operator*(Array&& v1, Array&& v2) { // NOLINT(cppcoreguidelines-rvalue-reference-param-not-moved)
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be multiplied");
        Array result = std::move(v2);
        std::transform(v1.begin(), v1.end(), result.begin(), result.begin(), std::multiplies<>());
        return result;
    }

    inline Array operator*(const Array& v1, Real a) {
        Array result(v1.size());
        std::transform(v1.begin(),v1.end(),result.begin(), [=](Real y) -> Real { return y * a; });
        return result;
    }

    inline Array operator*(Array&& v1, Real a) {
        Array result = std::move(v1);
        std::transform(result.begin(), result.end(), result.begin(), [=](Real y) -> Real { return y * a; });
        return result;
    }

    inline Array operator*(Real a, const Array& v2) {
        Array result(v2.size());
        std::transform(v2.begin(),v2.end(),result.begin(), [=](Real y) -> Real { return a * y; });
        return result;
    }

    inline Array operator*(Real a, Array&& v2) {
        Array result = std::move(v2);
        std::transform(result.begin(), result.end(), result.begin(), [=](Real y) -> Real { return a * y; });
        return result;
    }

    inline Array operator/(const Array& v1, const Array& v2) {
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be divided");
        Array result(v1.size());
        std::transform(v1.begin(), v1.end(), v2.begin(), result.begin(), std::divides<>());
        return result;
    }

    inline Array operator/(const Array& v1, Array&& v2) {
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be divided");
        Array result = std::move(v2);
        std::transform(v1.begin(), v1.end(), result.begin(), result.begin(), std::divides<>());
        return result;
    }

    inline Array operator/(Array&& v1, const Array& v2) {
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be divided");
        Array result = std::move(v1);
        std::transform(result.begin(), result.end(), v2.begin(), result.begin(), std::divides<>());
        return result;
    }

    inline Array operator/(Array&& v1, Array&& v2) { // NOLINT(cppcoreguidelines-rvalue-reference-param-not-moved)
        QL_REQUIRE(v1.size() == v2.size(),
                   "arrays with different sizes (" << v1.size() << ", "
                   << v2.size() << ") cannot be divided");
        Array result = std::move(v2);
        std::transform(v1.begin(), v1.end(), result.begin(), result.begin(), std::divides<>());
        return result;
    }

    inline Array operator/(const Array& v1, Real a) {
        Array result(v1.size());
        std::transform(v1.begin(),v1.end(),result.begin(), [=](Real y) -> Real { return y / a; });
        return result;
    }

    inline Array operator/(Array&& v1, Real a) {
        Array result = std::move(v1);
        std::transform(result.begin(), result.end(), result.begin(), [=](Real y) -> Real { return y / a; });
        return result;
    }

    inline Array operator/(Real a, const Array& v2) {
        Array result(v2.size());
        std::transform(v2.begin(),v2.end(),result.begin(), [=](Real y) -> Real { return a / y; });
        return result;
    }

    inline Array operator/(Real a, Array&
