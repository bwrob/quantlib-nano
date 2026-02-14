()->first;
    }

    template <class T, class C>
    inline Size TimeSeries<T,C>::size() const {
        return values_.size();
    }

    template <class T, class C>
    inline bool TimeSeries<T,C>::empty() const {
        return values_.empty();
    }

    template <class T, class C>
    inline typename TimeSeries<T,C>::const_iterator
    TimeSeries<T,C>::cbegin() const {
        return values_.begin();
    }

    template <class T, class C>
    inline typename TimeSeries<T,C>::const_iterator
    TimeSeries<T,C>::cend() const {
        return values_.end();
    }

    template <class T, class C>
    inline typename TimeSeries<T,C>::const_iterator
    TimeSeries<T,C>::find(const Date& d) {
        auto i = values_.find(d);
        if (i == values_.end()) {
            values_[d] = Null<T>();
            i = values_.find(d);
        }
        return i;
    }

    template <class T, class C>
    std::vector<Date> TimeSeries<T,C>::dates() const {
        std::vector<Date> v;
        v.reserve(size());
        std::transform(cbegin(), cend(), std::back_inserter(v),
                       TimeSeries<T,C>::get_time);
        return v;
    }

    template <class T, class C>
    std::vector<T> TimeSeries<T,C>::values() const {
        std::vector<T> v;
        v.reserve(size());
        std::transform(cbegin(), cend(), std::back_inserter(v),
                       TimeSeries<T,C>::get_value);
        return v;
    }

}

#endif