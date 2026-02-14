oidPtr = std::conditional_t<ReadOnly, const void *, void *>;

    ndarray() = default;

    explicit ndarray(detail::ndarray_handle *handle) : m_handle(handle) {
        if (handle)
            m_dltensor = *detail::ndarray_inc_ref(handle);
    }

    template <typename... Args2>
    explicit ndarray(const ndarray<Args2...> &other) : ndarray(other.m_handle) { }

    ndarray(VoidPtr data,
            size_t ndim,
            const size_t *shape,
            handle owner = { },
            const int64_t *strides = nullptr,
            dlpack::dtype dtype = nanobind::dtype<Scalar>(),
            int device_type = DeviceType,
            int device_id = 0,
            char order = Order) {

        m_handle = detail::ndarray_create(
            (void *) data, ndim, shape, owner.ptr(), strides, dtype,
            ReadOnly, device_type, device_id, order);

        m_dltensor = *detail::ndarray_inc_ref(m_handle);
    }

    ndarray(VoidPtr data,
            std::initializer_list<size_t> shape = { },
            handle owner = { },
            std::initializer_list<int64_t> strides = { },
            dlpack::dtype dtype = nanobind::dtype<Scalar>(),
            int device_type = DeviceType,
            int device_id = 0,
            char order = Order) {

        size_t shape_size = shape.size();

        if (strides.size() != 0 && strides.size() != shape_size)
            detail::fail("ndarray(): shape and strides have incompatible size!");

        size_t shape_buf[Config::N <= 0 ? 1 : Config::N];
        const size_t *shape_ptr = shape.begin();

        if constexpr (Config::N > 0) {
            if (!shape_size) {
                Config::Shape::put(shape_buf);
                shape_size = Config::N;
                shape_ptr = shape_buf;
            }
        } else {
            (void) shape_buf;
        }

        m_handle = detail::ndarray_create(
            (void *) data, shape_size, shape_ptr, owner.ptr(),
            (strides.size() == 0) ? nullptr : strides.begin(), dtype,
            ReadOnly, device_type, device_id, order);

        m_dltensor = *detail::ndarray_inc_ref(m_handle);
    }

    ~ndarray() {
        detail::ndarray_dec_ref(m_handle);
    }

    ndarray(const ndarray &t) : m_handle(t.m_handle), m_dltensor(t.m_dltensor) {
        detail::ndarray_inc_ref(m_handle);
    }

    ndarray(ndarray &&t) noexcept : m_handle(t.m_handle), m_dltensor(t.m_dltensor) {
        t.m_handle = nullptr;
        t.m_dltensor = dlpack::dltensor();
    }

    ndarray &operator=(ndarray &&t) noexcept {
        detail::ndarray_dec_ref(m_handle);
        m_handle = t.m_handle;
        m_dltensor = t.m_dltensor;
        t.m_handle = nullptr;
        t.m_dltensor = dlpack::dltensor();
        return *this;
    }

    ndarray &operator=(const ndarray &t) {
        detail::ndarray_inc_ref(t.m_handle);
        detail::ndarray_dec_ref(m_handle);
        m_handle = t.m_handle;
        m_dltensor = t.m_dltensor;
        return *this;
    }

    dlpack::dtype dtype() const { return m_dltensor.dtype; }
    size_t ndim() const { return (size_t) m_dltensor.ndim; }
    size_t shape(size_t i) const { return (size_t) m_dltensor.shape[i]; }
    int64_t stride(size_t i) const { return m_dltensor.strides[i]; }
    const int64_t* shape_ptr() const { return m_dltensor.shape; }
    const int64_t* stride_ptr() const { return m_dltensor.strides; }
    bool is_valid() const { return m_handle != nullptr; }
    int device_type() const { return (int) m_dltensor.device.device_type; }
    int device_id() const { return (int) m_dltensor.device.device_id; }
    detail::ndarray_handle *handle() const { return m_handle; }

    size_t size() const {
        size_t ret = is_valid();
        for (size_t i = 0; i < ndim(); ++i)
            ret *= shape(i);
        return ret;
    }

    size_t itemsize() const { return ((size_t) dtype().bits + 7) / 8; }
    size_t nbytes() const { return ((size_t) dtype().bits * size() + 7) / 8; }

    Scalar *data() const {
        return 