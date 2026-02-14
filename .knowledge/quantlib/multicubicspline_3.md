table &y2, output_data &v,
                           output_data &v1, output_data &v2,
                           result_type& r)
            :  a_(a), b_(b), a2_(a2), b2_(b2), i_(i), d_(d), d2_(d2),
               y_(y), y2_(y2), v_(v), v1_(v1), v2_(v2) {
                for(Size j = 0, dim = y_.size(); j < dim; ++j)
                    X(a_.second, b_.second, a2_.second, b2_.second, i_.second,
                      d_.second, d2_.second, y_[j], y2_[j], v_.second,
                      v1_.second, v2_.second, v1_.first[j]);
                base_cubic_spline(d_.first, d2_.first,
                                  v1_.first.first, v2_.first.first, v_.first);
                base_cubic_splint(a_.first, b_.first, a2_.first, b2_.first,
                                  i_.first, d_.first, d2_.first,
                                  v1_.first.first, v2_.first.first,
                                  v_.first, v1_.first, v2_.first, r);
            }
            ~n_cubic_splint() = default;

          private:
            const return_type &a_, &b_, &a2_, &b2_;
            const dimensions &i_;
            const data &d_, &d2_;
            const data_table &y_;
            data_table &y2_;
            output_data &v_, &v1_, &v2_;
        };

        typedef base_cubic_spline               cubic_spline_01;
        typedef n_cubic_spline<cubic_spline_01> cubic_spline_02;
        typedef n_cubic_spline<cubic_spline_02> cubic_spline_03;
        typedef n_cubic_spline<cubic_spline_03> cubic_spline_04;
        typedef n_cubic_spline<cubic_spline_04> cubic_spline_05;
        typedef n_cubic_spline<cubic_spline_05> cubic_spline_06;
        typedef n_cubic_spline<cubic_spline_06> cubic_spline_07;
        typedef n_cubic_spline<cubic_spline_07> cubic_spline_08;
        typedef n_cubic_spline<cubic_spline_08> cubic_spline_09;
        typedef n_cubic_spline<cubic_spline_09> cubic_spline_10;
        typedef n_cubic_spline<cubic_spline_10> cubic_spline_11;
        typedef n_cubic_spline<cubic_spline_11> cubic_spline_12;
        typedef n_cubic_spline<cubic_spline_12> cubic_spline_13;
        typedef n_cubic_spline<cubic_spline_13> cubic_spline_14;
        typedef n_cubic_spline<cubic_spline_14> cubic_spline_15;

        typedef base_cubic_splint               cubic_splint_01;
        typedef n_cubic_splint<cubic_splint_01> cubic_splint_02;
        typedef n_cubic_splint<cubic_splint_02> cubic_splint_03;
        typedef n_cubic_splint<cubic_splint_03> cubic_splint_04;
        typedef n_cubic_splint<cubic_splint_04> cubic_splint_05;
        typedef n_cubic_splint<cubic_splint_05> cubic_splint_06;
        typedef n_cubic_splint<cubic_splint_06> cubic_splint_07;
        typedef n_cubic_splint<cubic_splint_07> cubic_splint_08;
        typedef n_cubic_splint<cubic_splint_08> cubic_splint_09;
        typedef n_cubic_splint<cubic_splint_09> cubic_splint_10;
        typedef n_cubic_splint<cubic_splint_10> cubic_splint_11;
        typedef n_cubic_splint<cubic_splint_11> cubic_splint_12;
        typedef n_cubic_splint<cubic_splint_12> cubic_splint_13;
        typedef n_cubic_splint<cubic_splint_13> cubic_splint_14;
        typedef n_cubic_splint<cubic_splint_14> cubic_splint_15;

        template<Size i> struct Int2Type {
            typedef cubic_spline_01 c_spline;
            typedef cubic_splint_01 c_splint;
        };

        template<> struct Int2Type<2> {
            typedef cubic_spline_02 c_spline;
            typedef cubic_splint_02 c_splint;
        };

        template<> struct Int2Type<3> {
            typedef cubic_spline_03 c_spline;
            typedef cubic_splint_03 c_splint;
        };

        template<> struct Int2Type<4> {
            typedef cubic_spline_04 c_spline;
            typedef cubic_splint_04 c_splint;
        };

        template<> struct Int2Type<5> {
            typedef cubic_spline_05 c_spline;
            typedef cubic_splint_05 c_splint;
        };

        template<> struct Int2Type<6> {
            typedef cubic_spl