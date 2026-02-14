& v2) {
        Array result = std::move(v2);
        std::transform(result.begin(), result.end(), result.begin(), [=](Real y) -> Real { return a / y; });
        return result;
    }

    // functions

    inline Array Abs(const Array& v) {
        Array result(v.size());
        std::transform(v.begin(), v.end(), result.begin(),
                       [](Real x) -> Real { return std::fabs(x); });
        return result;
    }

    inline Array Abs(Array&& v) {
        Array result = std::move(v);
        std::transform(result.begin(), result.end(), result.begin(),
                       [](Real x) -> Real { return std::fabs(x); });
        return result;
    }

    inline Array Sqrt(const Array& v) {
        Array result(v.size());
        std::transform(v.begin(),v.end(),result.begin(),
                       [](Real x) -> Real { return std::sqrt(x); });
        return result;
    }

    inline Array Sqrt(Array&& v) {
        Array result = std::move(v);
        std::transform(result.begin(), result.end(), result.begin(),
                       [](Real x) -> Real { return std::sqrt(x); });
        return result;
    }

    inline Array Log(const Array& v) {
        Array result(v.size());
        std::transform(v.begin(),v.end(),result.begin(),
                       [](Real x) -> Real { return std::log(x); });
        return result;
    }

    inline Array Log(Array&& v) {
        Array result = std::move(v);
        std::transform(result.begin(), result.end(), result.begin(),
                       [](Real x) -> Real { return std::log(x); });
        return result;
    }

    inline Array Exp(const Array& v) {
        Array result(v.size());
        std::transform(v.begin(), v.end(), result.begin(),
                       [](Real x) -> Real { return std::exp(x); });
        return result;
    }

    inline Array Exp(Array&& v) {
        Array result = std::move(v);
        std::transform(result.begin(), result.end(), result.begin(),
                       [](Real x) -> Real { return std::exp(x); });
        return result;
    }

    inline Array Pow(const Array& v, Real alpha) {
        Array result(v.size());
        std::transform(v.begin(), v.end(), result.begin(),
                       [=](Real x) -> Real { return std::pow(x, alpha); });
        return result;
    }

    inline Array Pow(Array&& v, Real alpha) {
        Array result = std::move(v);
        std::transform(result.begin(), result.end(), result.begin(),
                       [=](Real x) -> Real { return std::pow(x, alpha); });
        return result;
    }

    inline void swap(Array& v, Array& w) noexcept {
        v.swap(w);
    }

    inline std::ostream& operator<<(std::ostream& out, const Array& a) {
        std::streamsize width = out.width();
        out << "[ ";
        if (!a.empty()) {
            for (Size n=0; n<a.size()-1; ++n)
                out << std::setw(int(width)) << a[n] << "; ";
            out << std::setw(int(width)) << a.back();
        }
        out << " ]";
        return out;
    }

}


#endif