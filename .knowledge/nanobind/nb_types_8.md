rator-,  PyNumber_Negative)
NB_IMPL_OP_1(operator~,  PyNumber_Invert)
NB_IMPL_OP_2(operator+,  PyNumber_Add)
NB_IMPL_OP_2(operator-,  PyNumber_Subtract)
NB_IMPL_OP_2(operator*,  PyNumber_Multiply)
NB_IMPL_OP_2(operator/,  PyNumber_TrueDivide)
NB_IMPL_OP_2(operator%,  PyNumber_Remainder)
NB_IMPL_OP_2(operator|,  PyNumber_Or)
NB_IMPL_OP_2(operator&,  PyNumber_And)
NB_IMPL_OP_2(operator^,  PyNumber_Xor)
NB_IMPL_OP_2(operator<<, PyNumber_Lshift)
NB_IMPL_OP_2(operator>>, PyNumber_Rshift)
NB_IMPL_OP_2(floor_div,  PyNumber_FloorDivide)
NB_IMPL_OP_2_I(operator+=, PyNumber_InPlaceAdd)
NB_IMPL_OP_2_I(operator%=, PyNumber_InPlaceRemainder)
NB_IMPL_OP_2_I(operator-=, PyNumber_InPlaceSubtract)
NB_IMPL_OP_2_I(operator*=, PyNumber_InPlaceMultiply)
NB_IMPL_OP_2_I(operator/=, PyNumber_InPlaceTrueDivide)
NB_IMPL_OP_2_I(operator|=, PyNumber_InPlaceOr)
NB_IMPL_OP_2_I(operator&=, PyNumber_InPlaceAnd)
NB_IMPL_OP_2_I(operator^=, PyNumber_InPlaceXor)
NB_IMPL_OP_2_I(operator<<=,PyNumber_InPlaceLshift)
NB_IMPL_OP_2_I(operator>>=,PyNumber_InPlaceRshift)

#undef NB_DECL_COMP
#undef NB_IMPL_COMP
#undef NB_DECL_OP_1
#undef NB_IMPL_OP_1
#undef NB_DECL_OP_2
#undef NB_IMPL_OP_2
#undef NB_DECL_OP_2_I
#undef NB_IMPL_OP_2_I
#undef NB_IMPL_OP_2_IO

NAMESPACE_END(detail)

inline detail::dict_iterator dict::begin() const { return { *this }; }
inline detail::dict_iterator dict::end() const { return { }; }

#if !defined(Py_LIMITED_API) && !defined(PYPY_VERSION)
inline detail::fast_iterator tuple::begin() const {
    return ((PyTupleObject *) m_ptr)->ob_item;
}
inline detail::fast_iterator tuple::end() const {
    PyTupleObject *v = (PyTupleObject *) m_ptr;
    return v->ob_item + v->ob_base.ob_size;
}
inline detail::fast_iterator list::begin() const {
    return ((PyListObject *) m_ptr)->ob_item;
}
inline detail::fast_iterator list::end() const {
    PyListObject *v = (PyListObject *) m_ptr;
    return v->ob_item + v->ob_base.ob_size;
}
#endif

template <typename T> void del(detail::accessor<T> &a) { a.del(); }
template <typename T> void del(detail::accessor<T> &&a) { a.del(); }

NAMESPACE_END(NB_NAMESPACE)
