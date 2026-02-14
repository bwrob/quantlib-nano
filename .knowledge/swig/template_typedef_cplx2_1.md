 this part */
  %template() unary_func_traits<double,Complex>;
  %template(UnaryFunction_double_complex) UnaryFunction<double,Complex>;
  %template(ArithUnaryFunction_double_complex) ArithUnaryFunction<double,Complex>;

  /* */

  %template() arith_traits<Complex, double >;
  %template() arith_traits<double, Complex >;

  %template(make_Multiplies_double_double_complex_complex)
    make_Multiplies<double, double, Complex, Complex>;

  %template(make_Multiplies_double_double_double_double)
    make_Multiplies<double, double, double, double>;

  %template(make_Multiplies_complex_complex_complex_complex)
    make_Multiplies<Complex, Complex, Complex, Complex>;

  %template(make_Multiplies_complex_complex_double_double)
    make_Multiplies<Complex, Complex, double, double>;

}

#endif

#endif // TEMPLATE_TYPEDEF_CPLX2_H