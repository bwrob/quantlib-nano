E = int> struct type_caster;
template <typename T> using make_caster = type_caster<intrinsic_t<T>>;

template <typename Impl> class accessor;
struct str_attr; struct obj_attr;
struct str_item; struct obj_item; struct num_item;
struct num_item_list; struct num_item_tuple;
class args_proxy; class kwargs_proxy;
struct borrow_t { };
struct steal_t { };
struct api_tag {
    constexpr static bool nb_typed = false;
};
class dict_iterator;
struct fast_iterator;

// Standard operations provided by every nanobind object
template <typename Derived> class api : public api_tag {
public:
    Derived &derived() { return static_cast<Derived &>(*this); }
    const Derived &derived() const { return static_cast<const Derived &>(*this); }

    NB_INLINE bool is(handle value) const;
    NB_INLINE bool is_none() const { return derived().ptr() == Py_None; }
    NB_INLINE bool is_type() const { return PyType_Check(derived().ptr()); }
    NB_INLINE bool is_valid() const { return derived().ptr() != nullptr; }
    NB_INLINE handle inc_ref() const &;
    NB_INLINE handle dec_ref() const &;
    iterator begin() const;
    iterator end() const;

    NB_INLINE handle type() const;
    NB_INLINE operator handle() const;

    accessor<obj_attr> attr(handle key) const;
    accessor<str_attr> attr(const char *key) const;
    accessor<str_attr> doc() const;

    accessor<obj_item> operator[](handle key) const;
    accessor<str_item> operator[](const char *key) const;
    template <typename T, enable_if_t<std::is_arithmetic_v<T>> = 1>
    accessor<num_item> operator[](T key) const;
    args_proxy operator*() const;

    template <rv_policy policy = rv_policy::automatic_reference,
              typename... Args>
    object operator()(Args &&...args) const;

    NB_DECL_COMP(equal)
    NB_DECL_COMP(not_equal)
    NB_DECL_COMP(operator<)
    NB_DECL_COMP(operator<=)
    NB_DECL_COMP(operator>)
    NB_DECL_COMP(operator>=)
    NB_DECL_OP_1(operator-)
    NB_DECL_OP_1(operator~)
    NB_DECL_OP_2(operator+)
    NB_DECL_OP_2(operator-)
    NB_DECL_OP_2(operator*)
    NB_DECL_OP_2(operator/)
    NB_DECL_OP_2(operator%)
    NB_DECL_OP_2(operator|)
    NB_DECL_OP_2(operator&)
    NB_DECL_OP_2(operator^)
    NB_DECL_OP_2(operator<<)
    NB_DECL_OP_2(operator>>)
    NB_DECL_OP_2(floor_div)
    NB_DECL_OP_2_I(operator+=)
    NB_DECL_OP_2_I(operator-=)
    NB_DECL_OP_2_I(operator*=)
    NB_DECL_OP_2_I(operator/=)
    NB_DECL_OP_2_I(operator%=)
    NB_DECL_OP_2_I(operator|=)
    NB_DECL_OP_2_I(operator&=)
    NB_DECL_OP_2_I(operator^=)
    NB_DECL_OP_2_I(operator<<=)
    NB_DECL_OP_2_I(operator>>=)
};

NAMESPACE_END(detail)

// *WARNING*: nanobind regularly receives requests from users who run it
// through Clang-Tidy, or who compile with increased warnings levels, like
//
//     -Wcast-qual, -Wsign-conversion, etc.
//
// (i.e., beyond -Wall -Wextra and /W4 that are currently already used)
//
// Their next step is to open a big pull request needed to silence all of
// the resulting messages.  This comment is strategically placed here
// because the (PyObject *) casts below cast away the const qualifier and
// will almost certainly be flagged in this process.
//
// My policy on this is as follows: I am always happy to fix issues in the
// codebase.  However, many of the resulting change requests are in the
// "ritual purification" category: things that cause churn, decrease
// readability, and which don't fix actual problems.  It's a never-ending
// cycle because each new revision of such tooling adds further warnings
// and purification rites.
//
// So just to be clear: I do not wish to pepper this codebase with
// "const_cast" and #pragmas/comments to avoid warnings in external
// tooling just so those users can have a "silent" build.  I don't think it
// is reasonable for them to impose their own style on this project.
//
// As a workaround it is likely possible to restrict the scope of style
// checks to particular C++ namespaces or source code locations.

class handle : pub