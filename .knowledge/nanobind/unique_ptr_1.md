      bool cpp_delete = true;
        if constexpr (IsNanobindDeleter)
            cpp_delete = value.get_deleter().owned_by_cpp();

        Td *ptr = (Td *) value.get();
        const std::type_info *type = &typeid(Td);
        if (!ptr)
            return none().release();

        constexpr bool has_type_hook =
            !std::is_base_of_v<std::false_type, type_hook<Td>>;
        if constexpr (has_type_hook)
            type = type_hook<Td>::get(ptr);

        handle result;
        if constexpr (!std::is_polymorphic_v<Td>) {
            result = nb_type_put_unique(type, ptr, cleanup, cpp_delete);
        } else {
            const std::type_info *type_p =
                (!has_type_hook && ptr) ? &typeid(*ptr) : nullptr;

            result = nb_type_put_unique_p(type, type_p, ptr, cleanup, cpp_delete);
        }

        if (result.is_valid()) {
            if (cpp_delete)
                value.release();
            else
                value.reset();
        }

        return result;
    }

    template <typename T_>
    bool can_cast() const noexcept {
        if (src.is_none() || inflight)
            return true;
        else if (!nb_type_relinquish_ownership(src.ptr(), IsDefaultDeleter))
            return false;
        inflight = true;
        return true;
    }

    explicit operator Value() {
        if (!inflight && !src.is_none() &&
            !nb_type_relinquish_ownership(src.ptr(), IsDefaultDeleter))
            throw next_overload();

        Td *p = caster.operator Td *();

        Value value;
        if constexpr (IsNanobindDeleter)
            value = Value(p, deleter<T>(src.inc_ref()));
        else
            value = Value(p);
        inflight = false;
        return value;
    }
};

NAMESPACE_END(detail)
NAMESPACE_END(NB_NAMESPACE)
