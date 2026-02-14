shared libraries with duplicate RTTI data
struct nb_alias_chain {
    const std::type_info *value;
    nb_alias_chain *next;
};

// Weak reference list. Usually, there is just one entry
struct nb_weakref_seq {
    void (*callback)(void *) noexcept;
    void *payload;
    nb_weakref_seq *next;
};

struct std_typeinfo_hash {
    size_t operator()(const std::type_info *a) const {
        const char *name = a->name();
        return std::hash<std::string_view>()({name, strlen(name)});
    }
};

struct std_typeinfo_eq {
    bool operator()(const std::type_info *a, const std::type_info *b) const {
        return a->name() == b->name() || strcmp(a->name(), b->name()) == 0;
    }
};

/// A simple pointer-to-pointer map that is reused a few times below (even if
/// not 100% ideal) to avoid template code generation bloat.
using nb_ptr_map  = tsl::robin_map<void *, void*, ptr_hash>;

using nb_type_map_fast = nb_ptr_map;
using nb_type_map_slow = tsl::robin_map<const std::type_info *, type_data *,
                                        std_typeinfo_hash, std_typeinfo_eq>;

/// Convenience functions to deal with the pointer encoding in 'internals.inst_c2p'

/// Does this entry store a linked list of instances?
NB_INLINE bool         nb_is_seq(void *p)   { return ((uintptr_t) p) & 1; }

/// Tag a nb_inst_seq* pointer as such
NB_INLINE void*        nb_mark_seq(void *p) { return (void *) (((uintptr_t) p) | 1); }

/// Retrieve the nb_inst_seq* pointer from an 'inst_c2p' value
NB_INLINE nb_inst_seq* nb_get_seq(void *p)  { return (nb_inst_seq *) (((uintptr_t) p) ^ 1); }

struct nb_translator_seq {
    exception_translator translator;
    void *payload;
    nb_translator_seq *next = nullptr;
};

#if defined(NB_FREE_THREADED)
