t<base_data_table, EmptyRes> base_output_data;


        // cubic spline iplementations

        // no heap memory is allocated
        // in any of the recursive calls
        class base_cubic_spline {
          public:
            typedef Real argument_type;
            typedef Real result_type;
            typedef base_data data;
            typedef base_data_table data_table;
            typedef base_output_data output_data;
            base_cubic_spline(const data &d, const data &d2,
                              const data_table& y, data_table &y2,
                              output_data &v) {
                Size dim = d.first.size();
                Size j = 1, k = 2, l = 3;
                result_type  &w = ((y2[dim] = y[1]) -= y[0]) /= d[0],
                    &u = ((y2[0] = y[2]) -= y[1]) /= d[1], &t = v[dim];
                y2[1] = -d[1] / d2[0], v[1] = 6.0 * (u - w) / d2[0];
                for(; k < dim; u = w, j = k, k = l, ++l) {
                    w = (y[l]-y[k])/d[k];
                    u = (u-w)*6.0;
                    (y2[k] = d[k]) /= ((t = -y2[j]) *= d[j]) -= d2[j];
                    (v[k] = (u += d[j] * v[j])) /= t;
                }
                y2[0] = y2[dim] = 0.0;
                while (k != 0U) {
                    (y2[k-1] *= y2[l-1]) += v[k-1];
                    --k; --l;
                }
            }
        };

        template<class X>
        class n_cubic_spline {
          public:
            typedef Data<base_data, typename X::data> data;
            typedef DataTable<typename X::data_table> data_table;
            typedef Point<base_output_data, typename X::output_data> output_data;
            n_cubic_spline(const data &d, const data &d2,
                           const data_table &y, data_table &y2, output_data &v)
            :  d_(d), d2_(d2), y_(y), y2_(y2), v_(v) {
                for(Size j = 0, dim = y_.size();  j < dim; ++j)
                    X(d_.second, d2_.second, y_[j], y2_[j], v_.second);
            }
            ~n_cubic_spline() = default;

          private:
            const data &d_, &d2_;
            const data_table &y_;
            data_table &y2_;
            output_data &v_;
        };

        class base_cubic_splint {
          public:
            typedef base_arg_type argument_type;
            typedef Real result_type;
            typedef base_data data;
            typedef base_data_table data_table;
            typedef base_dimensions dimensions;
            typedef base_output_data output_data;
            typedef base_return_type return_type;
            base_cubic_splint(const return_type &a, const return_type &b,
                              const return_type &a2, const return_type &b2,
                              const dimensions &i,
                              const data&, const data&,
                              const data_table &y, data_table &y2,
                              output_data&,
                              output_data&, output_data&,
                              result_type &res) {
                res = a * y[i] + b * y[i + 1] + a2 * y2[i] + b2 * y2[i + 1];
            }
        };

        template<class X>
        class n_cubic_splint {
          public:
            typedef Point<Real, typename X::argument_type> argument_type;
            typedef Real result_type;
            typedef Data<base_data, typename X::data> data;
            typedef DataTable<typename X::data_table> data_table;
            typedef Point<Size, typename X::dimensions> dimensions;
            typedef Point<base_output_data, typename X::output_data> output_data;
            typedef Point<result_type,
                          typename X::return_type> return_type;
            n_cubic_splint(const return_type &a, const return_type &b,
                           const return_type &a2, const return_type &b2,
                           const dimensions &i, const data &d, const data &d2,
                           const data_table &y, data_