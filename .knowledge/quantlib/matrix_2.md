line Matrix::Matrix(Size rows, Size columns, Real value)
    : data_(rows * columns > 0 ? new Real[rows * columns] : (Real*)nullptr), rows_(rows),
      columns_(columns) {
        std::fill(begin(),end(),value);
    }

    template <class Iterator>
    inline Matrix::Matrix(Size rows, Size columns, Iterator begin, Iterator end)
    : data_(rows * columns > 0 ? new Real[rows * columns] : (Real*)nullptr), rows_(rows),
      columns_(columns) {
        std::copy(begin, end, this->begin());
    }

    inline Matrix::Matrix(const Matrix& from)
    : data_(!from.empty() ? new Real[from.rows_ * from.columns_] : (Real*)nullptr),
      rows_(from.rows_), columns_(from.columns_) {
        #if defined(QL_PATCH_MSVC) && defined(QL_DEBUG)
        if (!from.empty())
        #endif
        std::copy(from.begin(),from.end(),begin());
    }

    inline Matrix::Matrix(Matrix&& from) noexcept
    : data_((Real*)nullptr) {
        swap(from);
    }

    inline Matrix::Matrix(std::initializer_list<std::initializer_list<Real>> data)
    : data_(data.size() == 0 || data.begin()->size() == 0 ?
            (Real*)nullptr : new Real[data.size() * data.begin()->size()]),
      rows_(data.size()), columns_(data.size() == 0 ? 0 : data.begin()->size()) {
        Size i=0;
        for (const auto& row : data) {
            #if defined(QL_EXTRA_SAFETY_CHECKS)
            QL_REQUIRE(row.size() == columns_,
                       "a matrix needs the same number of elements for each row");
            #endif
            std::copy(row.begin(), row.end(), row_begin(i));
            ++i;
        }
    }

    inline Matrix& Matrix::operator=(const Matrix& from) {
        // strong guarantee
        Matrix temp(from);
        swap(temp);
        return *this;
    }

    inline Matrix& Matrix::operator=(Matrix&& from) noexcept {
        swap(from);
        return *this;
    }

    inline bool Matrix::operator==(const Matrix& to) const {
        return rows_ == to.rows_ && columns_ == to.columns_ &&
               std::equal(begin(), end(), to.begin());
    }

    inline bool Matrix::operator!=(const Matrix& to) const { 
        return !this->operator==(to); 
    }

    inline void Matrix::swap(Matrix& from) noexcept {
        data_.swap(from.data_);
        std::swap(rows_, from.rows_);
        std::swap(columns_, from.columns_);
    }

    inline const Matrix& Matrix::operator+=(const Matrix& m) {
        QL_REQUIRE(rows_ == m.rows_ && columns_ == m.columns_,
                   "matrices with different sizes (" <<
                   m.rows_ << "x" << m.columns_ << ", " <<
                   rows_ << "x" << columns_ << ") cannot be "
                   "added");
        std::transform(begin(), end(), m.begin(), begin(), std::plus<>());
        return *this;
    }

    inline const Matrix& Matrix::operator-=(const Matrix& m) {
        QL_REQUIRE(rows_ == m.rows_ && columns_ == m.columns_,
                   "matrices with different sizes (" <<
                   m.rows_ << "x" << m.columns_ << ", " <<
                   rows_ << "x" << columns_ << ") cannot be "
                   "subtracted");
        std::transform(begin(), end(), m.begin(), begin(), std::minus<>());
        return *this;
    }

    inline const Matrix& Matrix::operator*=(Real x) {
        std::transform(begin(), end(), begin(), [=](Real y) -> Real { return y * x; });
        return *this;
    }

    inline const Matrix& Matrix::operator/=(Real x) {
        std::transform(begin(),end(),begin(), [=](Real y) -> Real { return y / x; });
        return *this;
    }

    inline Matrix::const_iterator Matrix::begin() const {
        return data_.get();
    }

    inline Matrix::iterator Matrix::begin() {
        return data_.get();
    }

    inline Matrix::const_iterator Matrix::end() const {
        return data_.get()+rows_*columns_;
    }

    inline Matrix::iterator Matrix::end() {
        return data_.get()+rows_*columns_;
    }

    inline Matrix::const_reverse_iterator Matrix::rbegin() const {
  