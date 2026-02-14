class Flag : public QuantLib::Observer {
      private:
        bool up_ = false;

      public:
        Flag() = default;
        void raise() { up_ = true; }
        void lower() { up_ = false; }
        bool isUp() const { return up_; }
        void update() override { raise(); }
    };

    template<class Iterator>
    Real norm(const Iterator& begin, const Iterator& end, Real h) {
        // squared values
        std::vector<Real> f2(end-begin);
        std::transform(begin, end, begin, f2.begin(), std::multiplies<>());
        // numeric integral of f^2
        Real I = h * (std::accumulate(f2.begin(),f2.end(),Real(0.0))
                      - 0.5*f2.front() - 0.5*f2.back());
        return std::sqrt(I);
    }


    inline Integer timeToDays(Time t, Integer daysPerYear = 360) {
        return Integer(std::lround(t * daysPerYear));
    }


    // Used to check that an exception message contains the expected message string
    struct ExpectedErrorMessage {

        explicit ExpectedErrorMessage(std::string msg) : expected(std::move(msg)) {}

        bool operator()(const Error& ex) const {
            std::string actual(ex.what());
            if (actual.find(expected) == std::string::npos) {
                BOOST_TEST_MESSAGE("Error expected to contain: '" << expected << "'.");
                BOOST_TEST_MESSAGE("Actual error is: '" << actual << "'.");
                return false;
            } else {
                return true;
            }
        }

        std::string expected;
    };


    // Allow streaming vectors to error messages.

    // The standard forbids defining new overloads in the std
    // namespace, so we have to use a wrapper instead of overloading
    // operator<< to send a vector to the stream directly.
    // Defining the overload outside the std namespace wouldn't work
    // with Boost streams because of ADT name lookup rules.

    template <class T>
    struct vector_streamer {
        explicit vector_streamer(std::vector<T> v) : v(std::move(v)) {}
        std::vector<T> v;
    };

    template <class T>
    vector_streamer<T> to_stream(const std::vector<T>& v) {
        return vector_streamer<T>(v);
    }

    template <class T>
    std::ostream& operator<<(std::ostream& out, const vector_streamer<T>& s) {
        out << "{ ";
        if (!s.v.empty()) {
            for (size_t n=0; n<s.v.size()-1; ++n)
                out << s.v[n] << ", ";
            out << s.v.back();
        }
        out << " }";
        return out;
    }


}


#endif