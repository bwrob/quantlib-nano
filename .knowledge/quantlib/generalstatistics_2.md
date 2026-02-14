tistics::add(Real value, Real weight) {
        QL_REQUIRE(weight>=0.0, "negative weight not allowed");
        samples_.emplace_back(value, weight);
        sorted_ = false;
    }

    inline void GeneralStatistics::reset() {
        samples_ = std::vector<std::pair<Real,Real> >();
        sorted_ = true;
    }

    inline void GeneralStatistics::reserve(Size n) const {
        samples_.reserve(n);
    }

    inline void GeneralStatistics::sort() const {
        if (!sorted_) {
            std::sort(samples_.begin(), samples_.end());
            sorted_ = true;
        }
    }

}


#endif
