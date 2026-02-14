td::ostringstream _ql_msg_stream; \
    _ql_msg_stream << message; \
    throw QuantLib::Error(__FILE__,__LINE__, \
                          BOOST_CURRENT_FUNCTION,_ql_msg_stream.str()); \
} \
QL_MULTILINE_ASSERTION_END


#endif