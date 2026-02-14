lumn_iterator
    Matrix::column_rbegin(Size i) {
        return reverse_column_iterator(column_end(i));
    }

    inline Matrix::const_reverse_column_iterator
    Matrix::column_rend(Size i) const {
        return const_reverse_column_iterator(column_begin(i));
    }

    inline Matrix::reverse_column_iterator
    Matrix::column_rend(Size i) {
        return reverse_column_iterator(column_begin(i));
    }

    inline Matrix::const_row_iterator
    Matrix::operator[](Size i) const {
        return row_begin(i);
    }

    inline Matrix::const_row_iterator
    Matrix::at(Size i) const {
        QL_REQUIRE(i < rows_, "matrix access out of range");
        return row_begin(i);
    }

    inline Matrix::row_iterator Matrix::operator[](Size i) {
        return row_begin(i);
    }

    inline Matrix::row_iterator Matrix::at(Size i) {
        QL_REQUIRE(i < rows_, "matrix access out of range");
        return row_begin(i);
    }

    inline Array Matrix::diagonal() const {
        Size arraySize = std::min<Size>(rows(), columns());
        Array tmp(arraySize);
        for(Size i = 0; i < arraySize; i++)
            tmp[i] = (*this)[i][i];
        return tmp;
    }

    inline Real &Matrix::operator()(Size i, Size j) const {
        return data_[i*columns()+j];
    }

    inline Size Matrix::rows() const {
        return rows_;
    }

    inline Size Matrix::columns() const {
        return columns_;
    }

    inline Size Matrix::size1() const {
        return rows();
    }

    inline Size Matrix::size2() const {
        return columns();
    }

    inline bool Matrix::empty() const {
        return rows_ == 0 || columns_ == 0;
    }

    inline Matrix operator+(const Matrix& m1, const Matrix& m2) {
        QL_REQUIRE(m1.rows() == m2.rows() &&
                   m1.columns() == m2.columns(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "added");
        Matrix temp(m1.rows(),m1.columns());
        std::transform(m1.begin(), m1.end(), m2.begin(), temp.begin(), std::plus<>());
        return temp;
    }

    inline Matrix operator+(const Matrix& m1, Matrix&& m2) {
        QL_REQUIRE(m1.rows() == m2.rows() &&
                   m1.columns() == m2.columns(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "added");
        std::transform(m1.begin(), m1.end(), m2.begin(), m2.begin(), std::plus<>());
        return std::move(m2);
    }

    inline Matrix operator+(Matrix&& m1, const Matrix& m2) {
        QL_REQUIRE(m1.rows() == m2.rows() &&
                   m1.columns() == m2.columns(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "added");
        std::transform(m1.begin(), m1.end(), m2.begin(), m1.begin(), std::plus<>());
        return std::move(m1);
    }

    inline Matrix operator+(Matrix&& m1, Matrix&& m2) { // NOLINT(cppcoreguidelines-rvalue-reference-param-not-moved)
        QL_REQUIRE(m1.rows() == m2.rows() &&
                   m1.columns() == m2.columns(),
                   "matrices with different sizes (" <<
                   m1.rows() << "x" << m1.columns() << ", " <<
                   m2.rows() << "x" << m2.columns() << ") cannot be "
                   "added");
        std::transform(m1.begin(), m1.end(), m2.begin(), m1.begin(), std::plus<>());
        return std::move(m1);
    }

    inline Matrix operator-(const Matrix& m1) {
        Matrix temp(m1.rows(), m1.columns());
        std::transform(m1.begin(), m1.end(), temp.begin(), std::negate<>());
        return temp;
    }

    inline Matrix operator-(Matrix&& m1) {
        std::transf
