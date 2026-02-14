y Exp(Array&&);
    /*! \relates Array */
    Array Pow(const Array&, Real);
    /*! \relates Array */
    Array Pow(Array&&, Real);

    // utilities
    /*! \relates Array */
    void swap(Array&, Array&) noexcept;

    // format
    /*! \relates Array */
    std::ostream& operator<<(std::ostream&, const Array&);


    // inline definitions

    inline Array::Array(Size size)
    : data_(size != 0U ? new Real[size] : (Real*)nullptr), n_(size) {}

    inline Array::Array(Size size, Real value)
    : data_(size != 0U ? new Real[size] : (Real*)nullptr), n_(size) {
        std::fill(begin(),end(),value);
    }

    inline Array::Array(Size size, Real value, Real increment)
    : data_(size != 0U ? new Real[size] : (Real*)nullptr), n_(size) {
        for (iterator i=begin(); i!=end(); ++i, value+=increment)
            *i = value;
    }

    inline Array::Array(const Array& from)
    : data_(from.n_ != 0U ? new Real[from.n_] : (Real*)nullptr), n_(from.n_) {
        if (data_)
            std::copy(from.begin(),from.end(),begin());
    }

    inline Array::Array(Array&& from) noexcept
    : data_((Real*)nullptr), n_(0) {
        swap(from);
    }

    namespace detail {

        template <class I>
        inline void _fill_array_(Array& a,
                                 std::unique_ptr<Real[]>& data_,
                                 Size& n_,
                                 I begin, I end,
                                 const std::true_type&) {
            // we got redirected here from a call like Array(3, 4)
            // because it matched the constructor below exactly with
            // ForwardIterator = int.  What we wanted was fill an
            // Array with a given value, which we do here.
            Size n = begin;
            Real value = end;
            data_.reset(n ? new Real[n] : (Real*)nullptr);
            n_ = n;
            std::fill(a.begin(),a.end(),value);
        }

        template <class I>
        inline void _fill_array_(Array& a,
                                 std::unique_ptr<Real[]>& data_,
                                 Size& n_,
                                 const I& begin, const I& end,
                                 const std::false_type&) {
            // true iterators
            Size n = std::distance(begin, end);
            data_.reset(n ? new Real[n] : (Real*)nullptr);
            n_ = n;
            #if defined(QL_PATCH_MSVC) && defined(QL_DEBUG)
            if (n_)
            #endif
            std::copy(begin, end, a.begin());
        }

    }

    inline Array::Array(std::initializer_list<Real> init) {
        detail::_fill_array_(*this, data_, n_, init.begin(), init.end(),
                             std::false_type());
    }

    template <class ForwardIterator>
    inline Array::Array(ForwardIterator begin, ForwardIterator end) {   // NOLINT(performance-unnecessary-value-param)
        // Unfortunately, calls such as Array(3, 4) match this constructor.
        // We have to detect integral types and dispatch.
        detail::_fill_array_(*this, data_, n_, begin, end,
                             std::is_integral<ForwardIterator>());
    }

    template <typename T, typename>
    Array::Array(std::initializer_list<T> init) {
        detail::_fill_array_(*this, data_, n_, init.begin(), init.end(), std::false_type());
    }

    inline Array& Array::operator=(const Array& from) {
        // strong guarantee
        Array temp(from);
        swap(temp);
        return *this;
    }

    inline Array& Array::operator=(Array&& from) noexcept {
        swap(from);
        return *this;
    }

    inline bool Array::operator==(const Array& to) const {
        return (n_ == to.n_) && std::equal(begin(), end(), to.begin());
    }

    inline bool Array::operator!=(const Array& to) const {
        return !(this->operator==(to));
    }

    inline const Array& Array::operator+=(const Array& v) {
        QL_REQUIRE(n_ == v.n_,
                   "arrays with different sizes ("
