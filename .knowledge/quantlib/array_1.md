 Inspectors
        //@{
        //! dimension of the array
        Size size() const;
        //! whether the array is empty
        bool empty() const;
        //@}
        typedef Size size_type;
        typedef Real value_type;
        typedef Real* iterator;
        typedef const Real* const_iterator;
        typedef std::reverse_iterator<iterator> reverse_iterator;
        typedef std::reverse_iterator<const_iterator> const_reverse_iterator;
        //! \name Iterator access
        //@{
        const_iterator begin() const;
        iterator begin();
        const_iterator end() const;
        iterator end();
        const_reverse_iterator rbegin() const;
        reverse_iterator rbegin();
        const_reverse_iterator rend() const;
        reverse_iterator rend();
        //@}
        //! \name Utilities
        //@{
        void resize(Size n);
        void swap(Array&) noexcept;
        //@}

      private:
        std::unique_ptr<Real[]> data_;
        Size n_;
    };


    /*! \relates Array */
    Real DotProduct(const Array&, const Array&);

    /*! \relates Array */
    Real Norm2(const Array&);

    // unary operators
    /*! \relates Array */
    Array operator+(const Array& v);
    /*! \relates Array */
    Array operator+(Array&& v);
    /*! \relates Array */
    Array operator-(const Array& v);
    /*! \relates Array */
    Array operator-(Array&& v);

    // binary operators
    /*! \relates Array */
    Array operator+(const Array&, const Array&);
    /*! \relates Array */
    Array operator+(const Array&, Array&&);
    /*! \relates Array */
    Array operator+(Array&&, const Array&);
    /*! \relates Array */
    Array operator+(Array&&, Array&&);
    /*! \relates Array */
    Array operator+(const Array&, Real);
    /*! \relates Array */
    Array operator+(Array&&, Real);
    /*! \relates Array */
    Array operator+(Real, const Array&);
    /*! \relates Array */
    Array operator+(Real, Array&&);
    /*! \relates Array */
    Array operator-(const Array&, const Array&);
    /*! \relates Array */
    Array operator-(const Array&, Array&&);
    /*! \relates Array */
    Array operator-(Array&&, const Array&);
    /*! \relates Array */
    Array operator-(Array&&, Array&&);
    /*! \relates Array */
    Array operator-(const Array&, Real);
    /*! \relates Array */
    Array operator-(Real, const Array&);
    /*! \relates Array */
    Array operator-(Array&&, Real);
    /*! \relates Array */
    Array operator-(Real, Array&&);
    /*! \relates Array */
    Array operator*(const Array&, const Array&);
    /*! \relates Array */
    Array operator*(const Array&, Array&&);
    /*! \relates Array */
    Array operator*(Array&&, const Array&);
    /*! \relates Array */
    Array operator*(Array&&, Array&&);
    /*! \relates Array */
    Array operator*(const Array&, Real);
    /*! \relates Array */
    Array operator*(Real, const Array&);
    /*! \relates Array */
    Array operator*(Array&&, Real);
    /*! \relates Array */
    Array operator*(Real, Array&&);
    /*! \relates Array */
    Array operator/(const Array&, const Array&);
    /*! \relates Array */
    Array operator/(const Array&, Array&&);
    /*! \relates Array */
    Array operator/(Array&&, const Array&);
    /*! \relates Array */
    Array operator/(Array&&, Array&&);
    /*! \relates Array */
    Array operator/(const Array&, Real);
    /*! \relates Array */
    Array operator/(Real, const Array&);
    /*! \relates Array */
    Array operator/(Array&&, Real);
    /*! \relates Array */
    Array operator/(Real, Array&&);

    // math functions
    /*! \relates Array */
    Array Abs(const Array&);
    /*! \relates Array */
    Array Abs(Array&&);
    /*! \relates Array */
    Array Sqrt(const Array&);
    /*! \relates Array */
    Array Sqrt(Array&&);
    /*! \relates Array */
    Array Log(const Array&);
    /*! \relates Array */
    Array Log(Array&&);
    /*! \relates Array */
    Array Exp(const Array&);
    /*! \relates Array */
    Arra
