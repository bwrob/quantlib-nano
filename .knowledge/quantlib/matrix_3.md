      return const_reverse_iterator(end());
    }

    inline Matrix::reverse_iterator Matrix::rbegin() {
        return reverse_iterator(end());
    }

    inline Matrix::const_reverse_iterator Matrix::rend() const {
        return const_reverse_iterator(begin());
    }

    inline Matrix::reverse_iterator Matrix::rend() {
        return reverse_iterator(begin());
    }

    inline Matrix::const_row_iterator
    Matrix::row_begin(Size i) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<rows_,
                   "row index (" << i << ") must be less than " << rows_ <<
                   ": matrix cannot be accessed out of range");
        #endif
        return data_.get()+columns_*i;
    }

    inline Matrix::row_iterator Matrix::row_begin(Size i) {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<rows_,
                   "row index (" << i << ") must be less than " << rows_ <<
                   ": matrix cannot be accessed out of range");
        #endif
        return data_.get()+columns_*i;
    }

    inline Matrix::const_row_iterator Matrix::row_end(Size i) const{
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<rows_,
                   "row index (" << i << ") must be less than " << rows_ <<
                   ": matrix cannot be accessed out of range");
        #endif
        return data_.get()+columns_*(i+1);
    }

    inline Matrix::row_iterator Matrix::row_end(Size i) {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<rows_,
                   "row index (" << i << ") must be less than " << rows_ <<
                   ": matrix cannot be accessed out of range");
        #endif
        return data_.get()+columns_*(i+1);
    }

    inline Matrix::const_reverse_row_iterator
    Matrix::row_rbegin(Size i) const {
        return const_reverse_row_iterator(row_end(i));
    }

    inline Matrix::reverse_row_iterator Matrix::row_rbegin(Size i) {
        return reverse_row_iterator(row_end(i));
    }

    inline Matrix::const_reverse_row_iterator
    Matrix::row_rend(Size i) const {
        return const_reverse_row_iterator(row_begin(i));
    }

    inline Matrix::reverse_row_iterator Matrix::row_rend(Size i) {
        return reverse_row_iterator(row_begin(i));
    }

    inline Matrix::const_column_iterator
    Matrix::column_begin(Size i) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<columns_,
                   "column index (" << i << ") must be less than " << columns_ <<
                   ": matrix cannot be accessed out of range");
        #endif
        return const_column_iterator(data_.get()+i,columns_);
    }

    inline Matrix::column_iterator Matrix::column_begin(Size i) {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<columns_,
                   "column index (" << i << ") must be less than " << columns_ <<
                   ": matrix cannot be accessed out of range");
        #endif
        return column_iterator(data_.get()+i,columns_);
    }

    inline Matrix::const_column_iterator
    Matrix::column_end(Size i) const {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<columns_,
                   "column index (" << i << ") must be less than " << columns_ <<
                   ": matrix cannot be accessed out of range");
        #endif
        return const_column_iterator(data_.get()+i+rows_*columns_,columns_);
    }

    inline Matrix::column_iterator Matrix::column_end(Size i) {
        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_REQUIRE(i<columns_,
                   "column index (" << i << ") must be less than " << columns_ <<
                   ": matrix cannot be accessed out of range");
        #endif
        return column_iterator(data_.get()+i+rows_*columns_,columns_);
    }

    inline Matrix::const_reverse_column_iterator
    Matrix::column_rbegin(Size i) const {
        return const_reverse_column_iterator(column_end(i));
    }

    inline Matrix::reverse_co
