swap(Data<std::vector<Real>, EmptyArg> &d) noexcept {
                first.swap(d.first);
            }
            Real operator[](Size n) const {return first[n];}
            Real& operator[](Size n) {return first[n];}
            std::vector<Real> first;
            EmptyArg second;
        };

        typedef Data<std::vector<Real>, EmptyArg> base_data;

        template<class X, class Y> struct Point {
            typedef X data_type;
            Point()
            : first(data_type()), second(Y()) {}
            Point(const std::vector<Real>::const_iterator &i)
            : first(*i), second(i + 1) {}
            Point(const std::vector<Real> &v)
            : first(v[0]), second(v.begin()+1) {}
            Point(const SplineGrid::const_iterator &i)
            : first(i->size()), second(i + 1) {}
            Point(const SplineGrid &grid)
            : first(grid[0].size()), second(grid.begin()+1) {}
            operator data_type() const {
                return first;
            }
            data_type operator[](Size n) const { return n != 0U ? second[n - 1] : first; }
            data_type& operator[](Size n) { return n != 0U ? second[n - 1] : first; }
            data_type first;
            Y second;
        };

        template<> struct Point<Real, EmptyArg> {
            typedef Real data_type;
            Point(data_type s)
            : first(s) {}
            Point(const std::vector<Real>::const_iterator &i)
            : first(*i) {}
            Point(const std::vector<Real> &v)
            : first(v[0]) {}
            operator data_type() const {return first;}
            data_type operator[](Size n) const {
                QL_REQUIRE(n == 0, "operator[] : access violation");
                return first;
            }
            data_type& operator[](Size n) {
                QL_REQUIRE(n == 0, "operator[] : access violation");
                return first;
            }
            data_type first;
            EmptyArg second;
        };

        typedef Point<Real, EmptyArg> base_arg_type;

        template<> struct Point<Real, EmptyRes> {
            typedef Real data_type;
            Point()
            : first(data_type()) {}
            Point(data_type s)
            : first(s) {}
            operator data_type() const {return first;}
            const data_type &operator[](Size n) const {
                QL_REQUIRE(n == 0, "operator[] : access violation");
                return first;
            }
            data_type &operator[](Size n) {
                QL_REQUIRE(n == 0, "operator[] : access violation");
                return first;
            }
            data_type first;
            EmptyRes second;
        };

        typedef Point<Real, EmptyRes> base_return_type;

        template<> struct Point<Size, EmptyDim> {
            typedef Size data_type;
            Point()
            : first(data_type()) {}
            Point(data_type s)
            : first(s) {}
            operator data_type() const {return first;}
            data_type operator[](Size n) const {
                QL_REQUIRE(n == 0, "operator[] : access violation");
                return first;
            }
            data_type& operator[](Size n) {
                QL_REQUIRE(n == 0, "operator[] : access violation");
                return first;
            }
            data_type first;
            EmptyDim second;
        };

        typedef Point<Size, EmptyDim> base_dimensions;

        template<> struct Point<base_data_table, EmptyRes> {
            typedef base_data_table data_type;
            Point(data_type s) : first(std::move(s)) {}
            Point(const SplineGrid::const_iterator &i)
            : first(i->size()) {}
            Point(const SplineGrid &grid)
            : first(grid[0].size()) {}
            Real operator[](Size n) const {return first[n];}
            Real& operator[](Size n) {return first[n];}
            data_type first;
            EmptyRes second;
        };

        typedef Poin
