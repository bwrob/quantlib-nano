if (src.is_none() && flags & (uint8_t) cast_flags::accepts_none) {
            value = ndarray<Args...>();
            return true;
        }

        int64_t shape_buf[Config::N <= 0 ? 1 : Config::N];
        ndarray_config config{Config()};

        if constexpr (Config::N > 0) {
            Config::Shape::put(shape_buf);
            config.shape = shape_buf;
        } else {
            (void) shape_buf;
        }

        value = Value(ndarray_import(src.ptr(), &config,
                                     flags & (uint8_t) cast_flags::convert,
                                     cleanup));

        return value.is_valid();
    }

    static handle from_cpp(const ndarray<Args...> &tensor, rv_policy policy,
                           cleanup_list *cleanup) noexcept {
        return ndarray_export(tensor.handle(), Config::Framework::value, policy, cleanup);
    }
};

template <typename... Args>
class ndarray_object : public object {
public:
    using object::object;
    using object::operator=;
    static constexpr auto Name = type_caster<ndarray<Args...>>::Name;
};

NAMESPACE_END(detail)

template <typename... Args>
auto ndarray<Args...>::cast(rv_policy rvp, class handle parent) {
    return borrow<detail::ndarray_object<Args...>>(
        nanobind::cast(*this, rvp, parent));
}

NAMESPACE_END(NB_NAMESPACE)
