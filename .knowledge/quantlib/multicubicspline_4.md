int_06 c_splint;
            typedef cubic_spline_06 c_spline;
        };

        template<> struct Int2Type<7> {
            typedef cubic_spline_07 c_spline;
            typedef cubic_splint_07 c_splint;
        };

        template<> struct Int2Type<8> {
            typedef cubic_spline_08 c_spline;
            typedef cubic_splint_08 c_splint;
        };

        template<> struct Int2Type<9> {
            typedef cubic_spline_09 c_spline;
            typedef cubic_splint_09 c_splint;
        };

        template<> struct Int2Type<10> {
            typedef cubic_spline_10 c_spline;
            typedef cubic_splint_10 c_splint;
        };

        template<> struct Int2Type<11> {
            typedef cubic_splint_11 c_splint;
            typedef cubic_spline_11 c_spline;
        };

        template<> struct Int2Type<12> {
            typedef cubic_spline_12 c_spline;
            typedef cubic_splint_12 c_splint;
        };

        template<> struct Int2Type<13> {
            typedef cubic_spline_13 c_spline;
            typedef cubic_splint_13 c_splint;
        };

        template<> struct Int2Type<14> {
            typedef cubic_spline_14 c_spline;
            typedef cubic_splint_14 c_splint;
        };

        template<> struct Int2Type<15> {
            typedef cubic_spline_15 c_spline;
            typedef cubic_splint_15 c_splint;
        };

    }


    // Multi-cubic spline

    typedef detail::SplineGrid SplineGrid;

    //! N-dimensional cubic spline interpolation between discrete points
    /*! \test interpolated values are checked against the original
              function.

        \todo
        - allow extrapolation as for the other interpolations
        - investigate if and how to implement Hyman filters and
          different boundary conditions

        \bug cannot interpolate at the grid points on the boundary
             surface of the N-dimensional region
    */
    template <Size i> class MultiCubicSpline {
        typedef typename detail::Int2Type<i>::c_spline c_spline;
        typedef typename detail::Int2Type<i>::c_splint c_splint;
        
      public:
        typedef typename c_splint::argument_type argument_type;
        typedef typename c_splint::result_type result_type;
        typedef typename c_splint::data_table data_table;
        typedef typename c_splint::return_type return_type;
        typedef typename c_splint::output_data output_data;
        typedef typename c_splint::dimensions dimensions;
        typedef typename c_splint::data data;
        
        MultiCubicSpline(const SplineGrid& grid, const data_table &y,
                         std::vector<bool> ae = {})
        : grid_(grid), y_(y), ae_(std::move(ae)), v_(grid), v1_(grid),
          v2_(grid), y2_(grid) {
            if (ae_.empty())
                ae_ = std::vector<bool>(grid.size(), false);
            set_shared_increments();
            c_spline(d_, d2_, y_, y2_, v_);
        }
        
        result_type operator()(const argument_type& x) const {
            set_shared_coefficients(x);
            c_splint(a_, b_, a2_, b2_, i_, d_, d2_, y_, y2_,
                     v_, v1_, v2_, res_);
            return res_;
        }
        void set_shared_increments() const;
        void set_shared_coefficients(const argument_type &x) const;
        
      private:
        const SplineGrid &grid_;
        const data_table &y_;
        std::vector<bool> ae_;
        mutable return_type a_, b_, a2_, b2_;
        mutable output_data v_, v1_, v2_;
        mutable result_type res_;
        mutable dimensions i_;
        mutable data d_, d2_;
        mutable data_table y2_;
    };

    // the data is checked and, in case of insufficient number of points,
    // exception is thrown BEFORE the main body of interpolation begins
    template <Size i>
    void MultiCubicSpline<i>::set_shared_increments() const {
        SplineGrid x(i), y(i);
        Size k = 0, dim = 0;
        for(Size j = 0; j < i; k = 0, ++j) {
            con