 {    \
    return op_<op_##id, op_r, T, self_t>();                                            \
}

#define NB_INPLACE_OPERATOR(id, op, expr)                                              \
template <typename B, typename L, typename R> struct op_impl<op_##id, op_l, B, L, R> { \
    static constexpr rv_policy default_policy = rv_policy::move;                       \
    static char const* name() { return "__" #id "__"; }                                \
    static auto execute(L &l, const R &r) -> decltype(expr) { return expr; }           \
    static B execute_cast(L &l, const R &r) { return B(expr); }                        \
};                                                                                     \
template <typename T> op_<op_##id, op_l, self_t, T> op(const self_t &, const T &) {    \
    return op_<op_##id, op_l, self_t, T>();                                            \
}

#define NB_UNARY_OPERATOR(id, op, expr)                                                \
template <typename B, typename L> struct op_impl<op_##id, op_u, B, L, undefined_t> {   \
    static constexpr rv_policy default_policy = rv_policy::automatic;                  \
    static char const* name() { return "__" #id "__"; }                                \
    static auto execute(const L &l) -> decltype(expr) { return expr; }                 \
    static B execute_cast(const L &l) { return B(expr); }                              \
};                                                                                     \
inline op_<op_##id, op_u, self_t, undefined_t> op(const self_t &) {                    \
    return op_<op_##id, op_u, self_t, undefined_t>();                                  \
}

NB_BINARY_OPERATOR(sub,       rsub,         operator-,    l - r)
NB_BINARY_OPERATOR(add,       radd,         operator+,    l + r)
NB_BINARY_OPERATOR(mul,       rmul,         operator*,    l * r)
NB_BINARY_OPERATOR(truediv,   rtruediv,     operator/,    l / r)
NB_BINARY_OPERATOR(mod,       rmod,         operator%,    l % r)
NB_BINARY_OPERATOR(lshift,    rlshift,      operator<<,   l << r)
NB_BINARY_OPERATOR(rshift,    rrshift,      operator>>,   l >> r)
NB_BINARY_OPERATOR(and,       rand,         operator&,    l & r)
NB_BINARY_OPERATOR(xor,       rxor,         operator^,    l ^ r)
NB_BINARY_OPERATOR(or,        ror,          operator|,    l | r)
NB_BINARY_OPERATOR(gt,        lt,           operator>,    l > r)
NB_BINARY_OPERATOR(ge,        le,           operator>=,   l >= r)
NB_BINARY_OPERATOR(lt,        gt,           operator<,    l < r)
NB_BINARY_OPERATOR(le,        ge,           operator<=,   l <= r)
NB_BINARY_OPERATOR(eq,        eq,           operator==,   l == r)
NB_BINARY_OPERATOR(ne,        ne,           operator!=,   l != r)
NB_INPLACE_OPERATOR(iadd,     operator+=,   l += r)
NB_INPLACE_OPERATOR(isub,     operator-=,   l -= r)
NB_INPLACE_OPERATOR(imul,     operator*=,   l *= r)
NB_INPLACE_OPERATOR(itruediv, operator/=,   l /= r)
NB_INPLACE_OPERATOR(imod,     operator%=,   l %= r)
NB_INPLACE_OPERATOR(ilshift,  operator<<=,  l <<= r)
NB_INPLACE_OPERATOR(irshift,  operator>>=,  l >>= r)
NB_INPLACE_OPERATOR(iand,     operator&=,   l &= r)
NB_INPLACE_OPERATOR(ixor,     operator^=,   l ^= r)
NB_INPLACE_OPERATOR(ior,      operator|=,   l |= r)
NB_UNARY_OPERATOR(neg,        operator-,    -l)
NB_UNARY_OPERATOR(pos,        operator+,    +l)
NB_UNARY_OPERATOR(invert,     operator~,    (~l))
NB_UNARY_OPERATOR(bool,       operator!,    !!l)
NB_UNARY_OPERATOR(abs,        abs,          std::abs(l))
NB_UNARY_OPERATOR(hash,       hash,         std::hash<L>()(l))

#undef NB_BINARY_OPERATOR
#undef NB_INPLACE_OPERATOR
#undef NB_UNARY_OPERATOR

NAMESPACE_END(detail)

// Add named operators so that they are accessible via `nb::`.
using detail::self;
using detail::hash;
using detail::abs;

NAMESPACE_END(NB_NAMESPACE)