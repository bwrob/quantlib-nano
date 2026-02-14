
            result = nb_type_put(type, ptr, rv_policy::reference,
                                 cleanup, &is_new);
        } else {
            const std::type_info *type_p =
                (!has_type_hook && ptr) ? &typeid(*ptr) : nullptr;

            result = nb_type_put_p(type, type_p, ptr, rv_policy::reference,
                                   cleanup, &is_new);
        }

        if (is_new) {
            std::shared_ptr<void> pp;
            if constexpr (std::is_const_v<T>)
                pp = std::static_pointer_cast<void>(std::const_pointer_cast<Td>(value));
            else
                pp = std::static_pointer_cast<void>(value);
            shared_from_cpp(std::move(pp), result.ptr());
        }

        return result;
    }
};

NAMESPACE_END(detail)
NAMESPACE_END(NB_NAMESPACE)