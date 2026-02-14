orm(m1.begin(), m1.end(), m1.begin(), std::negate<>());
        return std::move(m1);
    }

    inline Matrix operator-(const Matrix& m1, const Matrix& m2) {
        QL_REQUIRE(m1.rows() == m2.rows() &&
                   m1.columns() == m2.columns(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "subtracted");
        Matrix temp(m1.rows(),m1.columns());
        std::transform(m1.begin(), m1.end(), m2.begin(), temp.begin(), std::minus<>());
        return temp;
    }

    inline Matrix operator-(const Matrix& m1, Matrix&& m2) {
        QL_REQUIRE(m1.rows() == m2.rows() &&
                   m1.columns() == m2.columns(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "subtracted");
        std::transform(m1.begin(), m1.end(), m2.begin(), m2.begin(), std::minus<>());
        return std::move(m2);
    }

    inline Matrix operator-(Matrix&& m1, const Matrix& m2) {
        QL_REQUIRE(m1.rows() == m2.rows() &&
                   m1.columns() == m2.columns(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "subtracted");
        std::transform(m1.begin(), m1.end(), m2.begin(), m1.begin(), std::minus<>());
        return std::move(m1);
    }

    inline Matrix operator-(Matrix&& m1, Matrix&& m2) { // NOLINT(cppcoreguidelines-rvalue-reference-param-not-moved)
        QL_REQUIRE(m1.rows() == m2.rows() &&
                   m1.columns() == m2.columns(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "subtracted");
        std::transform(m1.begin(), m1.end(), m2.begin(), m1.begin(), std::minus<>());
        return std::move(m1);
    }

    inline Matrix operator*(const Matrix& m, Real x) {
        Matrix temp(m.rows(),m.columns());
        std::transform(m.begin(), m.end(), temp.begin(), [=](Real y) -> Real { return y * x; });
        return temp;
    }

    inline Matrix operator*(Matrix&& m, Real x) {
        std::transform(m.begin(), m.end(), m.begin(), [=](Real y) -> Real { return y * x; });
        return std::move(m);
    }

    inline Matrix operator*(Real x, const Matrix& m) {
        Matrix temp(m.rows(),m.columns());
        std::transform(m.begin(), m.end(), temp.begin(), [=](Real y) -> Real { return x * y; });
        return temp;
    }

    inline Matrix operator*(Real x, Matrix&& m) {
        std::transform(m.begin(), m.end(), m.begin(), [=](Real y) -> Real { return x * y; });
        return std::move(m);
    }

    inline Matrix operator/(const Matrix& m, Real x) {
        Matrix temp(m.rows(),m.columns());
        std::transform(m.begin(), m.end(), temp.begin(), [=](Real y) -> Real { return y / x; });
        return temp;
    }

    inline Matrix operator/(Matrix&& m, Real x) {
        std::transform(m.begin(), m.end(), m.begin(), [=](Real y) -> Real { return y / x; });
        return std::move(m);
    }

    inline Array operator*(const Array& v, const Matrix& m) {
        QL_REQUIRE(v.size() == m.rows(),
                   "vectors and matrices with different sizes ("
                   << v.size() << ", " << m.rows() << "x" << m.columns() <<
                   ") cannot be multiplied");
        Array result(m.columns());
        for (Size i=0; i<result.size(); i++)
            result[i] =
                std::inner_product(v.begin(),v.end(),
                                   m.column_begin(i),Real(0.0));
        return result;
    }

    inline Array operator*(const Matrix& m, const A