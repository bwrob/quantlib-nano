rray& v) {
        QL_REQUIRE(v.size() == m.columns(),
                   "vectors and matrices with different sizes ("
                   << v.size() << ", " << m.rows() << "x" << m.columns() <<
                   ") cannot be multiplied");
        Array result(m.rows());
        for (Size i=0; i<result.size(); i++)
            result[i] =
                std::inner_product(v.begin(),v.end(),m.row_begin(i),Real(0.0));
        return result;
    }

    inline Matrix operator*(const Matrix& m1, const Matrix& m2) {
        QL_REQUIRE(m1.columns() == m2.rows(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "multiplied");
        Matrix result(m1.rows(),m2.columns(),0.0);
        for (Size i=0; i<result.rows(); ++i) {
            for (Size k=0; k<m1.columns(); ++k) {
                for (Size j=0; j<result.columns(); ++j) {
                    result[i][j] += m1[i][k]*m2[k][j];
                }
            }
        }
        return result;
    }

    inline Matrix transpose(const Matrix& m) {
        Matrix result(m.columns(),m.rows());
        #if defined(QL_PATCH_MSVC) && defined(QL_DEBUG)
        if (!m.empty())
        #endif
        for (Size i=0; i<m.rows(); i++)
            std::copy(m.row_begin(i),m.row_end(i),result.column_begin(i));
        return result;
    }

    inline Matrix outerProduct(const Array& v1, const Array& v2) {
        return outerProduct(v1.begin(), v1.end(), v2.begin(), v2.end());
    }

    template <class Iterator1, class Iterator2>
    inline Matrix outerProduct(Iterator1 v1begin, Iterator1 v1end, Iterator2 v2begin, Iterator2 v2end) {

        Size size1 = std::distance(v1begin, v1end);
        QL_REQUIRE(size1>0, "null first vector");

        Size size2 = std::distance(v2begin, v2end);
        QL_REQUIRE(size2>0, "null second vector");

        Matrix result(size1, size2);

        for (Size i=0; v1begin!=v1end; i++, v1begin++)
            std::transform(v2begin, v2end, result.row_begin(i),
                           [=](Real y) -> Real { return y * (*v1begin); });

        return result;
    }

    inline void swap(Matrix& m1, Matrix& m2) noexcept {
        m1.swap(m2);
    }

    inline std::ostream& operator<<(std::ostream& out, const Matrix& m) {
        std::streamsize width = out.width();
        for (Size i=0; i<m.rows(); i++) {
            out << "| ";
            for (Size j=0; j<m.columns(); j++)
                out << std::setw(int(width)) << m[i][j] << " ";
            out << "|\n";
        }
        return out;
    }

}


#endif
