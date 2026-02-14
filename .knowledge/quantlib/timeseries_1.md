ypename const_iterator::iterator_category iterator_category;

        // Reverse iterators
        // The following class makes compilation fail for the code
        // that calls rbegin or rend with a container that does not
        // support reverse iterators.  All the rest TimeSeries class
        // features should compile and work for this type of
        // containers.
        template <class container, class iterator_category>
        struct reverse {
            typedef std::reverse_iterator<typename container::const_iterator>
                                                       const_reverse_iterator;
            reverse(const container& c) : c_(c) {}
            const_reverse_iterator rbegin() const {
                return const_reverse_iterator(c_.end());
            }
            const_reverse_iterator rend() const {
                return const_reverse_iterator(c_.begin());
            }
            const container& c_;
        };

        // This class defines reverse iterator features via
        // container's native calls.
        template <class container>
        struct reverse<container, std::bidirectional_iterator_tag> {
            typedef typename container::const_reverse_iterator
                                                       const_reverse_iterator;
            reverse(const container& c) : c_(c) {}
            const_reverse_iterator rbegin() const { return c_.rbegin(); }
            const_reverse_iterator rend() const { return c_.rend(); }
            const container& c_;
        };

        // The following typedef enables reverse iterators for
        // bidirectional_iterator_tag category.
        typedef std::conditional_t<
                std::is_same_v<iterator_category, std::bidirectional_iterator_tag> ||
                std::is_base_of_v<std::bidirectional_iterator_tag, iterator_category>,
            std::bidirectional_iterator_tag, std::input_iterator_tag> enable_reverse;

        typedef typename
        reverse<Container, enable_reverse>::const_reverse_iterator
                                                       const_reverse_iterator;

        const_iterator cbegin() const;
        const_iterator cend() const;
        const_iterator begin() const { return cbegin(); }
        const_iterator end() const { return cend(); }
        const_reverse_iterator crbegin() const {
            return reverse<Container, enable_reverse>(values_).rbegin();
        }
        const_reverse_iterator crend() const {
            return reverse<Container, enable_reverse>(values_).rend();
        }
        const_reverse_iterator rbegin() const { return crbegin(); }
        const_reverse_iterator rend() const { return crend(); }
        //@}

      private:
        typedef typename Container::value_type container_value_type;
        typedef std::function<Date(const container_value_type&)>
                                                              projection_time;
        typedef std::function<T(const container_value_type&)>
                                                             projection_value;

      public:
        //! \name Utilities
        //@{
        const_iterator find(const Date&);
        //! returns the dates for which historical data exist
        std::vector<Date> dates() const;
        //! returns the historical data
        std::vector<T> values() const;
        //@}

      private:
        static const Date& get_time (const container_value_type& v) {
            return v.first;
        }
        static const T& get_value (const container_value_type& v) {
            return v.second;
        }
    };


    // inline definitions

    template <class T, class C>
    inline Date TimeSeries<T,C>::firstDate() const {
        QL_REQUIRE(!values_.empty(), "empty timeseries");
        return values_.begin()->first;
    }

    template <class T, class C>
    inline Date TimeSeries<T,C>::lastDate() const {
        QL_REQUIRE(!values_.empty(), "empty timeseries");
        return rbegin