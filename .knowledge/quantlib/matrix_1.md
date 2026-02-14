reverse_iterator rbegin() const;
        reverse_iterator rbegin();
        const_reverse_iterator rend() const;
        reverse_iterator rend();
        const_row_iterator row_begin(Size i) const;
        row_iterator row_begin(Size i);
        const_row_iterator row_end(Size i) const;
        row_iterator row_end(Size i);
        const_reverse_row_iterator row_rbegin(Size i) const;
        reverse_row_iterator row_rbegin(Size i);
        const_reverse_row_iterator row_rend(Size i) const;
        reverse_row_iterator row_rend(Size i);
        const_column_iterator column_begin(Size i) const;
        column_iterator column_begin(Size i);
        const_column_iterator column_end(Size i) const;
        column_iterator column_end(Size i);
        const_reverse_column_iterator column_rbegin(Size i) const;
        reverse_column_iterator column_rbegin(Size i);
        const_reverse_column_iterator column_rend(Size i) const;
        reverse_column_iterator column_rend(Size i);
        //@}

        //! \name Element access
        //@{
        const_row_iterator operator[](Size) const;
        const_row_iterator at(Size) const;
        row_iterator operator[](Size);
        row_iterator at(Size);
        Array diagonal() const;
        Real& operator()(Size i, Size j) const;
        //@}

        //! \name Inspectors
        //@{
        Size rows() const;
        Size columns() const;
        bool empty() const;
        Size size1() const;
        Size size2() const;
        //@}

        //! \name Utilities
        //@{
        void swap(Matrix&) noexcept;
        //@}
      private:
        std::unique_ptr<Real[]> data_;
        Size rows_ = 0, columns_ = 0;
    };

    // algebraic operators

    /*! \relates Matrix */
    Matrix operator+(const Matrix&, const Matrix&);
    /*! \relates Matrix */
    Matrix operator+(const Matrix&, Matrix&&);
    /*! \relates Matrix */
    Matrix operator+(Matrix&&, const Matrix&);
    /*! \relates Matrix */
    Matrix operator+(Matrix&&, Matrix&&);
    /*! \relates Matrix */
    Matrix operator-(const Matrix&);
    /*! \relates Matrix */
    Matrix operator-(Matrix&&);
    /*! \relates Matrix */
    Matrix operator-(const Matrix&, const Matrix&);
    /*! \relates Matrix */
    Matrix operator-(const Matrix&, Matrix&&);
    /*! \relates Matrix */
    Matrix operator-(Matrix&&, const Matrix&);
    /*! \relates Matrix */
    Matrix operator-(Matrix&&, Matrix&&);
    /*! \relates Matrix */
    Matrix operator*(const Matrix&, Real);
    /*! \relates Matrix */
    Matrix operator*(Matrix&&, Real);
    /*! \relates Matrix */
    Matrix operator*(Real, const Matrix&);
    /*! \relates Matrix */
    Matrix operator*(Real, Matrix&&);
    /*! \relates Matrix */
    Matrix operator/(const Matrix&, Real);
    /*! \relates Matrix */
    Matrix operator/(Matrix&&, Real);

    // vectorial products

    /*! \relates Matrix */
    Array operator*(const Array&, const Matrix&);
    /*! \relates Matrix */
    Array operator*(const Matrix&, const Array&);
    /*! \relates Matrix */
    Matrix operator*(const Matrix&, const Matrix&);

    // misc. operations

    /*! \relates Matrix */
    Matrix transpose(const Matrix&);

    /*! \relates Matrix */
    Matrix outerProduct(const Array& v1, const Array& v2);

    /*! \relates Matrix */
    template <class Iterator1, class Iterator2>
    Matrix outerProduct(Iterator1 v1begin, Iterator1 v1end, Iterator2 v2begin, Iterator2 v2end);

    /*! \relates Matrix */
    void swap(Matrix&, Matrix&) noexcept;

    /*! \relates Matrix */
    std::ostream& operator<<(std::ostream&, const Matrix&);

    /*! \relates Matrix */
    Matrix inverse(const Matrix& m);

    /*! \relates Matrix */
    Real determinant(const Matrix& m);

    // inline definitions

    inline Matrix::Matrix() : data_((Real*)nullptr) {}

    inline Matrix::Matrix(Size rows, Size columns)
    : data_(rows * columns > 0 ? new Real[rows * columns] : (Real*)nullptr), rows_(rows),
      columns_(columns) {}

    in